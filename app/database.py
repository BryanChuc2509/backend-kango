#IMPORTANTE, NO MODIFICAR LAS CREDENCIALES NI LA FUNCION DE CONEXION A LA BD
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
uri = "mongodb+srv://databaseAccessPoint:dFzZn97QZgey2LZ@kankuntransportes.bxmqo.mongodb.net/?retryWrites=true&w=majority&appName=KanKunTransportes" 
#Credenciales mongodb desglosado
# "mongodb+srv:                                                 Aqui se esta utilizando pymongo
# databaseAccessPoint : dFzZn97QZgey2LZ                         Nombre de usuario y contraseña que se van a utilizar para la app
# @kankuntransportes.bxmqo.mongodb.net                          Url a acceder, donde se encuentra el cluster
# /?retryWrites=true&w=majority&appName=KanKunTransportes"      algunas configs y el nombre de la app

ca = certifi.where()    #Verifica las rutas de la bd, algo asi entendi

#Trata de conectar a la bd
def dbConnect():
    try:
        client = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=ca) #Conexion a Mongo
        db = client["kankunDBT"] #Base de datos utilizada
        return db   #Retorna la bd conectada para utilizarla
    except ConnectionError as e:    #En caso de error, no retorna nada
        print(e)
        return None
    


#Trata de conectar a la bd dentro del cluster, si no existe, se crea
def get_database():
    try:
        client = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=ca)
        db = client["kankunDBT"]

        # Verifica si la colección existe
        collection_name = "products"  # Nombre de la coleccion a verificar
        if collection_name not in db.list_collection_names():
            print(f"La colección '{collection_name}' no existe. Creándola...")

            # Inserta un documento temporal (MongoDB crea la colección automáticamente)
            db[collection_name].insert_one({"name": "Producto de prueba", "price": 0, 'quantity': 0})
            print("Colección creada con un documento de prueba.")
        return db
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        return None

# database = get_database()