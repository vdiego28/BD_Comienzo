<?php include('templates/header.html'); ?>

<body>
  <p style="text-align:center;">Inicio de sesión</p>
  <br>

  <form align="center" action="comprobar_usuario.php">
        Nombre:
        <input type="text" name="nombre_usuario">
        </br>
        Contraseña:
        <input type="text" name="contraseña_usuario">
        <br/><br/>
        <input type="submit" value="Ingresar">
  </form>

  <br>
  <br>
  <br>

  <form align="center" action="nueva_sesion.php">
      ¡¿No se ha creado una sesión?! Registrese acá
    <input type="submit" value="Registrase">
  </form>