from flask import Flask, json, request
from pymongo import MongoClient
from datetime import datetime

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


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola!</h1>"


@app.route("/busqueda-buque")
def buque():
    '''
    Usar agregacion para cambiar el formato de la fecha en la base de datos
    '''
    recived = request.json
    if not recived:
        return {"Succes": "nada"}
    inicio = recived["fecha_inicio"].replace("-", "/")
    # inicio = [inicio[2], inicio[1], inicio[0]]
    inicio_correcto = "/".join(inicio)
    fin = recived["fecha_termino"].replace("-", "/")
    # fin = [fin[2], fin[1], fin[0]]
    fin_correcto = "/".join(fin)
    print(inicio, fin)
    inicio_correcto = datetime.strptime(inicio, '%Y/%m/%d')
    fin_correcto = datetime.strptime(fin, '%Y/%m/%d')
    user = recived["userId"]
    words = recived["palabras_clave"].replace(",", " ")
    valor_or = {"search": {"$or": [{"sender": user}, {"receptant": user}]}}
    buque_text_l = list(messages.find({"$text": {"$search": words}}, {"_id": 0, "mid": 1}))
    buque_text = set([i['mid'] for i in buque_text_l])
    buques_user_2 = list(messages.find({"$or": [{"sender": user}, {"receptant": user}]}, {"_id": 0, "mid": 1}))
    buques_user = set([i['mid'] for i in buques_user_2])

    buques_date_i = list(messages.find(
        {"$expr": {
            "$gte": [{ "$dateFromString": { "dateString": "$date" }}, inicio_correcto ]}}, {"_id": 0, "mid": 1}))

    buques_date_f = list(messages.find(
        {"$expr": {
            "$lte": [{ "$dateFromString": { "dateString": "$date" }}, fin_correcto ]}}, {"_id": 0, "mid": 1}))

    buques_date_inicio = set([i['mid'] for i in buques_date_i])
    buques_date_fin = set([i['mid'] for i in buques_date_f])

    result = buques_date_inicio.intersection(buques_user).intersection(buque_text).intersection(buques_date_fin)
    final = list(messages.find({'mid': {"$in": list(result)}}, {"_id": 0}))

    return json.jsonify(final)


@app.route("/receptant")
def message_recived():
    '''
    Obtiene el message de id entregada
    '''
    recived = request.json
    if not recived:
        return json.jsonify({"success": False, "Error": f"No entrega mensaje"})
    receptant = recived["userId"]
    message = list(messages.find({"receptant": receptant}, {"_id": 0}))
    if len(message) != 0:
        return json.jsonify(message)
    else:
        return json.jsonify([{"success": False, "Error": f"No existe un mensaje enviado a {receptant}"}])


@app.route("/sender")
def message_send():
    '''
    Obtiene el message de id entregada
    '''
    sender = request.json
    if not sender:
        return json.jsonify([{"success": False, "Error": f"No entrega mensaje"}])
    sender = sender["userId"]
    message = list(messages.find({"sender": sender}, {"_id": 0}))
    if len(message) != 0:
        return json.jsonify(message)
    else:
        return json.jsonify(
            [{"success": False, "Error": f"No existe un mensaje con sender {sender}"}])


@app.route("/users")
def message_user():
    '''
    Obtiene el message de id entregada
    '''
    sender = request.json
    if not sender:
        return json.jsonify([{"success": False, "Error": f"No entrega mensaje"}])
    sender = sender["userId"]
    message = list(messages.find({"receptant": sender}, {"_id": 0}))
    if len(message) != 0:
        return json.jsonify(message)
    else:
        return json.jsonify(
            [{"success": False, "Error": f"No existe un mensaje con sender {sender}"}])


@app.route("/messages/<int:sender>", methods=['POST'])
def create_messages(sender):
    '''
    Crea un nuevo messages en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''
    MESSAGE_KEYS_2 = ['date', 'lat', 'long', 'message', 'receptant']
    try:
        faltantes = []
        for key in MESSAGE_KEYS_2:
            if key not in request.json.keys():
                faltantes.append(key)

        if faltantes:
            return json.jsonify([{'success': False, 'Required Keys': [key for key in faltantes]}])
        data = {key: request.json[key] for key in MESSAGE_KEYS_2}
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


if __name__ == "__main__":
    app.run(debug=True)
