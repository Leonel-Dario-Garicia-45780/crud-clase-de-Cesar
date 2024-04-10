import urllib.request
from aplicaion import app, productos, usuarios, categorias
from flask import render_template,request,redirect , session,jsonify
import pymongo #para manipular la base de datos mongodb(en este caso es atlas)
from bson import ObjectId # bson es de pymongo i traemos el objetid para manipular ids
import urllib

app.secret_key = 'your_secret_key'

# clases
""" class Producto(db.Document):
    codigo = db.StringField(required=True, max_lenth=50)
    nombre = db.StringField(required=True, max_length=100)
    precio = db.decimalfield(required=True)
    categoria = db.StringField(required=True, max_length=100)

class Usuario(db.Document):
    correo = db.EmailField(required=True)
    contraseña = db.StringField(required=True, max_lenth=50)

class Categoria(db.Document):
    nombre=db.StringField(required=True, max_lenth=100) """






# Función y ruta de inicio de sesión
@app.route("/", methods=["GET", "POST"])
def inicio_sesion():
    
    recaptcha_response = request.form['g-recaptcha-response']
    url='https://www.google.com/recaptcha/api/siteverify'
    values={
        "secret":'6LeKI7cpAAAAAERUp3iZ74F_2A45RfY-fjzsnnWL', # la clave sereta
        "response": recaptcha_response
    }
    data=urllib.parse.urlencode(values).endcode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    
    
    if request.method == "POST":
        correo = request.json.get("correo")
        contraseña = request.json.get("contraseña")

        # Verificar si el correo y la contraseña son válidos
        user = usuarios.find_one({"nombre": correo, "contraseña": contraseña})
        if user:
            # Si las credenciales son correctas, iniciar sesión y redirigir a la tabla de productos
            session["correo"] = correo
            return jsonify({"redireccionar": "/tabla_productos"})
        else:
            return jsonify({"error": "Correo o contraseña incorrectos"})

    return render_template("1 inisiodesecion.html")

# Ruta de categorías
@app.route("/categorias", methods=["GET", "POST"])
def categorias_añadir():
    mensaje = None
    if request.method == "POST":
        try:
            categoria_nombre = request.form.get("categoria")
            if categoria_nombre:
                categoria = {"nombre": categoria_nombre}
                accion = categorias.insert_one(categoria)
                if accion.acknowledged:
                    mensaje = "Categoría añadida"
                else:
                    mensaje = "Error al añadir la categoría"
            else:
                mensaje = "Debe ingresar el nombre de la categoría"
        except pymongo.errors.PyMongoError as error:
            mensaje = f"Error de MongoDB: {error}"
    elif request.method == "GET":
        mensaje = "Página de categorías (GET)"
    return render_template("2 categoria.html", mensaje=mensaje)

# Ruta para agregar productos
@app.route("/producto_añadido", methods=["POST", "GET"])
def producto_añadido():
    mensaje = None
    list_categorias = categorias.find()
    try:
        if request.method == "POST":
            producto_codigo = request.form["codigo"]
            producto_nombre = request.form["nombre"]
            producto_precio = request.form["precio"]
            id_categoria = request.form["categoria"]

            producto = {
                "codigo": int(producto_codigo),
                "nombre": producto_nombre,
                "precio": int(producto_precio),
                "categoria": id_categoria
            }
            accion_añadir = productos.insert_one(producto)
            if accion_añadir.acknowledged:
                mensaje = "Producto agregado correctamente"
            else:
                mensaje = "Error al agregar el producto"

    except pymongo.errors.PyMongoError as error:
        print(f"{error}")

    return render_template("3 producto_añadido.html", mensaje=mensaje, categorias=list_categorias)

# Ruta para mostrar productos en una tabla
@app.route("/tabla_productos", methods=["GET", "POST"])
def tabla_productos():
    try:
        lis_productos = productos.find()
        li_producto = []

        for p in lis_productos:
            categoria_id = p.get('categoria')
            if categoria_id and ObjectId.is_valid(categoria_id):
                categoria = categorias.find_one({'_id': ObjectId(categoria_id)})
                if categoria:
                    p['categoria'] = categoria['nombre']
            li_producto.append(p)

    except pymongo.errors.PyMongoError as error:
        print(f"{error}")

    return render_template("4 tablaproductos.html", productos=li_producto)

# Ruta para editar un producto
@app.route("/editar/<producto_id>", methods=["GET", "POST"])
def editar(producto_id):
    mensaje = None
    list_categorias = categorias.find()
    producto_editado = {}
    producto = productos.find_one({"_id": ObjectId(producto_id)})
    try:
        if request.method == "POST":
            nuevo_nombre = request.form["nombre_edit"]
            nuevo_precio = int(request.form["precio_edit"])
            nueva_categoria = request.form["categoria_edit"]

            buscar = {"_id": ObjectId(producto_id)}
            producto_editado = {
                "$set": {
                    "nombre": nuevo_nombre,
                    "precio": nuevo_precio,
                    "categoria": nueva_categoria
                }
            }
            editar_p = productos.update_one(buscar, producto_editado)

            if editar_p.acknowledged:
                mensaje = "Producto editado correctamente"
                return redirect("/tabla_productos")
            else:
                mensaje = "Error al editar el producto"

    except pymongo.errors.PyMongoError as error:
        print(f"Error al actualizar el producto: {error}")
        mensaje = "Error al actualizar el producto"

    return render_template("5 editar.html", mensaje=mensaje, categorias=list_categorias, producto=producto)

# Ruta para eliminar un producto
@app.route("/eliminar/<producto_id>", methods=["GET", "POST"])
def eliminar(producto_id):
    mensaje = None
    if request.method == "POST":
        if request.form.get("confirmar"):
            try:
                resultado = productos.delete_one({"_id": ObjectId(producto_id)})
                if resultado.deleted_count == 1:
                    mensaje = "Producto eliminado correctamente"
                else:
                    mensaje = "No se encontró el producto para eliminar"
            except pymongo.errors.PyMongoError as error:
                print(f"Error al eliminar el producto: {error}")
                mensaje = "Error al eliminar el producto"
            return redirect("/tabla_productos")
        else:
            return redirect("/tabla_productos")
    else:
        return render_template("6 preguntar eliminar.html", producto_id=producto_id)
