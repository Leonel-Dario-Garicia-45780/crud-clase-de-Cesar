from flask import request, jsonify
from modelos import Producto
from coneccion_engie import app


# Función para crear un nuevo producto
@app.route("/productos", methods=["POST"])
def crear_producto():
    data = request.json
    nuevo_producto = Producto(
        codigo=data["codigo"],
        nombre=data["nombre"],
        precio=data["precio"],
        categoria=data["categoria"]
    )
    nuevo_producto.save()
    return jsonify({"message": "Producto creado exitosamente"}), 201

# Función para obtener todos los productos
@app.route("/productos", methods=["GET"])
def obtener_productos():
    productos = Producto.objects().all()
    return jsonify(productos), 200

# Función para obtener un producto por su ID
@app.route("/productos/<id>", methods=["GET"])
def obtener_producto(id):
    producto = Producto.objects(id=id).first()
    if producto:
        return jsonify(producto), 200
    else:
        return jsonify({"message": "Producto no encontrado"}), 404

# Función para actualizar un producto
@app.route("/productos/<id>", methods=["PUT"])
def actualizar_producto(id):
    producto = Producto.objects(id=id).first()
    if producto:
        data = request.json
        producto.update(**data)
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    else:
        return jsonify({"message": "Producto no encontrado"}), 404

# Función para eliminar un producto
@app.route("/productos/<id>", methods=["DELETE"])
def eliminar_producto(id):
    producto = Producto.objects(id=id).first()
    if producto:
        producto.delete()
        return jsonify({"message": "Producto eliminado exitosamente"}), 200
    else:
        return jsonify({"message": "Producto no encontrado"}), 404

