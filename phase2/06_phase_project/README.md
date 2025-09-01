## `README.md`

Proyecto educativo: descarga datos de Open‑Meteo para varias ciudades de España, los guarda en SQLite y genera KPIs en CSV.

---

## 📁 Árbol de proyecto propuesto

```
phase2/06_phase_project/
├─ src/
│  ├─ api.py
│  ├─ db.py
│  ├─ transform.py
│  ├─ main.py
│  └─ paths.py
├─ exports/               # se crea automáticamente
├─ README.md
└─ requirements.txt
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso rápido

Ejecuta main.py. 
Por defecto las ciudades son una lista de ciudades españolas y el año del archivo 2024, pero se puede modificar en main.py.

Los CSV/DB se generan en `exports/`.

## Estructura de datos y DB

- `locations(id, name, lat, lon)`
- `forecast_daily(location_id, date, t_min, t_max)`
- `forecast_hourly(location_id, ts, temp)`
- `forecast_archive(id, name, lat, lon, precip_sum, rain_sum)`


Índices:

- `idx_daily_loc_date` en `(location_id, date)`
- `idx_hourly_loc_datetime` en `(location_id, datetime)`
- `idx_archive_loc_date` en `(location_id, date)`


## KPIs incluidos

- **Hottest days** (`t_max`)
- **Rainiest days** (`rain_sum`)
- **Rain % por ciudad** (días con lluvia / total)