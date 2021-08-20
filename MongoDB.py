import pymongo


class MongoDB:
    def __init__(self):
        pass

    def mongoConnect(self):
        Mongo_URI = "mongodb+srv://m001-student:123asterisco@sandbox.kvjof.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        try:
            self.cliente = pymongo.MongoClient(Mongo_URI)
            self.cliente.server_info()
            return "Conexion a MongoDB Exitosa"
        except pymongo.errors.ConnectionFailure as errorConexion:
            self.cliente = pymongo.MongoClient('localhost', 27017)
            self.cliente.server_info()

    def insertData(self, data):
        try:
            self.mydb = self.cliente['adonis']
            self.tabla = self.mydb['people']
            self.datosIns = self.tabla.insert_one(data)
            return "Datos insertados a MongoDB"
        except:
            return "No se insertado"
