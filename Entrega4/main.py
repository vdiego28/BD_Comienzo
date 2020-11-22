if __name__ == "__main__":
    from flask import Flask, json, request
    from pymongo import MongoClient

    USER = "grupo119"
    PASS = "grupo119"
    DATABASE = "grupo119"

    URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
    client = MongoClient(URL)

    MESSAGES_KEYS = ['uid', 'name', 'last_name', 'occupation', 'follows', 'age']

    # Base de datos del grupo
    db = client["grupo119"]

    # Seleccionamos los collections
    messages = db.messages
    usuarios = db.usuarios

    # Iniciamos la aplicación de flask
    app = Flask(__name__)


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola, estas en el archivo de main!</h1>"

# Users
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
    user = list(usuarios.find({"uid": uid}, {"_id": 0}))
    return json.jsonify(user)

#Messages
@app.route("/messages")
def get_messages():
    '''
    Obtiene todos los message
    '''
    try:  # Intenta obtener los dos ids desde el url del tipo ?id1=57&id2=35
        uid1 = int(request.args["id1"])
        uid2 = int(request.args["id2"])
        first = {"$and": [{"sender": uid1}, {"receptant": uid2}]}
        second = {"$and": [{"sender": uid2}, {"receptant": uid1}]}
        busqueda = {"$or": [first, second]}
        result = list(messages.find(busqueda, {"_id": 0}))
        return json.jsonify(result)
    except KeyError:  # Si estos ids no existen, entonces entregamos todos los mensajes
        message = list(messages.find({}, {"_id": 0}))
        return json.jsonify(message)


@app.route("/messages/<int:mid>")
def get_message(mid):
    '''
    Obtiene el message de id entregada
    '''
    message = list(messages.find({"mid": mid}, {"_id": 0}))
    return json.jsonify(message)


# @app.route("/messages?id1=<int:uid1>&id2=<int:uid2>")
def get_messages_users(uid1, uid2):
    '''
    Obtiene los usuarios de ids entregadas
    Busca messages en ambas direcciones
    '''
    first = [{"sender": uid1}, {"receptant": uid2}]
    second = [{"sender": uid2}, {"receptant": uid1}]
    busqueda = {"$or": [first, second]}
    result = list(messages.find({"receptant": uid1}, {"_id": 0}))
    return json.jsonify(result)


@app.route("/messages", methods=['POST'])
def create_messages():
    '''
    Crea un nuevo messages en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''
    mid = list(messages.find({"mid": request.json["mid"]}))
    if len(mid) != 0:
        return json.jsonify({"success": False})
    try:
        data = {key: request.json[key] for key in MESSAGES_KEYS}
        # El valor de result nos puede ayudar a revisar
        # si el usuario fue insertado con éxito
        result = messages.insert_one(data)
        return json.jsonify({"success": True})
    except KeyError:  # Si algún valor no se entregó se levanta esta excepción y retornamos
        return json.jsonify({"success": "Faltan valores de llaves"})


@app.route("/messages", methods=['DELETE'])
def delete_messages():
    '''
    Elimina el messages de id entregada
    '''
    try:
        mid = request.json['mid']
        messages.remove({"mid": mid})
        return json.jsonify({"success": True})
    except TypeError:  # Si falla entonces retornamos False
        return json.jsonify({"success": False})


#Busqueda de texto
@app.route("/text-search")
def search_messages():
    '''
    Obtiene el contenido de los mensajes
    ejemplo: collection.find({"$text": {"$search": your search}})
    '''
    recived = {key: request.json[key] for key in MESSAGES_KEYS}
    # recievd = request.json[key]
    busqueda = ""
    if "required" in recived.keys():  # Ingresamos los valores obligatorios
        if len(recived["required"]) > 0:
            obligatorio = "\"" + "\" \"".join(recived["required"]) + "\" "
            busqueda += obligatorio
    if "desired" in recived.keys():  # agregamos los valores deseados
        if len(recived["desired"]) > 0:
            maybe = " " + " ".join(recived["desired"])
            busqueda += maybe
    if "forbidden" in recived.keys():  # agregamos los valores prohibidos
        if len(recived["forbidden"]) > 0:
            prohibido = " -\"" + "\" -\"".join(recived["forbidden"]) + "\" "
            if len(busqueda) == 0:
                result = messages.find({"$and": [{'$text': {"$search": {'$not': {'$in': recived["forbidden"]}}}}, {"sender": recived["userId"]}]}, {"_id": 0})
                return json.jsonify(list(result))
            busqueda += "x " + prohibido
    print(busqueda)
    if len(busqueda) > 0:
        message = list(messages.find({"$and": [{"$text": {"$search": busqueda}}, {"sender": recived["userId"]}]}, {"_id": 0}))
    else:
        message = list(messages.find({"sender": recived["userId"]}, {"_id": 0}))
    return json.jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
