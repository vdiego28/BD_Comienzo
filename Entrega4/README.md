El archivo principal es main.py, el resto fue de archivos con extensión .py fueron usados para crear las funciones. Dentro del archivo main.py está separado en 'secciones' las funciones.

Primero están las 3 de usuarios que son bastante simples.

Segundo, las 3 rutas de mensajes en donde la ruta "/messages" entrega todos los mensajes si el url solo contine "/messages" o entrega los mensajes intercambiados entre dos usuarios si el url es del tipo "/messages$id1=<**id1**>&id2=<**id2**>".

Finalmente está la ruta de text-search, en donde se agrega a un string las palabras que se están buscando. Si se le entrega solo palabras negativas actualmente el programa retorna una lista vacía.

Dentro de la carpeta 4 está el PipFile.
