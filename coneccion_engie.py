from flask import Flask
""" from flask_mongoengine import MongoEngine """#esta linea la comento proque se repite en modelos
from modelos import db, Producto, Usuario, Categoria

app = Flask(__name__)
app.secret_key = "123456lomasseguroqueexiste"
app.config["UPLOAD_FOLDER"] = "./static/imagenes"
app.config["MONGODB_SETTINGS"] = {
    # esta coneccion le pedi ayuda a gpt
    "host": "mongodb+srv://gun45780:adso145780@cluster0.feqs5gd.mongodb.net/gestiondeproductos",
}

db.init_app(app)

if __name__ == "__main__":
    app.run(port=3000, debug=True)
