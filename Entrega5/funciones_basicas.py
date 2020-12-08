from flask import Flask, json, request
from pymongo import MongoClient

USER = "grupo119"
PASS = "grupo119"
DATABASE = "grupo119"

URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
client = MongoClient(URL)

MESSAGES_KEYS = ['uid', 'name', 'last_name', 'occupation', 'follows', 'age']
SEARCH_KEYS = ['desired', 'required', 'forbidden', 'userId']

# Base de datos del grupo
db = client["grupo119"]

# Seleccionamos los collections
messages = db.messages
usuarios = db.usuarios

# Iniciamos la aplicación de flask
app = Flask(__name__)


@app.route("/receptant/<int:receptant>")
def get_message(receptant):
    '''
    Obtiene el message de id entregada
    '''
    message = list(messages.find({"receptant": receptant}, {"_id": 0}))
    if len(message) != 0:
        return json.jsonify(message)
    else:
        return json.jsonify([{"success": False, "Error": f"No existe un mensaje con uid {mid}"}])


@app.route("/sent/<int:sender>")
def get_message(sender):
    '''
    Obtiene el message de id entregada
    '''
    message = list(messages.find({"sender": sender}, {"_id": 0}))
    if len(message) != 0:
        return json.jsonify(message)
    else:
        return json.jsonify(
            [{"success": False, "Error": f"No existe un mensaje con uid {mid}"}])


@app.route("/messages/<int:sender>", methods=['POST'])
def create_messages(sender):
    '''
    Crea un nuevo messages en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''
    try:
        MESSAGE_KEYS2 = ['date', 'lat', 'long', 'message', 'receptant']
        faltantes = []
        for key in MESSAGE_KEYS2:
            if key not in request.json.keys():
                faltantes.append(key)

        if faltantes:
            return json.jsonify([{'success': False, 'Required Keys': [key for key in faltantes]}])
        data = {key: request.json[key] for key in MESSAGES_KEYS2}
        mid = messages.find_one(sort=[("mid", -1)])["mid"] + 1
        data["sender"] = sender
        data['mid'] = mid
        messages.insert_one(data)
        return json.jsonify([{"success": True}])

    except KeyError:  # Si algún valor no sirve como llave...
        return json.jsonify([{"success": 'False', 'Error': 'Keys invalidas entregadas'}])



@app.route("/text-search")
def search_messages():
    recived = request.json
    for llave in SEARCH_KEYS:
        if llave not in recived.keys():
            recived[llave] = []

    busqueda_buena = ""
    d_malos = []

    if len(recived["required"]) > 0:
        obligatorio = "\"" + "\" \"".join(recived["required"]) + "\" "
        busqueda_buena += obligatorio

    if len(recived["desired"]) > 0:
        maybe = " " + " ".join(recived["desired"])
        busqueda_buena += maybe

    if len(recived["forbidden"]) > 0:
        negativ = "\"" + "\" \"".join(recived["forbidden"]) + "\" "
        alternative = " ".join(recived["forbidden"])
        if recived["userId"] != []:
            d_malos = list(messages.find({"$and": [{"sender": recived["userId"]},{"$text": {"$search": alternative}}]}, {"_id": 0}))
        else:
            d_malos = list(messages.find({"$text": {"$search": alternative}}, {"_id": 0}))
    if len(busqueda_buena) > 0:
        if recived["userId"] != []:
            d_buenos = list(messages.find({"$and": [{"sender": recived["userId"]},{"$text": {"$search": busqueda_buena}}]}, {"_id": 0}))
        else:
            d_buenos = list(messages.find({"$text": {"$search": busqueda_buena}}, {"_id": 0}))

    else:
        if recived["userId"] != []:
            d_buenos = list(messages.find({"sender": recived["userId"]}, {"_id": 0, "mid": 1}))
        else:
            d_buenos = list(messages.find({}, {"_id": 0, "mid": 1}))

    set_buenos = set([i['mid'] for i in d_buenos])
    set_malos = set([i['mid'] for i in d_malos])
    resultado_final = list(set_buenos - set_malos)

    result = list(messages.find({'mid': {"$in": resultado_final}}, {"_id": 0}))
    return json.jsonify(result)


app.run(debug=True)
