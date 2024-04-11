from flask import Flask
from flask_mongoengine import MongoEngine 

app = Flask(__name__)

# Configuración de MongoEngine
app.config['MONGODB_SETTINGS'] = {
    'db': 'gestiondeproductos',
    'host': 'mongodb+srv://gun45780:adso145780@cluster0.feqs5gd.mongodb.net/'
}

db = MongoEngine()
db.init_app(app)

# Importar controlador para que todo funcione
from controlador.controladoraplicacion import *

# Inicia la aplicación
if __name__ == '__main__':
    app.run(port=3000, debug=True)
