from flask_restx import Namespace, Resource
ping_namespace = Namespace("ping")

class Ping(Resource):
    '''
    Simple servicio para comprobar si el backend está funcionando.
    '''
    def get(self):
        return {"status": "success", "message": "pong!"}

ping_namespace.add_resource(Ping, "")