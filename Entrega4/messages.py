if __name__ == "__main__":
    from flask import Flask, json, request
    from pymongo import MongoClient

    USER = "grupo119"
    PASS = "grupo119"
    DATABASE = "grupo119"

    URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
    client = MongoClient(URL)

    MESSAGES_KEYS = ['date', 'lat', 'long', 'message', 'mid', 'receptant', 'sender']

    # Base de datos del grupo
    db = client["grupo119"]

    # Seleccionamos la collección de message
    messages = db.messages

    #Iniciamos la aplicación de flask
    app = Flask(__name__)


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola, estas en el archivo de menssages!</h1>"


@app.route("/messages")
def get_messages():
    '''
    Obtiene todos los message
    '''
    try:
        uid1 = int(request.args["id1"])
        uid2 = int(request.args["id2"])
        first = {"$and": [{"sender": uid1}, {"receptant": uid2}]}
        second = {"$and": [{"sender": uid2}, {"receptant": uid1}]}
        busqueda = {"$or": [first, second]}
        result = list(messages.find(busqueda, {"_id": 0}))
        if len(result) != 0:
            return json.jsonify(result)
        else:
            return json.jsonify([{"success": False, "Error": "No existe un mensaje con este mid"}])
    except KeyError:
        result = list(messages.find({}, {"_id": 0}))
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
    Obtiene el usuario de id entregada
    '''
    print(uid1)
    first = [{"sender": uid1}, {"receptant": uid2}]
    second = [{"sender": uid2}, {"receptant": uid1}]
    busqueda = {"or": [first, second]}
    result = list(messages.find({"$or": busqueda["or"]}, {"_id": 0}))
    if len(result) != 0:
        return json.jsonify(result)
    else:
        return json.jsonify({"success": False, "Error": "No existe un mensaje con este mid"})


@app.route("/messages", methods=['POST'])
def create_messages():
    '''
    Crea un nuevo messages en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''
    try:
        MESSAGE_KEYS2 = ['date', 'lat', 'long', 'message', 'receptant', 'sender']
        faltantes = []

        for key in MESSAGE_KEYS2:
            if key not in request.json.keys():
                faltantes.append(key)

        if faltantes:
            return json.jsonify([{'success': False, 'Required Keys': [key for key in faltantes]}])
        data = {key: request.json[key] for key in MESSAGES_KEYS2}
        mid = messages.find_one(sort=[("mid", -1)])["mid"] + 1
        data['mid'] = mid
        messages.insert_one(data)
        return json.jsonify([{"success": True}])

    except KeyError:  # Si algún valor no sirve como llave...
        return json.jsonify([{"success": 'False', 'Error': 'Keys invalidas entregadas'}])


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
        return json.jsonify({"success": False, "Error": f"No existe mensaje con mid: {mid}""})


if __name__ == "__main__":
    app.run(debug=True)
