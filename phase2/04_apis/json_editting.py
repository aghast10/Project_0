import requests
import json
import os
import re
import sqlite3
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, HttpUrl, ValidationError, Field
from decimal import Decimal


if os.path.exists('phase2/apis/02_user_array.json'):
    with open('phase2/apis/02_user_array.json',"r", encoding="utf-8") as f:
            user_array = json.load(f)
else:
    url = "https://jsonplaceholder.typicode.com/users"  # endpoint seguro para pruebas
    r = requests.get(url)
    user_array = []
    user_array.append(r.json())
    user_array = user_array[0]
    with open("phase2/apis/02_user_array.json", "w", encoding="utf-8") as f:
        json.dump(user_array, f, indent=4, ensure_ascii=False)

user_array_names = [i['name'] for i in user_array]


def to_snake_case(s: str) -> str:
    """Convierte camelCase/PascalCase a snake_case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

def snake_case_any(obj):
    if isinstance(obj, list):
        new_list = []
        for i in obj:
            new_list.append(snake_case_any(i))
        return new_list

    elif isinstance(obj,dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = to_snake_case(k)
            new_dict[new_key] = snake_case_any(v)
        return new_dict

    else:
        return obj     
    
new_user_array = snake_case_any(user_array)


class Geo(BaseModel):
    lat: Decimal
    lng: Decimal

class Company(BaseModel):
    name: str
    catch_phrase: str
    bs: str

class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str = Field(pattern=r"\d{5}-\d{4}")
    @field_validator("zipcode", mode="before")
    @classmethod
    def normalize_zipcode(cls, v: str):#formateamos si es posible
        v = str(v)
        if re.fullmatch(r"\d+", v):
            v = v[0:5]+"-"+v[5::]
        if v.endswith('-'):
            v = v+"0000" 
        return v
    geo: Geo

class User(BaseModel):
    id:int
    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    @field_validator("phone", mode="before")
    @classmethod
    def normalize_phone(cls, v: str):
        v = str(v)
        v = re.sub(r"([A-Za-z]).*", "", v)
        v = re.sub(r"([)(])","", v)
        v = v.replace('.', '-')
        return v
    website: HttpUrl
    @field_validator("website", mode="before")
    @classmethod
    def normalize_website(cls, v:str) ->str:
        if isinstance(v, str) and not v.startswith(("https://","http://")):
            v =''.join(['https://', v])
            return v
        return v

    company: Company

validated_user_array_json = []
errors = []
for i in new_user_array:
    try:
        validated_user_array_json.append(User(**i).model_dump(mode="json")) #mode="json" sirve para que pydantic entienda que lo vamos a exportar a json
    except ValidationError as e:
        print(f"Validation error (user id: {i['id']}): {e}. user excluded.")
        errors.append(e) #guardamos los errores en una lista de errores

#guardamos a un archivo json
with open("phase2/apis/02_validated_user_array.json", "w", encoding="utf-8") as f:
            json.dump(validated_user_array_json, f, indent=4) #type: ignore
print(f"processed_at: {datetime.now()}")

##Guardamos los users en una base de datos de sqlite
with sqlite3.connect("phase2/sql/mina_de_datos.db") as conn:
    cur = conn.cursor()
    cur.execute ("PRAGMA foreign_keys = ON;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users_json (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data JSON
        );
    """)
    cur.executemany(
    "INSERT INTO users_json (data) VALUES (?);",
    [(json.dumps(user),) for user in validated_user_array_json]
) #guardamos como tupla para que cada user con sus campos cuente como un solo elemento
