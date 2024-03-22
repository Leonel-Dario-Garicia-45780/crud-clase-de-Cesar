from aplicaion import app, productos, usuarios, categorias
from flask import render_template,request,redirect
import yagmail #para el login. su funcion es mandar un correo
import pymongo #para manipular la base de datos mongodb(en este caso es atlas)
from bson import ObjectId # bson es de pymongo i traemos el objetid para manipular ids

#funcion y ruta de logoin
@app.route("/")
def inicio():
    return render_template("1 inisiodesecion.html")

#funcion y ruta de categorias
@app.route("/categorias", methods=["GET","POST"])
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
        # Aquí puedes manejar la lógica para mostrar categorías existentes u otras acciones GET
        mensaje = "Página de categorías (GET)"
    return render_template("2 categoria.html", mensaje=mensaje)

""" 
@app.route("/iniciosesion", methods=["POST"])
def iniciarsecion():
    mensaje=""
    # este es el estado de si inicio o no sesion
    si_inicio=False
    try:
        usuario_nombre=request.form["usuario"]
        usuario_contraseña=request.form["contraseña"]
        datos_consulta={"usuario":usuario_nombre, "contraseña":usuario_contraseña}
        #usuario_basedd=usuarios.find_one(datos_consulta)
    
        if(usuario):
            email=yagmail.SMTP("gun45780@gmail.com",open(".contraseña").read(),encoding='UTF-8')
            asunto="confirmacion si funciona"
            mensaje=f"se informa al usuario {usuario} que ha ingresado al sistema "
            email.send(to="",subject=asunto,contents=mensaje)
            return redirect("/")
    except pymongo.erros as error:
        mensaje=error

    return render_template("formulario.html", si_inicio=si_inicio,mensaje=mensaje) """
#funcion y ruta de agregar productos
@app.route("/producto_añadido", methods=["POST","GET"] )
def producto_añadido(): 
    mensaje=None
    list_categorias=categorias.find()
    try:
        #gracias a este if no hay errores pero no lo entiendo
        if request.method=="POST":
            producto_codigo=request.form["codigo"]
            producto_nombre=request.form["nombre"]
            producto_precio=request.form["precio"]
            id_categoria=request.form["categoria"]

            producto={
                "codigo":int(producto_codigo),
                "nombre":producto_nombre,
                "precio":int(producto_precio),
                "categoria":id_categoria
            }
            accion_añadir=productos.insert_one(producto)
            if accion_añadir.acknowledged:
                mensaje="agregado"
            else:
                mensaje="error"

    except pymongo.errors.PyMongoError as error:
        print(f"{error}")
        #tener e cuenta que los datos que se traen de la bdd se deben renderisar
    return render_template("3 producto_añadido.html", mensaje=mensaje, categorias=list_categorias )

#funcion y ruta para mostrar productos en una tabla
@app.route("/tabla_productos", methods=["GET","POST"])
def tabla_productos():
    try:
        lis_productos = productos.find()
        li_producto = []

        for p in lis_productos:
            categoria_id = p.get('categoria')  # Obtener el ID de la categoría del producto
            if categoria_id and ObjectId.is_valid(categoria_id):  # Verificar si el ID de la categoría es válido
                categoria = categorias.find_one({'_id': ObjectId(categoria_id)})
                if categoria:
                    p['categoria'] = categoria['nombre']
            li_producto.append(p)

    except pymongo.errors.PyMongoError as error:
        print(f"{error}")

    return render_template("4 tablaproductos.html", productos=li_producto)

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
        
            buscar = {"_id": ObjectId(producto_id)}  # Corregido aquí
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

""" @app.route("/editar/",methods=["GET","POST"])
def vistatabla():
    return redirect("5 editar.html") """