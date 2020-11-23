# README Entrega 4 Grupo 119

El archivo principal es main.py, el resto de los archivos con extensión .py fueron usados para crear las funciones de una manera más ordenada. Dentro del archivo main.py está separado en "secciones" las funciones.

- Primero están las 3 de usuarios que son bastante simples.
- Segundo, las 3 rutas de mensajes en donde la ruta "/messages" entrega todos los mensajes si el url solo contine "/messages" o entrega los mensajes intercambiados entre dos usuarios si el url es del tipo "/messages$id1=<**id1**>&id2=<**id2**>".
- Finalmente está la ruta de text-search, en donde realizan dos busquedas, una con las palabras que se quieren que esten en los mensajes y otra con las palabras que no se quieren en los mensajes, luego estas se filtran quitando de la lista con palabras deseadas los mensajes que tambien estén en la lista de palabras no deseadas. Se espera que el input entregado sea del estilo, {

Dentro de la carpeta 4 está el PipFile y se explica con más detalle el funcionamiento de las funciones.
