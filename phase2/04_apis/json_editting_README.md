🧩 Martes — “Descifrar la profecía (JSON) — Edición JSONPlaceholder”

Fuente: https://jsonplaceholder.typicode.com/users
Objetivo: Practicar .json(), dict/list comprehensions y validación con Pydantic sobre un JSON anidado real.

🗺️ Misiones

Extraer el JSON:

Haz GET /users y obtén una lista de usuarios.

Trabaja en memoria (no guardes archivo).

Normalizar y transformar:

Convierte claves a snake_case.

Address y company vienen anidados: decide si aplanas (p. ej. address_city) o modelas submodelos.

Limpia campos:

email → formato válido.

phone → quita extensiones/ruido (solo dígitos, +, espacios y guiones).

website → si no tiene esquema, antepón http://.

address.zipcode → valida patrón (ej. NNNNN-XXXX) y normaliza a uppercase.

address.geo.lat/lng → convierte a Decimal.

Timestamp de proceso:

Añade processed_at: datetime con datetime.utcnow() (la API no trae fechas; este campo demuestra conversión a datetime).

Validar con Pydantic:

Crea modelos User, Address, Geo, Company.

Usa tipos y validadores:

EmailStr para email.

constr/Field para longitudes y regex.

HttpUrl | AnyUrl | str (si normalizas website antes, HttpUrl sirve).

Decimal para geo.

Incluye validadores (@field_validator / @model_validator) para limpieza extra.

Comprensiones:

Usa list comprehensions para mapear la lista cruda → lista validada.

(Opcional) dict comprehension para indexar por company.name o por dominio del email.

📦 Entregable

02_parsear_profecia.py que:

Hace la petición, response.json().

Normaliza y transforma (snake_case, limpieza, processed_at).

Valida con Pydantic.

Imprime los datos validados (por usuario), o un resumen de errores indicando índice y campo.

✅ Criterios de aceptación

El script corre sin argumentos y procesa los 10 usuarios.

Al menos 1 submodelo Pydantic (p. ej., Address).

email inválido o website sin esquema → el validador lo corrige o lanza error claro.

geo.lat/lng son Decimal, no str.

Se imprime una lista de instancias Pydantic (o .model_dump()), legible.

Si falla la validación de un usuario, el script no crashea: muestra el error y continúa con los demás.

🧪 Pruebas sugeridas

Forzar un website vacío en un elemento (simulado) y ver el error.

Cambiar email a foo@bar para ver validación.

Modificar zipcode a un formato raro y comprobar normalización/regex.

🌟 Extra (opcionales)

Añade CLI con argparse para --pretty (imprime JSON bonito) y --index-by company.

Exporta los validados a validated_users.json.

Métricas rápidas: cuántos dominios de email únicos.

¿Quieres que te deje un esqueleto inicial del script con los modelos y los puntos de extensión marcados?