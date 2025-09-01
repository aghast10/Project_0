# Refactor de `phase2/06_phase_project`

A continuación tienes una propuesta **modular**, con **CLI** y **modelo relacional** en SQLite. Copia estos archivos en tu repo siguiendo el árbol indicado. Mantengo compatibilidad con tus rutas en `paths.py` y extiendo funcionalidades sin cambiar la fuente de datos (Open‑Meteo).

---

## 📁 Árbol de proyecto propuesto

```markdown
phase2/06_phase_project/
├─ src/
│  ├─ __init__.py
│  ├─ api.py
│  ├─ db.py
│  ├─ transform.py
│  ├─ cli.py
│  └─ paths.py
├─ exports/               # se crea automáticamente
├─ README.md
└─ requirements.txt
```

> **Nota**: He movido tu lógica de `db.py` (monolítica) a `src/api.py`, `src/db.py`, `src/transform.py` y un CLI en `src/cli.py`. Tus constantes de rutas/URLs siguen en `src/paths.py`.

---

## `src/paths.py`

```python
from pathlib import Path

# Raíz del proyecto (esta carpeta)
BASE_DIR = Path(__file__).resolve().parents[1] / "phase2" / "06_phase_project"
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Archivos intermedios (JSON)
FORECAST_DAILY_JSON = EXPORT_DIR / 'forecast_daily.json'
FORECAST_HOURLY_JSON = EXPORT_DIR / 'forecast_hourly.json'
FORECAST_ANNUALLY_DAILY_JSON = EXPORT_DIR / 'forecast_annually.json'

# Base de datos
FORECAST_DATABASE = EXPORT_DIR / 'forecast.db'

# Endpoints
URL_GEOCODE = 'https://geocoding-api.open-meteo.com/v1/search'
URL_FORECAST = 'https://api.open-meteo.com/v1/forecast'
URL_ARCHIVE = 'https://archive-api.open-meteo.com/v1/archive'
```

---

## `src/api.py`

```python
from __future__ import annotations
import requests
from typing import List, Tuple, Dict, Any

from .paths import URL_GEOCODE, URL_FORECAST, URL_ARCHIVE


class ApiClient:
    """Cliente para Open‑Meteo (geocoding, forecast, archive)."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def geocode(self, city: str) -> Tuple[float, float]:
        r = self.session.get(
            URL_GEOCODE,
            params={"name": city, "language": "en"},
            timeout=self.timeout,
        )
        r.raise_for_status()
        data = r.json()
        res = data.get("results") or []
        if not res:
            raise ValueError(f"No se encontraron coordenadas para {city!r}")
        lat = float(res[0]["latitude"])  # type: ignore[index]
        lon = float(res[0]["longitude"])  # type: ignore[index]
        return lat, lon

    def forecast_raw(self, city: str, timezone: str = "Europe/Madrid") -> Dict[str, Any]:
        lat, lon = self.geocode(city)
        r = self.session.get(
            URL_FORECAST,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "rain_sum"],
                "hourly": "temperature_2m",
                "timezone": timezone,
            },
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def archive_daily_raw(self, city: str, year: int) -> Dict[str, Any]:
        lat, lon = self.geocode(city)
        r = self.session.get(
            URL_ARCHIVE,
            params={
                "latitude": lat,
                "longitude": lon,
                "start_date": f"{year}-01-01",
                "end_date": f"{year}-12-31",
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "rain_sum",
                ],
                "timezone": "UTC",
            },
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    # Helpers para listas tabulares
    def build_forecast_daily(self, cities: List[str], timezone: str = "Europe/Madrid") -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for city in cities:
            raw = self.forecast_raw(city, timezone=timezone)
            for i, dt in enumerate(raw["daily"]["time"]):
                rows.append({
                    "date": dt,
                    "t_min": raw["daily"]["temperature_2m_min"][i],
                    "t_max": raw["daily"]["temperature_2m_max"][i],
                    "precip_sum": raw["daily"].get("precipitation_sum", [None] * 1000)[i],
                    "rain_sum": raw["daily"].get("rain_sum", [None] * 1000)[i],
                    "city": city,
                })
        return rows

    def build_forecast_hourly(self, cities: List[str], timezone: str = "Europe/Madrid") -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for city in cities:
            raw = self.forecast_raw(city, timezone=timezone)
            for i, ts in enumerate(raw["hourly"]["time"]):
                rows.append({
                    "ts": ts,
                    "temp": raw["hourly"]["temperature_2m"][i],
                    "city": city,
                })
        return rows

    def build_archive_daily(self, cities: List[str], year: int) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for city in cities:
            raw = self.archive_daily_raw(city, year)
            for i, dt in enumerate(raw["daily"]["time"]):
                rows.append({
                    "date": dt,
                    "t_min": raw["daily"]["temperature_2m_min"][i],
                    "t_max": raw["daily"]["temperature_2m_max"][i],
                    "precip_sum": raw["daily"]["precipitation_sum"][i],
                    "rain_sum": raw["daily"]["rain_sum"][i],
                    "city": city,
                })
        return rows
```

---

## `src/db.py`

```python
from __future__ import annotations
import sqlite3
from typing import Iterable, Tuple, Dict, Any
from contextlib import closing

from .paths import FORECAST_DATABASE


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
        precip_sum REAL,
        rain_sum REAL,
        UNIQUE(location_id, date),
        FOREIGN KEY(location_id) REFERENCES locations(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS forecast_hourly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER NOT NULL,
        ts TEXT NOT NULL,
        temp REAL,
        UNIQUE(location_id, ts),
        FOREIGN KEY(location_id) REFERENCES locations(id)
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_daily_loc_date ON forecast_daily(location_id, date);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_hourly_loc_ts ON forecast_hourly(location_id, ts);
    """,
]


def connect():
    return sqlite3.connect(FORECAST_DATABASE)


def init_db() -> None:
    with connect() as conn:
        for stmt in DDL:
            conn.executescript(stmt)


def upsert_location(conn: sqlite3.Connection, name: str, lat: float | None = None, lon: float | None = None) -> int:
    conn.execute(
        "INSERT OR IGNORE INTO locations(name, lat, lon) VALUES(?, ?, ?)", (name, lat, lon)
    )
    row = conn.execute("SELECT id FROM locations WHERE name = ?", (name,)).fetchone()
    assert row is not None
    return int(row[0])


def insert_daily(conn: sqlite3.Connection, rows: Iterable[Dict[str, Any]]) -> None:
    data = []
    for r in rows:
        data.append((r["city"], r.get("lat"), r.get("lon"), r["date"], r.get("t_min"), r.get("t_max"), r.get("precip_sum"), r.get("rain_sum")))
    with closing(conn.cursor()) as cur:
        for (city, lat, lon, date, t_min, t_max, precip_sum, rain_sum) in data:
            loc_id = upsert_location(conn, city, lat, lon)
            cur.execute(
                """
                INSERT OR REPLACE INTO forecast_daily(location_id, date, t_min, t_max, precip_sum, rain_sum)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (loc_id, date, t_min, t_max, precip_sum, rain_sum),
            )


def insert_hourly(conn: sqlite3.Connection, rows: Iterable[Dict[str, Any]]) -> None:
    with closing(conn.cursor()) as cur:
        for r in rows:
            loc_id = upsert_location(conn, r["city"], r.get("lat"), r.get("lon"))
            cur.execute(
                """
                INSERT OR REPLACE INTO forecast_hourly(location_id, ts, temp)
                VALUES (?, ?, ?)
                """,
                (loc_id, r["ts"], r.get("temp")),
            )
```

---

## `src/transform.py`

```python
from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import List

from .paths import EXPORT_DIR


def df_to_csv(df: pd.DataFrame, name: str) -> Path:
    out = EXPORT_DIR / name
    df.to_csv(out, index=False)
    return out


def kpi_hottest_days(df_daily: pd.DataFrame, top_n: int = 11) -> pd.DataFrame:
    cols = ["date", "city", "t_max"]
    return (df_daily.sort_values("t_max", ascending=False)
            .loc[:, cols]
            .head(top_n)
            .reset_index(drop=True))


def kpi_rainiest_days(df_daily: pd.DataFrame, top_n: int = 11) -> pd.DataFrame:
    cols = ["date", "city", "rain_sum"]
    return (df_daily.sort_values("rain_sum", ascending=False)
            .loc[:, cols]
            .head(top_n)
            .reset_index(drop=True))


def kpi_rain_percentage(df_daily: pd.DataFrame, year: int) -> pd.DataFrame:
    tmp = df_daily.assign(did_rain=(df_daily["rain_sum"].fillna(0) > 0))
    out = (tmp.groupby("city", as_index=False)["did_rain"].mean()
           .rename(columns={"did_rain": "percentage"}))
    out["percentage"] = (out["percentage"] * 100).round(1)
    out["year"] = year
    return out.loc[:, ["year", "city", "percentage"]]


def kpi_amplitud_termica(df_daily: pd.DataFrame) -> pd.DataFrame:
    out = df_daily.copy()
    out["amplitude"] = out["t_max"] - out["t_min"]
    return out.loc[:, ["date", "city", "amplitude"]]


def kpi_tendencia(df_daily: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    tmp = df_daily.sort_values(["city", "date"]).copy()
    tmp["t_max_ma"] = tmp.groupby("city")["t_max"].transform(lambda s: s.rolling(window, min_periods=1).mean())
    return tmp.loc[:, ["date", "city", "t_max_ma"]]
```

---

## `src/cli.py`

```python
from __future__ import annotations
import argparse
import json
from datetime import datetime
import pandas as pd

from .api import ApiClient
from . import db as dbmod
from .paths import (
    FORECAST_DAILY_JSON,
    FORECAST_HOURLY_JSON,
    FORECAST_ANNUALLY_DAILY_JSON,
    EXPORT_DIR,
)
from .transform import (
    df_to_csv,
    kpi_hottest_days,
    kpi_rainiest_days,
    kpi_rain_percentage,
    kpi_amplitud_termica,
    kpi_tendencia,
)

DEFAULT_CITIES = ["MADRID", "OVIEDO", "ZARAGOZA", "BARCELONA", "VALENCIA", "SEVILLA", "BILBAO"]


def cmd_fetch(args: argparse.Namespace) -> None:
    api = ApiClient()

    cities = args.cities or DEFAULT_CITIES
    year = int(args.year)

    # Construir datasets
    daily_rows = api.build_forecast_daily(cities=cities)
    hourly_rows = api.build_forecast_hourly(cities=cities)
    annual_rows = api.build_archive_daily(cities=cities, year=year)

    # Guardar JSON intermedios
    for path, rows in [
        (FORECAST_DAILY_JSON, daily_rows),
        (FORECAST_HOURLY_JSON, hourly_rows),
        (FORECAST_ANNUALLY_DAILY_JSON, annual_rows),
    ]:
        path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    # Inicializar DB y cargar
    dbmod.init_db()
    with dbmod.connect() as conn:
        dbmod.insert_daily(conn, daily_rows)
        dbmod.insert_hourly(conn, hourly_rows)

    # KPIs rápidos a CSV
    df_daily = pd.DataFrame(annual_rows)  # para KPIs de 2024
    df_forecast_daily = pd.DataFrame(daily_rows)

    today_tag = datetime.now().strftime("%Y%m%d")
    df_to_csv(kpi_hottest_days(df_daily), f"hottest_days_{year}.csv")
    df_to_csv(kpi_rainiest_days(df_daily), f"rainiest_days_{year}.csv")
    df_to_csv(kpi_rain_percentage(df_daily, year), f"rain_days_{year}.csv")
    df_to_csv(kpi_hottest_days(df_forecast_daily), f"forecasted_hottest_days_{today_tag}.csv")

    if args.extras:
        df_to_csv(kpi_amplitud_termica(df_daily), f"amplitud_termica_{year}.csv")
        df_to_csv(kpi_tendencia(df_daily, window=14), f"tendencia14_{year}.csv")
        df_to_csv(kpi_tendencia(df_daily, window=30), f"tendencia30_{year}.csv")

    print(f"Descargas y KPIs guardados en {EXPORT_DIR}")


def cmd_analyze(args: argparse.Namespace) -> None:
    year = int(args.year)
    df_daily = pd.read_json(FORECAST_ANNUALLY_DAILY_JSON)

    if args.metric == "hottest":
        out = kpi_hottest_days(df_daily)
        path = df_to_csv(out, f"hottest_days_{year}.csv")
    elif args.metric == "rainiest":
        out = kpi_rainiest_days(df_daily)
        path = df_to_csv(out, f"rainiest_days_{year}.csv")
    elif args.metric == "rain_pct":
        out = kpi_rain_percentage(df_daily, year)
        path = df_to_csv(out, f"rain_days_{year}.csv")
    elif args.metric == "amplitude":
        out = kpi_amplitud_termica(df_daily)
        path = df_to_csv(out, f"amplitud_termica_{year}.csv")
    elif args.metric == "trend14":
        out = kpi_tendencia(df_daily, window=14)
        path = df_to_csv(out, f"tendencia14_{year}.csv")
    elif args.metric == "trend30":
        out = kpi_tendencia(df_daily, window=30)
        path = df_to_csv(out, f"tendencia30_{year}.csv")
    else:
        raise SystemExit("Métrica no reconocida")

    print(f"CSV generado: {path}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="weather", description="API → SQLite → KPIs en CSV")
    sub = p.add_subparsers(dest="cmd", required=True)

    # fetch
    pf = sub.add_parser("fetch", help="Descargar datos y cargar DB + KPIs")
    pf.add_argument("--cities", nargs="+", help="Lista de ciudades (por defecto predefinidas)")
    pf.add_argument("--year", type=int, default=2024, help="Año para histórico (archive)")
    pf.add_argument("--extras", action="store_true", help="Exportar KPIs adicionales")
    pf.set_defaults(func=cmd_fetch)

    # analyze
    pa = sub.add_parser("analyze", help="Generar CSV de una métrica concreta a partir del JSON anual")
    pa.add_argument("--year", type=int, default=2024)
    pa.add_argument(
        "--metric",
        choices=["hottest", "rainiest", "rain_pct", "amplitude", "trend14", "trend30"],
        default="hottest",
    )
    pa.set_defaults(func=cmd_analyze)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
```

---

## `src/__init__.py`

```python
# Permite ejecutar: python -m src.cli fetch ...
```

---

## `requirements.txt`

```markdown
requests>=2.32
pandas>=2.2
requests-cache>=1.2
```

*(sqlite3 es parte de la librería estándar de Python)*

---

## `README.md`

```markdown
# Weather Oracle — Phase 2 (API → SQLite → CSV)

Proyecto educativo: descarga datos de Open‑Meteo para varias ciudades de España, los guarda en SQLite y genera KPIs en CSV.

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso rápido

```bash
# 1) Descarga forecast + archivo anual 2024, carga SQLite y exporta KPIs básicos
python -m src.cli fetch --year 2024

# 2) Analiza una métrica concreta desde el JSON anual (sin llamar a la API)
python -m src.cli analyze --year 2024 --metric hottest
```

Los CSV/DB se generan en `exports/`.

## Estructura de datos y DB

- `locations(id, name, lat, lon)`
- `forecast_daily(location_id, date, t_min, t_max, precip_sum, rain_sum)`
- `forecast_hourly(location_id, ts, temp)`

Índices:

- `idx_daily_loc_date` en `(location_id, date)`
- `idx_hourly_loc_ts` en `(location_id, ts)`

## KPIs incluidos

- **Hottest days** (`t_max`)
- **Rainiest days** (`rain_sum`)
- **Rain % por ciudad** (días con lluvia / total)
- **Amplitud térmica** (`t_max - t_min`) *(extra)*
- **Tendencia 14/30** (media móvil de `t_max`) *(extra)*
