if __name__ == "__main__":
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


# Sección usuarios
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
    if len(user) != 0:
        return json.jsonify(user)
    else:
        return json.jsonify([{"success": False, "Error": f"No existe un mensaje con uid {uid}"}])

# Sección mensajes
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
            return json.jsonify([{"success": False, "Error": "No existe un mensajes entre estos usuarios"}])
    except KeyError:
        result = list(messages.find({}, {"_id": 0}))
        return json.jsonify(result)


@app.route("/messages/<int:mid>")
def get_message(mid):
    '''
    Obtiene el message de id entregada
    '''
    message = list(messages.find({"mid": mid}, {"_id": 0}))
    if len(message) != 0:
        return json.jsonify(message)
    else:
        return json.jsonify([{"success": False, "Error": f"No existe un mensaje con uid {mid}"}])


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
        return json.jsonify({"success": False, "Error": f"No existe mensaje con mid: {mid}"})


# Sección busqueda de texto
'''
Se espera que el contenido del body sea del estilo:
{
    "desired": ["Buenas tarde", "P=NP => N=1"],
    "required": ["Saludos"],
    "forbidden": ["Palabrotas", "GPU"],
    "userId": 0
    }
'''


@app.route("/text-search")
def search_messages():
    '''
    Obtiene el contenido del body, si este no tiene todas las llaves o está vacio retornamos el error
    '''
    try:
        recived = {key: request.json[key] for key in SEARCH_KEYS}
        if not recived:
            result = list(messages.find({}, {"_id": 0}))
            return json.jsonify(result)
    except KeyError:
        return json.jsonify([{"success": "Falta(n) llave(s)"}])
    except TypeError:
        result = list(messages.find({}, {"_id": 0}))
        return json.jsonify(result)
    busqueda_buena = ""
    d_malos = []

    '''
    Primero tomo todas las palabras que se requiere que estén y las uno entre comillas
    Luego las guardo todas en un un string
    '''

    if len(recived["required"]) > 0:
        obligatorio = "\"" + "\" \"".join(recived["required"]) + "\" "
        busqueda_buena += obligatorio
        print(busqueda_buena)

    '''
    Segundo tomo todas las palabras que pueden como pueden que no estén
    Luego las guardo todas en el mismo string de antes
    '''

    if len(recived["desired"]) > 0:
        maybe = " " + " ".join(recived["desired"])
        busqueda_buena += maybe

    '''
    Tercero, tomamos las palabras que no deben estar y las unimos
    Realizamos una busqueda en donde el usuario debe ser igual al entregado y los mensajes contengan las palabras prohibidas
    Guardamos los ids de los mensajes encontrados
    '''
    if len(recived["forbidden"]) > 0:
        negativ = "\"" + "\" \"".join(recived["forbidden"]) + "\" "
        alternative = " ".join(recived["forbidden"])
        d_malos = list(messages.find({"$and": [{"sender": recived["userId"]},{"$text": {"$search": alternative}}]}, {"_id": 0}))
        print("lista prohibida ", d_malos)

    '''
    Si no hay palabras obligatorias o deseadas entonces buscamos todos los mensajes del usuario
    sino, buscamos las palabras
    '''
    if len(busqueda_buena) > 0:
        d_buenos = list(messages.find({"$and": [{"sender": recived["userId"]},{"$text": {"$search": busqueda_buena}}]}, {"_id": 0}))
    else:
        d_buenos = list(messages.find({"sender": recived["userId"]}, {"_id": 0, "mid": 1}))

    '''
    Guardamos los ids de los mensajes dentro de Sets y luego eliminamos los resultados de las palabras prohibidas
    '''
    set_buenos = set([i['mid'] for i in d_buenos])
    print(set_buenos)
    set_malos = set([i['mid'] for i in d_malos])
    print(set_malos)
    resultado_final = list(set_buenos - set_malos)
    print(resultado_final)

    '''
    Finalmente realizamos una busqueda en donde los mensajes tengan el ids de los mensajes que se filtraron anteriormente
    '''
    result = list(messages.find({'mid': {"$in": resultado_final}}, {"_id": 0}))
    return json.jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
