from flask import request, jsonify
from modelos import Usuario
from coneccion_engie import app

# Función para crear un nuevo usuario
@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.json
    nuevo_usuario = Usuario(
        correo=data["correo"],
        contraseña=data["contraseña"]
    )
    nuevo_usuario.save()
    return jsonify({"message": "Usuario creado exitosamente"}), 201

# Función para obtener todos los usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    usuarios = Usuario.objects().all()
    return jsonify(usuarios), 200

# Función para obtener un usuario por su ID
@app.route("/usuarios/<id>", methods=["GET"])
def obtener_usuario(id):
    usuario = Usuario.objects(id=id).first()
    if usuario:
        return jsonify(usuario), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# Función para actualizar un usuario
@app.route("/usuarios/<id>", methods=["PUT"])
def actualizar_usuario(id):
    usuario = Usuario.objects(id=id).first()
    if usuario:
        data = request.json
        usuario.update(**data)
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# Función para eliminar un usuario
@app.route("/usuarios/<id>", methods=["DELETE"])
def eliminar_usuario(id):
    usuario = Usuario.objects(id=id).first()
    if usuario:
        usuario.delete()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404


