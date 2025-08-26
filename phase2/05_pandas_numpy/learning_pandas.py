# 
# Config & paths: definir BASE_DIR, EXPORT_DIR, semilla NumPy.
# Carga usuarios: leer JSON, seleccionar columnas base, extraer city y company_name, tipar. (Tu JSON viene de la semana anterior).
# Generación de transacciones (sintético): fechas en 2024, categorías, importes lognormales + multiplicadores por categoría, introducir ruido (nulos controlados).
# Limpieza & tipado: fechas → datetime, rellenar nulos de categoría, asegurar amount numérico.
# Selección/filtrado: máscara por fecha/importe; query; loc/iloc. (Cuenta como 3 técnicas).
# Agregaciones: groupby(...).agg(sum, mean, size), top de categorías, resample mensual + rolling(3).
# Joins: unir transactions con users para métricas por ciudad/compañía.
# Transformaciones NumPy: descuentos/recargos con np.where, ufunc (p. ej. np.log1p) en una nueva columna.
# Exportación CSV: al menos: transactions_*.csv, agg_user_cat_*.csv, top_categories_*.csv, pivot_month_cat_*.csv, spend_city_*.csv.
# Resumen final: imprimir contadores + top‑5 de categorías/ciudades + ruta de exportación.
# BASE_DIR = Path("phase2/05_pandas_numpy")
# EXPORT_DIR = Path(BASE_DIR / "exports") # establece ruta: 05_pandas_numpy/exports
# EXPORT_DIR.mkdir(parents=True, exist_ok=True) #crea la carpeta y las anteriores(parents=True) exports si no existe (exists_ok=true)
# USERS_JSON = Path("phase2/04_apis/02_validated_user_array.json")
#
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
# Config & paths: definir BASE_DIR, EXPORT_DIR, semilla NumPy.
BASE_DIR = Path('phase2/05_pandas_numpy')
EXPORT_DIR = BASE_DIR/"exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True) #creamos directorio, junto con los parents si no existen(parents=True) y no da error si no existe(exist_ok =True).

USERS_JSON = Path('phase2/04_apis/02_validated_user_array.json')

np.random.seed(42) #esto fija el algoritmo de aleatorizacion, para que siempre genere los mismos valores cuando ejecutemos el script.

# Carga usuarios: leer JSON, seleccionar columnas base, extraer city y company_name, tipar. (Tu JSON viene de la semana anterior).
users = pd.read_json(USERS_JSON) #panda leerá la ruta como archivo json y la devuelve como un DataFrame
users = users[[
    'id','name','username','email','address','phone','website','company'
]] #users es un objeto de Pandas. en ellos, doble corchete es para seleccionar las columnas que queremos de un DataFram(solo un corchete es para una serie)

users['city'] = users['address'].apply(lambda x: x['city']) 
users['company_name'] = users['company'].apply(lambda x: x['name'])
## .apply() es propio de pandas, sirve parecido a map() de python, pero para aplicar una funcion en las series o DataFrames.
users= users.drop(columns=['address', 'company']) #drop muestra el dataframe sin las columnas indicadas, y asignamos a users el dataframe sin esas columnas

# Generación de transacciones (sintético): fechas en 2024, categorías, importes lognormales + multiplicadores por categoría, introducir ruido (nulos controlados).
N = 5000
users_ids = users['id'].to_numpy() #esto nos entrega un array con los ids que hubiera en el dataframe(df)

start = datetime(2024, 1, 1)
end = datetime(2024, 12, 31)
span_days = (end - start).days + 1
#trx: transacción
trx_user_id = np.random.choice(users_ids, size=N) #np.random.choice() es una funcion de numpy. escoge al azar valores del array, y repite el proceso N veces.
trx_days = np.random.randint(0, span_days, size =N) #np.random.randint() es otra func de np. escoge al azar numeros enteros de entr 0 y spandays(366), N veces.
trx_date = np.array([start + timedelta(days=int(d)) for d in trx_days])#crea un array(de numpy), generando una fecha por cada numero en rango 0-366.
categories = np.array(['alimentos','ocio','suscripciones','transporte','salud','otros']) #creamos un array de np con categorias
categories_trx = np.random.choice(categories, size=N, p =[.35,.2,.15,.15,.1,.05]) #p son las probabilidades de que random.choice escoja ese valor del array.

amount= np.random.lognormal(mean=6, sigma=0.6, size= N) # crea un array de numpy, con valores aleatorios pero siguiendo una distribucion lognormal(muchos alrededor de un valor inicial, unos pocos alejados de ese valor)
cat_multiplier = {
    'alimentos': 1.0,
    'ocio': 1.3,
    'suscripciones': 0.6,
    'transporte': 0.8,
    'salud': 1.5,
    'otros': 0.9,
}

mult = np.vectorize(cat_multiplier.get)(categories_trx) #devuelve un array de multiplicadores. np.vectorize(cat_multiplier.get) es una funcion que devuelve el valor de un indice de diccionario. (categories_trx es el argumento-diccionario sobre el que actuará get.)
amount_trx = np.round(amount*mult, 2)#multiplicamos amount por los multiplicadores segun categoria.

# Limpieza & tipado: fechas → datetime, rellenar nulos de categoría, asegurar amount numérico.
#primero creamos ruido sintético para limpiarlo después.
mask_null = np.random.rand(N) < 0.01 #esta funcion crea un array de tamaño N con valores de 0 a 1. < 0,01 la transforma en valores booleanos. true si es menor de 0,01 y false si es mayor.
categories_trx[mask_null] = None #en numpy (y pandas) esto hace que para cada valor dee categories_trx, si su homologo en mask_null es True, se aplique la transformacion (= None)

