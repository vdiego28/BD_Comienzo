<?php include('templates/header.html'); ?>

<body>
  <p style="text-align:center;">Busqueda de mensaje enviados</p>
  <br>

  <form align="center" action="search_sent.php">
        <input type="text" name="contraseña_usuario">
        <br/><br/>
        <input type="submit" value="Ingresar">
        <input type="hidden" id="1">
  </form>

  <br>
  <br>
  <br>

  <form align="center" action="nueva_sesion.php">
      ¡¿No se ha creado una sesión?! Registrese acá
    <input type="submit" value="Registrase">
  </form>