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
trx_category = np.random.choice(categories, size=N, p =[.35,.2,.15,.15,.1,.05]) #p son las probabilidades de que random.choice escoja ese valor del array.

amount= np.random.lognormal(mean=2.5, sigma=0.6, size= N) # crea un array de numpy, con valores aleatorios pero siguiendo una distribucion lognormal(muchos alrededor de un valor inicial, unos pocos alejados de ese valor)
cat_multiplier = {
    'alimentos': 1.0,
    'ocio': 1.3,
    'suscripciones': 0.6,
    'transporte': 0.8,
    'salud': 1.5,
    'otros': 0.9,
}

mult = np.vectorize(cat_multiplier.get)(trx_category) #devuelve un array de multiplicadores. np.vectorize(cat_multiplier.get) es una funcion que devuelve el valor de un indice de diccionario. (categories_trx es el argumento-diccionario sobre el que actuará get.)
amount_trx = np.round(amount*mult, 2)#multiplicamos amount por los multiplicadores segun categoria.

# Limpieza & tipado: fechas → datetime, rellenar nulos de categoría, asegurar amount numérico.
#primero creamos ruido sintético para limpiarlo después.
mask_null = np.random.rand(N) < 0.01 #esta funcion crea un array de tamaño N con valores de 0 a 1. < 0,01 la transforma en valores booleanos. true si es menor de 0,01 y false si es mayor.
trx_category[mask_null] = None #en numpy (y pandas) esto hace que para cada valor de categories_trx, si su homologo en mask_null es True, se aplique la transformacion (= None)

transactions = pd.DataFrame({
    'trx_id': np.arange(1, N+1), #crea una lista de rango entre 1 y N(incluido por el +1)
    'user_id': trx_user_id, 
    'date': trx_date, 
    'category': trx_category, 
    'amount': amount_trx
})
# Limpieza & tipado: fechas → datetime, rellenar nulos de categoría, asegurar amount numérico.
transactions['date'] = pd.to_datetime(transactions['date'],errors = 'coerce') #convierte las fechas en un formato de fechas entendible para pandas y normaliza. si no es una fecha, coerce lo transforma en un Not a Time(NaT).
transactions['category'] = transactions['category'].fillna('sin categoría')
transactions['amount'] = pd.to_numeric(transactions['amount'], errors='coerce') #lo mismo que to_datetime, pero para numeros.

# Selección/filtrado: máscara por fecha/importe; query; loc/iloc. (Cuenta como 3 técnicas).
from_date = pd.Timestamp('01-06-2025') #como pd.to_datetime, pero para un unico valor. tambien serviria pd.to_datetime
mask = (transactions['date'] >= from_date) & (transactions['amount'] > 5) #mask es un filtrado de transactions que filtra todas las fechas anteriores a la que hemos elegido y todos los valores inferiores al que hemos elegido. genera un array booleano.
subset = transactions.loc[mask, ['trx_id','user_id', 'date','category', 'amount' ]] #.loc permite llamar al dataframe filtrando filas(las que sean True en mask) y columnas(las que hemos seleccionado)

subset_q = transactions.query("date >= @from_date and amount > 5") #query es otra forma de hacer lo mismo pero mas simplificado. el @ le comunica a pandas que from_date no es una columna sino algo externo al dataframe.

sample_loc = transactions.loc[transactions.index[:5], ['trx_id','user_id','amount']] #creamos un subset con loc, que de solo filas hasta el index numero 4(5-1) y solo las columnas id y amount.
sample_iloc = transactions.iloc[:5, :3] #iloc para filtrar con indices en vez de valores. aqui seleccionamos las filas hasta el 4 y las columnas hasta el 2 en el df transactions.

# Agregaciones: groupby(...).agg(sum, mean, size), top de categorías, resample mensual + rolling(3).
ordered_by = transactions.groupby(['user_id', 'category'], as_index=False) #ordena el dataframe por usuarios y categorias. as index = false para que esas columnas no se transformen en indices, y crea un objeto groupby sobre el que operar luego.
agg_user_cat = (ordered_by.agg( #.agg opera sobre el objeto groupby. primero se escribe la columna sobre opear y luego el tipo de operacion (sum, mean, size etc)
    total=('amount','sum'),
    media = ('amount', 'mean'), 
    n = ('amount', 'size')
))
#top de categorias
top_categories = transactions.groupby(['category'], as_index=False).agg(total=('amount', 'sum')).sort_values('total',ascending=False).reset_index()
# Tabla pivote mensual por categoría (totales de cada mes)
transactions['year_month'] = transactions['date'].dt.to_period('M') #creamos una nueva columna en el dataframe, que para una fecha en date crea un mes/año en la nueva columna.
monthly_totals = pd.pivot_table( #pivot table permite visualizar columnas y operar sobre ellas. elegimos el df transactions. los valores sobre los que operar(trx_amount) la columna que queremos que se vea (categories), el indice (month_year) y el tipo de operacion ()'sum')
    transactions, 
    values= 'amount', 
    index = 'year_month', 
    columns = 'category',
    aggfunc= 'sum',
    fill_value=0.0).astype(float)

monthly_totals_resample = transactions.set_index('date')['amount'].resample('ME').sum() #set_index para cambiar el indice del DT a 'date', para poder trabajar con resample. resample('M') agrupa fechas dentro de cada mes, si el DT tiene un indice de fechas. sum() le dice que sume los importes para cada agrupacion de fechas
rolling_3m = monthly_totals_resample.rolling(3).mean() #rolling(3) va agrupando de 3 en 3. mean calcula la media para cada agrupacion.

# Joins: unir transactions con users para métricas por ciudad/compañía.
trx_users = transactions.merge(users[['id','city','company_name']], left_on='user_id', right_on='id', how='left') #hacemos una union de los dos dataframes. seleccionamos qué queremos hacer coincidir (user_id de transactions que corresponda con id de users. how: left indica un left join (siempre se ve la fila de transactions, aunque el otro dataframe no tenga equivalente)
trx_users = trx_users.drop(columns=['id']) #una vez hecho el merge, tenemos dos columnas id iguales, por lo que una ya no es necesaria.

#gasto por ciudad
spending_per_city= trx_users.groupby(['city'], as_index=False).agg(total=('amount', 'sum')).sort_values('total', ascending=False).reset_index()
spend_city = trx_users.groupby('city')['amount'].sum().sort_values(ascending=False).reset_index()

# Transformaciones NumPy: descuentos/recargos con np.where, ufunc (p. ej. np.log1p) en una nueva columna.
# Aplica un descuento del 5% a 'suscripciones' y un recargo del 10% a 'ocio',
# usando máscaras booleanas vectorizadas.
mask_sub = trx_users['category'] == 'suscripciones'
trx_users.loc[mask_sub,'amount'] = trx_users.loc[mask_sub,'amount'].apply(lambda x: np.round(x*0.95, 2)) #.loc permite modificar el dataframe al que se le aplica.

mask_is_ocio = (trx_users['category'].to_numpy() == 'ocio')
amount_np = trx_users['amount'].to_numpy(dtype=float)
amount_np = np.where(mask_is_ocio, amount_np*1.10, amount_np) #where(condicion, valor si se cumple la condicion, valor si no se cumple)
trx_users['amount'] = np.round(amount_np, 2)

# Exportación CSV: al menos: transactions_*.csv, agg_user_cat_*.csv, top_categories_*.csv, pivot_month_cat_*.csv, spend_city_*.csv.
now_tag = datetime.now().strftime('%Y%m%d_%H%M%S')

trx_users.to_csv(EXPORT_DIR/f"transactions_{now_tag}.csv", index=False)
agg_user_cat.to_csv(EXPORT_DIR/f"agg_user_cat_{now_tag}.csv", index=False)
top_categories.to_csv(EXPORT_DIR/f"top_categories_{now_tag}.csv", index=False)
monthly_totals.to_csv(EXPORT_DIR/f"pivot_month_cat_{now_tag}.csv")
spend_city.to_csv(EXPORT_DIR/f"spend_city_{now_tag}.csv", index=False)

print("\n=== RESUMEN DE GEMAS ===")
print(f"Transacciones: {len(transactions):,}")
print("Top 5 categorías por gasto total:\n", top_categories.head(5))
print("Top 5 ciudades por gasto:\n", spend_city.head(5))
print("CSV exportados en:", EXPORT_DIR.resolve())
print(trx_users)
