<?php include('templates/header.html'); ?>

<body>
  <p style="text-align:center;">Menú de inicio</p>
  <br>

  <form align="center" action="mapa.php">
        Ir a funcionalidades PDI
        <input type="hidden" name="current_user" value="1">
        <input type="submit" value="Ingresar">
  </form>

  <br>
  <br>
  <br>

  <form align="center" action="form_sent.php">
        Ir a busqueda de mensaje enviados
        <input type="hidden" name="current_user" value="1">
        <input type="submit" value="Buscar">
  </form>

<br>
<br>
<br>

<form align="center" action="form_rec.php">
  Ir a busqueda de mensaje recibidos
  <input type="hidden" id="1">
  <input type="submit" value="Buscar">
</form>

<br>
<br>
<br>

<form align="center" action="busqueda_texto_mensaje.php">
    Busqueda de mensajes avanzada
    userId:
    <input type="text" name="userId">
    </br>
    Obligatorias:
    <input type="text" name="required">
    </br>
    Prohibidas:
    <input type="text" name="forbidden">
    </br>
    Deseadas:
    <input type="text" name="desired">
  <input type="hidden" name="current_user" value="1">
  <input type="submit" value="Buscar">
</form>