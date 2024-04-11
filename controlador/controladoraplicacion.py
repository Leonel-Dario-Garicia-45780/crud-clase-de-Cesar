import urllib.request
from flask import render_template, request, redirect, session, jsonify
from flask import JSONEncoder
import json
import urllib
from aplicaion import app, db

app.secret_key = 'your_secret_key'

# Definición de modelos con MongoEngine
class Producto(db.Document):
    codigo = db.IntField(required=True)
    nombre = db.StringField(required=True, max_length=100)
    precio = db.FloatField(required=True)
    categoria = db.ReferenceField('Categoria')

class Usuario(db.Document):
    correo = db.EmailField(required=True)
    contraseña = db.StringField(required=True)

class Categoria(db.Document):
    nombre = db.StringField(required=True, max_length=100)


# Rutas y controladores como antes, con ajustes para usar MongoEngine

# Función y ruta de inicio de sesión con verificación de reCAPTCHA
@app.route("/", methods=["GET", "POST"])
def inicio_sesion():
    if request.method == "POST":
        recaptcha_response = request.form['g-recaptcha-response']
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            "secret": '6LeKI7cpAAAAAERUp3iZ74F_2A45RfY-fjzsnnWL',
            "response": recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        
        if result['success']:
            correo = request.form["correo"]
            contraseña = request.form["contraseña"]
            user = Usuario.objects(correo=correo, contraseña=contraseña).first()
            if user:
                session["correo"] = correo
                return redirect("/tabla_productos")
            else:
                return jsonify({"error": "Correo o contraseña incorrectos"})
    return render_template("1_inisiodesecion.html")

# Ruta para agregar categorías
@app.route("/categorias", methods=["GET", "POST"])
def categorias_añadir():
    if request.method == "POST":
        categoria_nombre = request.form.get("categoria")
        if categoria_nombre:
            categoria = Categoria(nombre=categoria_nombre)
            categoria.save()
            return redirect("/categorias")
        else:
            return jsonify({"error": "Debe ingresar el nombre de la categoría"})
    categorias = Categoria.objects()
    return render_template("2_categoria.html", categorias=categorias)

# Ruta para agregar productos
@app.route("/producto_añadido", methods=["POST", "GET"])
def producto_añadido():
    categorias = Categoria.objects()
    if request.method == "POST":
        producto_codigo = request.form["codigo"]
        producto_nombre = request.form["nombre"]
        producto_precio = request.form["precio"]
        id_categoria = request.form["categoria"]
        categoria = Categoria.objects(id=id_categoria).first()

        producto = Producto(
            codigo=int(producto_codigo),
            nombre=producto_nombre,
            precio=float(producto_precio),
            categoria=categoria
        )
        producto.save()
        return redirect("/tabla_productos")
    return render_template("3_producto_añadido.html", categorias=categorias)

# Ruta para mostrar productos en una tabla
@app.route("/tabla_productos", methods=["GET", "POST"])
def tabla_productos():
    productos = Producto.objects().all()
    return render_template("4_tablaproductos.html", productos=productos)

# Ruta para editar un producto
@app.route("/editar/<producto_id>", methods=["GET", "POST"])
def editar(producto_id):
    producto = Producto.objects(id=producto_id).first()
    categorias = Categoria.objects()
    if request.method == "POST":
        producto.update(
            nombre=request.form["nombre_edit"],
            precio=float(request.form["precio_edit"]),
            categoria=Categoria.objects(id=request.form["categoria_edit"]).first()
        )
        return redirect("/tabla_productos")
    return render_template("5_editar.html", producto=producto, categorias=categorias)

# Ruta para eliminar un producto
@app.route("/eliminar/<producto_id>", methods=["GET", "POST"])
def eliminar(producto_id):
    producto = Producto.objects(id=producto_id).first()
    if request.method == "POST":
        if request.form.get("confirmar"):
            producto.delete()
            return redirect("/tabla_productos")
    return render_template("6_preguntar_eliminar.html", producto=producto)



# Implementación ajustada para las operaciones CRUD, manipulación de sesiones, etc.




