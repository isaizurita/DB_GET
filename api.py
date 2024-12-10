from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import shutil
import os
import uuid
import orm.repo as repo #Funciones para hacer consultas a la DB
from sqlalchemy.orm import Session
from orm.config import generador_sesion #Generador de sesiones
import orm.esquemas as esquemas

# creación del servidor
app = FastAPI()
    
usuarios = [{
    "id": 0,
    "nombre": "Homero Simpson",
    "edad": 40,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 1,
    "nombre": "Marge Simpson",
    "edad": 38,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 2,
    "nombre": "Lisa Simpson",
    "edad": 8,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 3,
    "nombre": "Bart Simpson",
    "edad": 10,
    "domicilio": "Av. Simpre Viva"
}]


# decorator
@app.get("/")
def hola_mundo():
    print("invocando a ruta /")
    respuesta = {
        "mensaje": "hola mundo!"
    }

    return respuesta


@app.get("/usuarios/{id}/compras/{id_compra}")
def compras_usuario_por_id(id: int, id_compra: int):
    print("buscando compra con id:", id_compra, " del usuario con id:", id)
    # simulamos la consulta
    compra = {
        "id_compra": 787,
        "producto": "TV",
        "precio": 14000
    }

    return compra

@app.get("/usuarios/{id}")
def usuario_por_id(id: int, sesion: Session=Depends(generador_sesion)):
    print("Api consultando usuario por ID")
    return repo.usuario_por_id(sesion, id)

@app.get("/usuarios/{id}/fotos")
def fotos_por_id_usr(id: int, sesion: Session=Depends(generador_sesion)):
    print("API consultando fotos del usuario ", id)
    return repo.fotos_por_id_usuario(sesion, id)

@app.get("/usuarios/{id}/compras")
def compras_por_id_usr(id: int, sesion: Session=Depends(generador_sesion)):
    print("API consultando compras por usuario ", id)
    return repo.compras_por_id_usuario(sesion,id)

# "/compras?edad_min={edad_min}&edad_max={edad_max}"
@app.get("/usuarios")
def lista_usuarios_db(edad_min: int, edad_max: int, sesion: Session=Depends(generador_sesion)):
    print("Api consultando todos los usuarios")
    return repo.lista_usuarios_edad(sesion, edad_min, edad_max)


@app.get("/compras/{id}")
def compra_por_id(id: int, sesion: Session=Depends(generador_sesion)):
    print("Api consultando compra por ID")
    return repo.compra_por_id(sesion, id)

# "/compras?id_usuario={id_usr}&precio={p}"
@app.get("/compras")
def lista_compras(id_usuario:int,precio:float,sesion:Session=Depends(generador_sesion)):
    print("/compras?id_usuario={id_usr}&precio={p}")
    return repo.devuelve_compras_por_usuario_precio(sesion,id_usuario,precio)

@app.get("/fotos/{id}")
def foto_por_id(id: int, sesion: Session=Depends(generador_sesion)):
    print("Api consultando foto por ID")
    return repo.foto_por_id(sesion, id)

'''
@app.get("/usuarios")
def lista_usuarios(*,lote:int=10,pag:int,orden:Optional[str]=None): #parametros de consulta ?lote=10&pag=1
    print("lote:",lote, " pag:", pag, " orden:", orden)
    #simulamos la consulta
    return usuarios
'''

@app.put("/usuario/{id}")
def actualizar_usuario(id:int,info_usuario: esquemas.UsuarioBase, sesion: Session=Depends(generador_sesion)):
    repo.actualiza_usuario(sesion, id, info_usuario)

@app.put("/fotos/{id}")
def actualizar_foto(id:int, info_foto: esquemas.FotoBase, sesion: Session=Depends(generador_sesion)):
    repo.actualiza_foto(sesion, id, info_foto)

@app.put("/compras/{id}")
def actualizar_compra(id:int, info_compra: esquemas.CompraBase, sesion: Session=Depends(generador_sesion)):
    repo.actualiza_compra(sesion, id, info_compra)
    
@app.delete("/usuario/{id}")
def borrar_usuario(id:int, sesion: Session=Depends(generador_sesion)):
    repo.borrar_compras_por_id_usuario(sesion,id)
    repo.borrar_fotos_por_id_usuario(sesion, id)
    repo.borra_usuario_por_id(sesion,id)
    return {"status_borrado", "ok"}

@app.post("/fotos")
async def guardar_foto(titulo:str=Form(None), descripcion:str=Form(...), foto:UploadFile=File(...)):
    print("titulo:", titulo)
    print("descripcion:", descripcion)

    home_usuario=os.path.expanduser("~")
    nombre_archivo=uuid.uuid4().hex  #generamos nombre único en formato hexadecimal
    extension = os.path.splitext(foto.filename)[1]
    ruta_imagen=f'{home_usuario}/fotos-ejemplo/{nombre_archivo}{extension}'
    print("guardando imagen en ruta:", ruta_imagen)

    with open(ruta_imagen,"wb") as imagen:
        contenido = await foto.read() #read funciona de manera asyncrona
        imagen.write(contenido)

    return {"titulo":titulo, "descripcion":descripcion, "foto":foto.filename}

@app.post("/usuarios")
def guardar_usuario(usuario: esquemas.UsuarioBase, sesion: Session=Depends(generador_sesion)):
    print(usuario)
    #Guardado en la base
    return repo.guardar_usuario(sesion, usuario)

@app.post("/usuarios/{id}/compras")
def guardar_compra(id: int, compra: esquemas.CompraBase, sesion: Session=Depends(generador_sesion)):
    return repo.guardar_compra(sesion, id, compra)

@app.post("/usuarios/{id}/fotos")
def guardar_foto(id: int, foto: esquemas.FotoBase, sesion: Session=Depends(generador_sesion)):
    return repo.guardar_foto(sesion, id, foto)