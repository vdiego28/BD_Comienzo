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


@app.route("/algo")
def message_recived():
    '''
    Obtiene el message de id entregada
    '''
    return json.jsonify([{"success": False}])


app.run(debug=True)
