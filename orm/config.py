#El engine permite confirgurar la conexión a la BD
from sqlalchemy import create_engine
#El session maker permite crear sesiones para hacer consultas
#Por cada consulta se abre y cierra una sesión
from sqlalchemy.orm import sessionmaker
#Importar el archivo de modelos
from orm import modelos
import os
#1. Configurar la conexion BD
# Crear la URL de la BD -> servidorBD://usuario:password@url:puerto/nombreBD
'''URL_BASE_DATOS = "postgresql://isaizurita:704250@localhost:5432/prueba_api"
# Conectarnos mediante el esquema app
engine = create_engine(URL_BASE_DATOS,
                       connect_args={
                           "options": "-csearch_path=app"                           
                       })
'''
#Conecta a la base de datos
engine = create_engine(os.getenv("db_uri","sqlite://base-ejemplo.db"))
modelos.BaseClass.metadata.create_all(engine)

#2. Obtener la clase que nos permite crear objetos tipo session
SessionClass = sessionmaker(engine) 
# Crear una función para obtener objetos de la clase SessionClass
def generador_sesion():
    sesion = SessionClass()
    try:
        #equivalente a return sesion pero de manera segura
        yield sesion 
    finally:
        sesion.close()

