if __name__ == "__main__":
    from flask import Flask, json, request
    from pymongo import MongoClient


    USER = "grupo119"
    PASS = "grupo119"
    DATABASE = "grupo119"

    URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
    client = MongoClient(URL)

    MESSAGES_KEYS = ['uid', 'name', 'last_name',
                'occupation', 'follows', 'age']

    # Base de datos del grupo
    db = client["grupo119"]

    # Seleccionamos la collección de message
    messages = db.messages

    # Iniciamos la aplicación de flask
    app = Flask(__name__)


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola, estas en archivo de busqueda!</h1>"

@app.route("/text-search)
def search_messages(mid):
    '''
    Obtiene el contenido de los mensajes
    '''
    recived = {key: request.json[key] for key in MESSAGES_KEYS}
    maybe = " ".join(recived["maybe"])
    # guardamos los maybe
    data = messages.find({"sender": recived["userID"]}, {$text: {$search: maybe}}, {"description.value": 1})
    # Guardamos los obligatorios
    for key in recived["required"]:
        data = data.find({$text: {"$search": f"(\"{key}\""}}, {"description.value": 1})
    # Sacamos los prohibidos
    for key in recived["forbidden"]:
        data = data.find({$text: {"$search": f"(-\"{key}\""}}, {"description.value": 1})
    return json.jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
