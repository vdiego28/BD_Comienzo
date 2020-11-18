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
    return "<h1>¡Hola, estas en el archivo de mensajes!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
