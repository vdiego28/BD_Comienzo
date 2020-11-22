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
    usuarios = db.usuarios

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
    error = False
    if not recived:#el diccionario esta vacio
        error=True #deben retornarse todos los mensajes
    #if False:#no hay body, no se como verificarlo?
     #   error=True
    if error:
        message = list(messages.find({}, {"_id": 0}))
        return json.jsonify(message)
    only=False #si solo esta forbidden
    ''' 1. Si solo se entregan palabras prohibidas, la busqueda de texto de mongo no entregar´a r
    resultados, as´ı que uds deben resolver c´omo entregar todos los mensajes excepto aquellos
que contengan palabras prohibidas. (st only y lista forb)
        2. chequear que el id exista. Si no existe, se debe retornar un error amigable al usuario (no un
INTERNAL SERVER ERROR). su try y pico?
        3. Funciona recived como un dict, cierto?
        4. Si no llega body se deben retornar todos los mensajes (if false...)
        5. Se puede hacer una busqueda sin user_id?'''
    #chequeando id
    if not "userId" in recived.keys():
        return json.jsonify(["No hay id"])

    # recievd = request.json[key]
    busqueda = ""
    if "required" in recived.keys():#funciona esto??? es un dict o no?
        if len(recived["required"]) > 0:
            obligatorio = "\"" + "\" \"".join(recived["required"]) + "\" "
            busqueda += obligatorio
    if "forbidden" in recived.keys():
        if len(recived["forbidden"]) > 0:
            prohibido = " -\"" + "\" -\"".join(recived["forbidden"]) + "\" "
            busqueda += prohibido
            if "desired" not in recived.keys() and "required" not in recived.keys():
                only=True
                forb=recived["forbidden"]
    if "desired" in recived.keys():
        if len(recived["desired"]) > 0:
            maybe = " " + " ".join(recived["desired"])
            busqueda += maybe
    print(busqueda)
    if only:
        pass #se debe buscar manualmente (piola) las weas
    if len(busqueda) > 0:
        message = list(messages.find({"$and": [{"$text": {"$search": busqueda}}, {"sender": recived["userId"]}]}, {"_id": 0}))
    else:# el $and?
        message = list(messages.find({"sender": recived["userId"]}, {"_id": 0}))
    return json.jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
