import sqlite3
import pandas as pd
from pathlib import Path

with sqlite3.connect("phase2/03_sqlite_postgresql_minions/mina_de_datos.db") as conn:
    cur = conn.cursor()
    cur.execute ("PRAGMA foreign_keys = ON;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS personajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            clase TEXT NOT NULL ,
            nivel INTEGER NOT NULL DEFAULT 0 CHECK(nivel >= 0),
            UNIQUE(nombre)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dificultad TEXT NOT NULL CHECK (dificultad IN ('easy','normal','hard')),
            personaje_id INTEGER NOT NULL REFERENCES personajes(id) ON DELETE CASCADE,
            UNIQUE(nombre)
        );
    """)

    items = [
        ("lea", "hechicera", 5),
        ("kronk", "guerrero", 10),
        ("arthur", "pícaro", 7)
    ]
    cur.executemany("INSERT OR IGNORE INTO personajes(nombre, clase, nivel) VALUES(?, ?, ?);",
                        items
        )

    mision_items = [
        ("cazando jabalís marrones", "easy", 1),
        ("la senda de la luna roja", "hard", 3),
        ("domando al dragón dorado", "hard", 2),
        ("Caminos lúgrubres", "normal",1),
        ("derrota al jefe goblin", "normal",2)
    ]
    cur.executemany("INSERT OR IGNORE INTO misiones(nombre, dificultad, personaje_id) VALUES(?, ?, ?);",
                        mision_items 
        )

    # Check if the 'recompensa' column exists(done by AI, not by user)
    cur.execute("PRAGMA table_info(misiones);")
    columns = [col[1] for col in cur.fetchall()]
    if 'recompensa' not in columns:
        cur.execute("ALTER TABLE misiones ADD COLUMN recompensa INTEGER;")
    
    cur.executemany("UPDATE misiones SET recompensa = ? WHERE dificultad = ?;", [(100, 'easy'), (1000, 'normal'), (10000, 'hard')])

    # # Consultar personajes
    cur.execute("SELECT id, nombre, clase, nivel FROM personajes;")
    personajes = cur.fetchall()
    for p in personajes:
        print(f"Personaje: {p[1]}, Clase: {p[2]}, Nivel: {p[3]}")
    print("---------------------")
    # # Consultar las misiones de un personaje concreto
    cur.execute("""SELECT p.nombre, p. clase, p.nivel, m.nombre, m.dificultad
                FROM personajes p
                JOIN misiones m ON p.id = m.personaje_id
                WHERE p.id = 1;""")
    misiones = cur.fetchall()
    for m in misiones:
        print(f"Personaje: {m[0]}, Clase: {m[1]}, Nivel: {m[2]}, Misión: {m[3]}, Dificultad: {m[4]}")
    print("---------------------")

    cur.execute("SELECT p.nombre, COUNT(m.id) AS total_misiones FROM personajes p LEFT JOIN misiones m ON p.id = m.personaje_id GROUP BY p.id;")
    total_misiones = cur.fetchall()
    for tm in total_misiones:
        print(f"Personaje: {tm[0]}, Total Misiones: {tm[1]}")
    print("---------------------")

    cur.execute("SELECT nombre, dificultad FROM misiones WHERE dificultad = 'hard';")
    misiones_dificultad = cur.fetchall()
    for md in misiones_dificultad:
        print(f"Misión: {md[0]}, Dificultad: {md[1]}") 
    print("---------------------")  
    
    df = pd.read_sql_query("""
    SELECT M.id, M.nombre, M.dificultad, P.nombre AS personaje, P.clase, P.nivel
    FROM Misiones M
    JOIN Personajes P ON P.id = M.personaje_id
    ORDER BY M.id;
    """, conn)

    df.to_csv(Path("phase2/03_sqlite_postgresql_minions/reporte_misiones.csv"),index=False, encoding="utf-8")
