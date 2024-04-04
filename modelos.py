from flask_mongoengine import MongoEngine

db=MongoEngine()

class Producto(db.Document):
    codigo = db.StringField(required=True, max_lenth=50)
    nombre = db.StringField(required=True, max_length=100)
    precio = db.decimalfield(required=True)
    categoria = db.StringField(required=True, max_length=100)

class Usuario(db.Document):
    correo = db.EmailField(required=True)
    contraseña = db.StringField(required=True, max_lenth=50)

class Categoria(db.Document):
    nombre=db.StringField(required=True, max_lenth=100)
