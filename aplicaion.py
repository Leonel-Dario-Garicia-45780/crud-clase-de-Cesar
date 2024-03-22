from flask import Flask
import pymongo

app =Flask(__name__)

#conecion a mongo atlas
conexion= pymongo.MongoClient('mongodb+srv://gun45780:adso145780@cluster0.feqs5gd.mongodb.net/')

#base de datos
basedeDatos=conexion['gestiondeproductos']

#colecciones
productos=basedeDatos['productos']
usuarios=basedeDatos['usuarios']
categorias=basedeDatos['categorias']

""" 
para crear el usuario
@app.route("/")
    def inicio():
    usuario_nombre="gun45780@gmal.com"
    usuario_contraseña="123456"

    try:
        usuario={
            "nombre":usuario_nombre,
            "contraseña":usuario_contraseña
        }
        accion=usuarios.insert_one(usuario)
        if accion.acknowledged:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as error:
        print(f"usuario no ingresado: {error}")
        return False
"""
#importar controlador para que todo funcione (alla como aca)
from controlador.controladoraplicacion import *

#inicia la aplicacion
if __name__=='__main__':
    app.run(port=3000, debug=True)
