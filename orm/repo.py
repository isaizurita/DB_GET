import orm.modelos as modelos
import orm.esquemas as esquemas
from sqlalchemy.orm import Session
from sqlalchemy import and_

#Esta función es llamada por api.py
#Para atender GET '/usuarios/{id}'
#select * from usuarios where id = id_usuario

def usuario_por_id(sesion: Session, id_usuario: int):
    print("select * from app.usuarios where id= ", id_usuario)
    return sesion.query(modelos.Usuario).filter(modelos.Usuario.id==id_usuario).first()

def compra_por_id(sesion: Session, id_compra: int):
    print("select * from app.compras where id= ", id_compra)
    return sesion.query(modelos.Compra).filter(modelos.Compra.id==id_compra).first()

def foto_por_id(sesion: Session, id_foto: int):
    print("select * from app.fotos where id= ", id_foto)
    return sesion.query(modelos.Fotos).filter(modelos.Fotos.id==id_foto).first()

def lista_usuarios_db(sesion: Session):
    print("select * from app.usuarios")
    return sesion.query(modelos.Usuario).all()

def lista_usuarios_edad(sesion:Session, edad_min: int, edad_max: int):
    print("select * from app.usuarios where edad >= edad_min and edad <= edad_max")
    return sesion.query(modelos.Usuario).filter(and_(modelos.Usuario.edad>=edad_min, modelos.Usuario.edad<=edad_max)).all()

# GET '/compras?id_usuario={id_usr}&precio={p}'
# select * from app.compras where id_usuario=id_usr and precio>=p
def devuelve_compras_por_usuario_precio(sesion:Session, id_usr:int, p:float):
    print("select * from app.compras where id_usuario=id_usr and precio>=p")
    return sesion.query(modelos.Compra).filter(and_(modelos.Compra.id_usuario==id_usr, modelos.Compra.precio>=p)).all()

#Buscar foto por id de usuario
#GET '/usuarios/{id}/fotos'
#select * from app.fotos where id_usuario=id
def fotos_por_id_usuario(sesion: Session, id_usuario):
    print("select * from app.fotos where id_usuario=", id_usuario)
    return sesion.query(modelos.Fotos).filter(modelos.Fotos.id_usuario==id_usuario).all()

#Borra fotos por id de usuario
#DELETE '/usuarios/{id}/fotos'
#delete from app.fotos where id_usuario=id
def borrar_fotos_por_id_usuario(sesion: Session, id_usuario: int):
    print("delete from app.fotos where id_usuario=", id_usuario)
    fotos_usr=fotos_por_id_usuario(sesion, id_usuario)
    if fotos_usr is not None:
        for foto_usuario in fotos_usr:
            sesion.delete(foto_usuario)
        sesion.commit()

#Borra compras por id de usuario
#DELETE '/usuarios/{id}/compras'
#delete from app.compras where id_usuario=id
def borrar_compras_por_id_usuario(sesion: Session, id_usuario: int):
    print("delete from app.compras where id_usuario=", id_usuario)
    compras_usr=compras_por_id_usuario(sesion, id_usuario)
    if compras_usr is not None:
        for compra_usuario in compras_usr:
            sesion.delete(compra_usuario)
        sesion.commit()

#Buscar compra por id de usuario
#GET '/usuarios/{id}/compras
#select * from app.compras where id_usuario=id
def compras_por_id_usuario(sesion: Session, id_usuario):
    print("select * from app.compras where id_usuario=", id_usuario)
    return sesion.query(modelos.Compra).filter(modelos.Compra.id_usuario==id_usuario).all()

#DELETE '/usuarios/{id}'
#Delete from app.usuarios where id=id_usuario
def borra_usuario_por_id(sesion: Session, id_usuario: int):
    print("delete from app.usuarios where id=", id_usuario)
    #1.- Select para ver si existe el usuario a borrar
    usr=usuario_por_id(sesion, id_usuario)
    #2.- Borramos
    if usr is not None:
        #Borramos usuario
        sesion.delete(usr)
        #Confirmar los cambios
        sesion.commit()
    respuesta={
        "mensaje":"usuario eliminado"
    }
    return respuesta

#PUT '/usuarios/{id}
def actualiza_usuario(sesion: Session, id_usuario: int, usr_esquema: esquemas.UsuarioBase):
    #Verificar que el usuario exista
    usr_bd = usuario_por_id(sesion, id_usuario)
    if usr_bd is not None:
        #Si existe modificar la siguiente información
        usr_bd.nombre = usr_esquema.nombre
        usr_bd.edad = usr_esquema.edad
        usr_bd.domicilio = usr_esquema.domicilio
        usr_bd.email = usr_esquema.email
        usr_bd.password = usr_esquema.password
        #Confirmar los cambios
        sesion.commit()
        #Refrescar la base de datos
        sesion.refresh(usr_bd)
        #Imprimir los nuevos datos
        print(usr_esquema)
        return usr_esquema
    else:
        respuesta={"mensaje":"No existe el usuario"}
        return respuesta

#PUT '/fotos/{id}
def actualiza_foto(sesion: Session, id_foto: int, foto_esquema: esquemas.FotoBase):
    #Verificar que la foto exista
    foto_bd = foto_por_id(sesion, id_foto)
    if foto_bd is not None:
        foto_bd.titulo = foto_esquema.titulo
        foto_bd.descripcion = foto_esquema.descripcion
        foto_bd.ruta = foto_esquema.ruta

        sesion.commit()
        sesion.refresh(foto_bd)
        print(foto_esquema)
        return foto_esquema
    else:
        respuesta={"mensaje":"No existe la foto"}
        return respuesta
    
#PUT '/compras/{id}
def actualiza_compra(sesion: Session, id_compra: int, compra_esquema: esquemas.CompraBase):
    compra_bd = compra_por_id(sesion, id_compra)
    if compra_bd is not None:
        compra_bd.producto = compra_esquema.producto
        compra_bd.precio = compra_esquema.precio
        
        sesion.commit()
        sesion.refresh(compra_bd)
        print(compra_esquema)
        return compra_esquema
    else: 
        respuesta={"mensaje":"No existe la compra"}
        return respuesta