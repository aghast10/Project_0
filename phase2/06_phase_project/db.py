import sqlite3
from paths import FORECAST_DATABASE
from api import ApiClient
#DDL: Data Definition Language
DDL = [
    """
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        lat REAL,
        lon REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS forecast_daily (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        t_min REAL,
        t_max REAL,
        UNIQUE(location_id, date),
        FOREIGN KEY(location_id) REFERENCES locations(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS forecast_hourly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER NOT NULL,
        datetime TEXT NOT NULL,
        temp REAL,
        UNIQUE(location_id, datetime),
        FOREIGN KEY(location_id) REFERENCES locations(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS forecast_archive (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        t_min REAL,
        t_max REAL,
        precip_sum REAL,
        rain_sum REAL,
        UNIQUE(location_id, date),
        FOREIGN KEY(location_id) REFERENCES locations(id)
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_daily_loc_date ON forecast_daily(location_id, date);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_hourly_loc_datetime ON forecast_hourly(location_id, datetime);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_hourly_loc_date ON forecast_archive(location_id, date);
    """,
]
# UNIQUE(location_id, date): esto indica que el par location, date ha de ser unico, pero por separado pueden repetirse.
# creamos un indice para cada par location_id, date en cada tabla.

def init_db():
    with sqlite3.connect(FORECAST_DATABASE) as conn:
        cur = conn.cursor()
        for stmt in DDL: #stmt: statement
            cur.execute(stmt)

def insert_into_locations(apiobject: ApiClient):
    with sqlite3.connect(FORECAST_DATABASE) as conn:
        cur = conn.cursor()
        for city in apiobject.cities:
            lat, lon = apiobject.geocode(city)
            cur.execute("INSERT OR IGNORE INTO locations(name, lat, lon) VALUES(?, ?, ?);",
                        (city, lat, lon))
def location_id(name): 
    with sqlite3.connect(FORECAST_DATABASE) as conn:
        cur = conn.cursor()
        row = cur.execute("SELECT id FROM locations WHERE name = ?", (name,)).fetchone() #fetchone sirve para entregar los valores de la fila.
        return row[0] #[0] es la columna id, la que nos interesa.

def insert_into_forecast_daily(apiobject: ApiClient):
    fc = apiobject.forecast_daily_list() 
    with sqlite3.connect(FORECAST_DATABASE) as conn:
        cur = conn.cursor()
        for i, date in enumerate(fc['time']):
            loc = location_id(fc['city'][i]) #fc['city'][i] devuelve el nombre de la ciudad
            t_min = fc['temperature_2m_min'][i]
            t_max = fc['temperature_2m_max'][i]
            cur.execute("INSERT OR IGNORE INTO forecast_daily(location_id, date, t_min, t_max) VALUES(?, ?, ?, ?);",
                        (loc, date, t_min, t_max))

def insert_into_forecast_hourly(apiobject: ApiClient):
    fc = apiobject.forecast_hourly_list() 
    with sqlite3.connect(FORECAST_DATABASE) as conn:
        cur = conn.cursor()
        for i, date in enumerate(fc['time']):
            loc = location_id(fc['city'][i])
            temp = fc['temperature_2m'][i]
            cur.execute("INSERT OR IGNORE INTO forecast_hourly(location_id, datetime, temp) VALUES(?, ?, ?);",
                        (loc, date, temp))

def insert_into_forecast_archive(apiobject: ApiClient):
    fc = apiobject.forecast_annually_daily_list()
    with sqlite3.connect(FORECAST_DATABASE) as conn:
        cur = conn.cursor()
        for i, date in enumerate(fc['time']):
            loc = location_id(fc['city'][i])
            t_min = fc['temperature_2m_min'][i]
            t_max = fc['temperature_2m_max'][i]
            precip_sum = fc['precipitation_sum'][i]
            rain_sum = fc['rain_sum'][i]
            cur.execute("INSERT OR IGNORE INTO forecast_archive(location_id, date, t_min, t_max, precip_sum, rain_sum) VALUES(?, ?, ?, ?, ?, ?);",
                        (loc, date, t_min, t_max, precip_sum, rain_sum))

def pipeline(apiobject: ApiClient):
    init_db()
    insert_into_locations(apiobject)
    insert_into_forecast_daily(apiobject)
    insert_into_forecast_hourly(apiobject)
    insert_into_forecast_archive(apiobject)