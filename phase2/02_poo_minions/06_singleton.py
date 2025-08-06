# 🎯 Objetivo:
#
# Desarrollar una clase ConfigManager que se asegure de que solo exista una instancia global de 
# configuración durante toda la ejecución de un programa. Esta instancia debe poder ser accedida 
# desde cualquier parte del código para leer o modificar configuraciones.
#
# 🛠️ Descripción del escenario:
#
# Imagina que estás desarrollando una aplicación web o de escritorio que necesita conectarse 
# a una base de datos, cargar parámetros desde un archivo .json y establecer configuraciones 
# como el modo debug, idioma, o nivel de logs. 
#
# Estas configuraciones deben ser únicas y coherentes en toda la aplicación.
#
# ✅ Requisitos de la implementación:
#
#   Crear una clase ConfigManager que implemente el patrón Singleton.
#
#    La clase debe:#
#
#        Leer configuraciones desde un archivo .json.
#
#        Proporcionar métodos para obtener y actualizar configuraciones.
#
#    Garantizar que cualquier módulo o script que importe y use ConfigManager trabaje con la misma instancia.
#

import json

class ConfigManager:
    _instance = None
    def __new__(cls, config_file = "config_singleton.json"): #los singleton usan __new__(cls), que antecede a __init__
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
            cls._instance._load_config(config_file)
        return cls._instance
    
    def _load_config(self, config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            self._config = json.load(f)
            
    def get (self, key):
        return self._config.get(key)
    
    def set (self, key, value):
        self._config[key] = value

cnfg1 = ConfigManager()
print(cnfg1.get("language"))
cnfg1.set("language", "en")
print(cnfg1.get("language"))

cnfg2 = ConfigManager()
print(cnfg2 == cnfg1)
print (cnfg2.get("language"))