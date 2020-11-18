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

    #Iniciamos la aplicación de flask
    app = Flask(__name__)


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola!</h1>"

@app.route("/<str:mid>")
def search_messages(mid):
    '''
    Obtiene el message de id entregada
    '''
    message = list(messages.find({"mid": mid}, {"_id": 0}))
    return json.jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
