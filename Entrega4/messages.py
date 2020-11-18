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

    # Seleccionamos la collección de message
    messages = db.messages

    #Iniciamos la aplicación de flask
    app = Flask(__name__)


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola!</h1>"


@app.route("/messages")
def get_messages():
    '''
    Obtiene todos los message
    '''
    message = list(messages.find({}, {"_id": 0}))
    return json.jsonify(message)


@app.route("/messages/<int:mid>")
def get_message(mid):
    '''
    Obtiene el message de id entregada
    '''
    message = list(messages.find({"mid": mid}, {"_id": 0}))
    return json.jsonify(message)


@app.route("/messages?id1=<int:uid1>&id2=<int:uid2>")
def get_messages_users(uid1, uid2):
    '''
    Obtiene el usuario de id entregada
    '''
    message = list(messages.find({"sender":uid1, "receptant":uid2}, {"sender":uid2, "receptant":uid1}, {"_id": 0}))
    return json.jsonify(message)


@app.route("/messages", methods=['POST'])
def create_messages():
    '''
    Crea un nuevo messages en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''
    data = {key: request.json[key] for key in MESSAGES_KEYS}
    # El valor de result nos puede ayudar a revisar
    # si el usuario fue insertado con éxito
    result = messages.insert_one(data)
    return json.jsonify({"success": True})


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


if __name__ == "__main__":
    app.run(debug=True)


# mongo -u grupo119 -p grupo119 gray.ing.puc.cl/grupo119 --authenticationDatabase admin