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
    "userId": 19
    }
'''


@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola, estas en archivo de busqueda!</h1>"


'''
Se espera que el contenido del body sea del estilo:
{
    "desired": palabras_deseada,
    "required": palabras_obligatoria,
    "forbidden": palabras_prohibida,
    "userId": Id_usuario
    }
'''
@app.route("/text-search")
def search_messages():
    '''
    Obtiene el contenido del body, si este no tiene todas las llaves o está vacio retornamos el error
    '''
    try:
        recived = {key: request.json[key] for key in MESSAGES_KEYS}
        if not received:
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
        obligatorio = "\"" + "\" \"".joi
        n(recived["required"]) + "\" "
        busqueda_buena += obligatorio

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
        prohibido = " -\"" + "\" -\"".join(recived["forbidden"]) + "\" "
        negativ = "\"" + "\" \"".join(recived["forbidden"]) + "\" "
        d_malos = list(messages.find({"$and": [{"sender": recived["userId"]},{"$text": {"$search": negativ}}]}, {"_id": 0}))

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
    set_malos = set([i['mid'] for i in d_malos])
    resultado_final = list(set_buenos - set_malos)

    '''
    Finalmente realizamos una busqueda en donde los mensajes tengan el ids de los mensajes que se filtraron anteriormente
    '''
    result = list(messages.find({'mid': {"$in": resultado_final}}, {"_id": 0}))
    return json.jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
