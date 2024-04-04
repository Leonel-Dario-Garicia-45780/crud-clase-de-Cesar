from flask import request, jsonify
from modelos import Categoria
from coneccion_engie import app


# Función para agregar una nueva categoría
@app.route("/categorias", methods=["POST"])
def agregar_categoria():
    data = request.json
    nueva_categoria = Categoria(
        nombre=data["nombre"]
    )
    nueva_categoria.save()
    return jsonify({"message": "Categoría agregada exitosamente"}), 201

# Función para eliminar una categoría
@app.route("/categorias/<id>", methods=["DELETE"])
def eliminar_categoria(id):
    categoria = Categoria.objects(id=id).first()
    if categoria:
        categoria.delete()
        return jsonify({"message": "Categoría eliminada exitosamente"}), 200
    else:
        return jsonify({"message": "Categoría no encontrada"}), 404

