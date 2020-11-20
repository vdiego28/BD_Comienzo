if __name__ == "__main__":
    from flask import Flask, json, request
    from pymongo import MongoClient


    USER = "grupo119"
    PASS = "grupo119"
    DATABASE = "grupo119"

    URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
    client = MongoClient(URL)

    MESSAGES_KEYS = ['desired', 'required', 'forbidden', 'userId']

    # Base de datos del grupo
    db = client["grupo119"]

    # Seleccionamos la collección de message
    messages = db.messages

    # Iniciamos la aplicación de flask
    app = Flask(__name__)


'''
ejemplo: {
    "desired":["Hola", "Viste las noticias?"],
    "required": ["arrastre", "magikarp"],
    "forbidden": ["origami", "Qué","tal?"],
    "userId":
    }
'''


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola, estas en archivo de busqueda!</h1>"

@app.route("/text-search")
def search_messages():
    '''
    Obtiene el contenido de los mensajes
    ejemplo: collection.find({"$text": {"$search": your search}})
    '''
    recived = {key: request.json[key] for key in MESSAGES_KEYS}
    # recievd = request.json[key]
    maybe = " ".join(recived["desired"])
    # guardamos los maybe
    data = messages.find({'$text': {'$search': maybe}}, {"description.value": 1})
    # Guardamos los obligatorios
    for key in recived["required"]:
        data = messages.distinct({'$text': {"$search": f"(\"{key}\""}}, {"description.value": 1})
    # Sacamos los prohibidos
    for key in recived["forbidden"]:
        data = messages.distinct({'$text': {"$search": f"(-\"{key}\""}}, {"description.value": 1})
    data = messages.find({"userId": recived["userId"]})
    return json.jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
