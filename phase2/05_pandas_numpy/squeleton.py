import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

BASE_DIR = Path('phase2/05_pandas_numpy')
EXPORT_DIR = BASE_DIR / 'exports'
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

USERS_JSON = Path('phase2/04_api_requests/02_validated_user_array.json')

np.random.seed(42)

# ------------------------
# 1) Carga usuarios (roca base)
# ------------------------
if not USERS_JSON.exists():
    raise FileNotFoundError("No encuentro 02_validated_user_array.json. Ejecuta la semana 6 primero.")

users = pd.read_json(USERS_JSON)
# Asegura columnas básicas
users = users[[
    'id','name','username','email','address','phone','website','company'
]]

# Extrae campos anidados útiles (ciudad y compañía)
users['city'] = users['address'].apply(lambda d: d['city'])
users['company_name'] = users['company'].apply(lambda d: d['name'])
users = users.drop(columns=['address','company'])

# ------------------------
# 2) Genera transacciones sintéticas con NumPy (roca a tallar)
# ------------------------
N = 5_000  # tamaño moderado
user_ids = users['id'].to_numpy()

start = datetime(2024, 1, 1)
end = datetime(2024, 12, 31)
span_days = (end - start).days + 1

# Utiliza NumPy para generar columnas vectorizadas
trx_user_id = np.random.choice(user_ids, size=N)
trx_days = np.random.randint(0, span_days, size=N)
trx_date = np.array([start + timedelta(days=int(d)) for d in trx_days])

categories = np.array(['alimentos','ocio','suscripciones','transporte','salud','otros'])
trx_category = np.random.choice(categories, size=N, p=[.35,.2,.15,.15,.1,.05])

# Importes con distribución lognormal para simular sesgo positivo
amount = np.random.lognormal(mean=2.5, sigma=0.6, size=N)
# Añade variación por categoría (broadcasting)
cat_multiplier = {
    'alimentos': 1.0,
    'ocio': 1.3,
    'suscripciones': 0.6,
    'transporte': 0.8,
    'salud': 1.5,
    'otros': 0.9,
}
mult = np.vectorize(cat_multiplier.get)(trx_category)
trx_amount = np.round(amount * mult, 2)

# Introduce algunos nulos/ruido controlado para practicar limpieza
mask_null = np.random.rand(N) < 0.01
trx_category[mask_null] = None

transactions = pd.DataFrame({
    'trx_id': np.arange(1, N+1),
    'user_id': trx_user_id,
    'date': trx_date,
    'category': trx_category,
    'amount': trx_amount,
})

# ------------------------
# 3) Limpieza & tipado
# ------------------------
transactions['date'] = pd.to_datetime(transactions['date'])
# Rellena categoría nula con 'sin_clasificar'
transactions['category'] = transactions['category'].fillna('sin_clasificar')
# Asegura tipo numérico (por si viniera como object)
transactions['amount'] = pd.to_numeric(transactions['amount'], errors='coerce')

# ------------------------
# 4) Selección y filtrado (gemas emergen)
# ------------------------
# a) Subconjunto por fecha y cantidad
from_date = pd.Timestamp('2024-06-01')
mask = (transactions['date'] >= from_date) & (transactions['amount'] > 5)
subset = transactions.loc[mask, ['trx_id','user_id','date','category','amount']]

# b) query de Pandas (equivalente)
subset_q = transactions.query("date >= @from_date and amount > 5")

# c) iloc (posicional) y loc (etiquetas)
sample_loc = transactions.loc[transactions.index[:5], ['trx_id','amount']]
sample_iloc = transactions.iloc[:5, :3]

# ------------------------
# 5) Agregaciones y agrupaciones
# ------------------------
# Gasto total por usuario y categoría
agg_user_cat = (
    transactions
    .groupby(['user_id','category'], as_index=False)
    .agg(total=('amount','sum'),
         media=('amount','mean'),
         n=('amount','size'))
)

# Top categorías globales
top_categories = (
    transactions.groupby('category')['amount']
    .agg(total='sum', media='mean', n='size')
    .sort_values('total', ascending=False)
    .reset_index()
)

# Tabla pivote mensual por categoría
transactions['year_month'] = transactions['date'].dt.to_period('M')
pivot_month_cat = pd.pivot_table(
    transactions,
    values='amount',
    index='year_month',
    columns='category',
    aggfunc='sum',
    fill_value=0.0
).astype(float)

# Rolling window (media móvil de 3 meses sobre total global)
monthly_total = transactions.set_index('date')['amount'].resample('M').sum()
rolling_3m = monthly_total.rolling(3).mean()

# ------------------------
# 6) Joins/merge con usuarios
# ------------------------
trx_users = transactions.merge(users[['id','city','company_name']], left_on='user_id', right_on='id', how='left')
trx_users = trx_users.drop(columns=['id'])

# Gasto por ciudad
spend_city = trx_users.groupby('city')['amount'].sum().sort_values(ascending=False).reset_index()

# ------------------------
# 7) NumPy avanzado (vectorización extra)
#   Aplica un descuento del 5% a 'suscripciones' y un recargo del 10% a 'ocio',
#   usando máscaras booleanas vectorizadas.

is_sub = (transactions['category'].to_numpy() == 'suscripciones')
is_ocio = (transactions['category'].to_numpy() == 'ocio')
amount_np = transactions['amount'].to_numpy(dtype=float)
amount_np = np.where(is_sub, amount_np * 0.95, amount_np)
amount_np = np.where(is_ocio, amount_np * 1.10, amount_np)
transactions['amount_adjusted'] = np.round(amount_np, 2)

# ------------------------
# 8) Exportación a CSV (gemas pulidas)
# ------------------------
now_tag = datetime.now().strftime('%Y%m%d_%H%M%S')

transactions.to_csv(EXPORT_DIR / f'transactions_{now_tag}.csv', index=False)
agg_user_cat.to_csv(EXPORT_DIR / f'agg_user_cat_{now_tag}.csv', index=False)
top_categories.to_csv(EXPORT_DIR / f'top_categories_{now_tag}.csv', index=False)
pivot_month_cat.to_csv(EXPORT_DIR / f'pivot_month_cat_{now_tag}.csv')
spend_city.to_csv(EXPORT_DIR / f'spend_city_{now_tag}.csv', index=False)

# ------------------------
# 9) Resumen para la corte
# ------------------------
print("\n=== RESUMEN DE GEMAS ===")
print(f"Transacciones: {len(transactions):,}")
print("Top 5 categorías por gasto total:\n", top_categories.head(5))
print("Top 5 ciudades por gasto:\n", spend_city.head(5))
print("CSV exportados en:", EXPORT_DIR.resolve())