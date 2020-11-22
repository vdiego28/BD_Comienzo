if __name__ == "__main__":
    from flask import Flask, json, request
    from pymongo import MongoClient
    USER = "grupo119"
    PASS = "grupo119"
    DATABASE = "grupo119"

    URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
    client = MongoClient(URL)

    USER_KEYS = ['uid', 'name', 'last_name',
                'occupation', 'follows', 'age']

    # Base de datos del grupo
    db = client["grupo119"]

    # Seleccionamos la collección de usuarios
    usuarios = db.usuarios

    # Iniciamos la aplicación de flask
    app = Flask(__name__)


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola, estas en el archivo de usuarios!</h1>"

@app.route("/users")
def get_users():
    '''
    Obtiene todos los usuarios
    '''
    users = list(usuarios.find({}, {"_id": 0}))
    return json.jsonify(users)

@app.route("/users/<int:uid>")
def get_user(uid):
    '''
    Obtiene el usuario de id entregada
    '''
    #falta chequear que la id exista
    try:
        user = list(usuarios.find({"uid": uid}, {"_id": 0}))
        return json.jsonify(user)
    except KeyError:
        return json.jsonify(["No existe la id"]) #funcionaria esta wea?


if __name__ == "__main__":
    app.run(debug=True)
