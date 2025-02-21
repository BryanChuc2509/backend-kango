# Importaciones necesarias
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from bson import ObjectId
import database as dbase

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Conexión a la BD y objeto que contiene las colecciones etc.
db = dbase.dbConnect()

# Configuración de Swagger para la documentación de la API
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Gestión de Lugares"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Pagina principal del CRUD
@app.route("/")
def index():
    destinos = db['destinos']  # destinos es igual a la colección destinos dentro de la bd
    destinosReceived = destinos.find()  # Recibe los destinos para mostrar
    return render_template("", destinos=destinosReceived)

# METODO POST para Insertar
@app.route('/lugares', methods=['POST'])
def registrar_lugar():
    """
    7.1 Registrar lugar
    Esta función maneja la creación de un nuevo lugar en la base de datos.
    """
    # Obtener los datos del lugar desde la solicitud JSON
    data = request.get_json()
    
    # Crear un diccionario con los datos del nuevo lugar
    nuevo_lugar = {
        'Nombre': data['Nombre'],
        'Descripcion': data.get('Descripcion', ''),
        'Direccion': data.get('Direccion', '')
    }
    
    try:
        # Insertar el nuevo lugar en la base de datos
        result = db['destinos'].insert_one(nuevo_lugar)
        # Devolver una respuesta exitosa con el ID del nuevo lugar
        return jsonify({
            'mensaje': 'Lugar registrado exitosamente',
            'id': str(result.inserted_id)
        }), 201
    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return jsonify({'error': str(e)}), 400

# METODO PUT para Editar
@app.route('/lugares/<id>', methods=['PUT'])
def editar_lugar(id):
    """
    7.2 Editar información del lugar
    Esta función maneja la actualización de la información de un lugar existente.
    """
    try:
        # Obtener los nuevos datos del lugar desde la solicitud JSON
        data = request.get_json()
        
        # Verificar si el lugar existe
        if not db['destinos'].find_one({'_id': ObjectId(id)}):
            return jsonify({'error': 'Lugar no encontrado'}), 404
        
        # Actualizar la información del lugar en la base de datos
        result = db['destinos'].update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'Nombre': data.get('Nombre'),
                'Descripcion': data.get('Descripcion'),
                'Direccion': data.get('Direccion')
            }}
        )
        
        # Verificar si se realizaron cambios y devolver la respuesta apropiada
        if result.modified_count:
            return jsonify({'mensaje': 'Información del lugar actualizada exitosamente'}), 200
        return jsonify({'mensaje': 'No se realizaron cambios'}), 200
        
    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return jsonify({'error': str(e)}), 400

# METODO DELETE para Eliminar
@app.route('/lugares/<id>', methods=['DELETE'])
def eliminar_lugar(id):
    """
    7.3 Eliminar lugar
    Esta función maneja la eliminación de un lugar de la base de datos.
    """
    try:
        # Intentar eliminar el lugar de la base de datos
        result = db['destinos'].delete_one({'_id': ObjectId(id)})
        
        # Verificar si se eliminó el lugar y devolver la respuesta apropiada
        if result.deleted_count:
            return jsonify({'mensaje': 'Lugar eliminado exitosamente'}), 200
        return jsonify({'error': 'Lugar no encontrado'}), 404
        
    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return jsonify({'error': str(e)}), 400

# ERROR 404 EN CASO DE FALLO
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado, error: ' + request.url,
        'status': '404 NOT FOUND'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

# Debug mode, para correrlo así, en vez de utilizar flask run, utiliza py -m app
if __name__ == "__main__":
    app.run(debug=True, port=8080)