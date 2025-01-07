#La clase base de las clases modelos
#Los modelos o clases modelo son las clases que mapean a las tablas
from orm.config import BaseClass
#Importar de SQAlchemy los tipos de datos que usan las tablas
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
# declarative_base permite definir la clase base para mapear las tablas de la BD
from sqlalchemy.ext.declarative import declarative_base
#Para calcular la hora actual
import datetime

#3.- Obtener la clase base para mapear tablas
BaseClass = declarative_base()

class Usuario(BaseClass):
    __tablename__="usuarios"
    id=Column(Integer,primary_key=True)
    nombre=Column(String(100))
    edad=Column(Integer)
    domicilio=Column(String(100))
    email=Column("email",String(100))
    password=Column(String(100))
    fecha_registro=Column(DateTime(timezone=True),default=datetime.datetime.now)

class Compra(BaseClass):
    __tablename__="compras"
    id=Column(Integer,primary_key=True)
    id_usuario=Column(Integer, ForeignKey(Usuario.id))
    producto=Column(String(100))
    precio=Column(Float)

class Fotos(BaseClass):
    __tablename__="fotos"
    id=Column(Integer,primary_key=True)
    id_usuario=Column(Integer, ForeignKey(Usuario.id))
    titulo=Column(String(100))
    descripcion=Column(String(100))
    ruta=Column(String(100))



