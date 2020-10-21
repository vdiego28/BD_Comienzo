<?php include('templates/header.html');   ?>

<!--
Un gran agradecimiento a los ayudantes,
toda la estructura y parte del codigo fue inspirado
de la ayudantia.
-->

<body>
  
  <h1 align="center">Puertos e Instalaciones </h1>
  <p style="text-align:center;">Aquí se podra encontrar información sobre puertos.</p>
  <br>
  
  <form align="center" action="nueva_sesion.php" method="post">
    <br/><br/>
    <input type="submit" value="crear sesion">
  </form>

  <br>

  <h3 align="center"> Todos los puertos junto la ciudad a la que son asignados.</h3>

  <form align="center" action="consultas/consulta_puertos_con_ciudades.php" method="post">
    <br/><br/>
    <input type="submit" value="Buscar">
  </form>
  
  <br>
  <br>
  <br>

  <h3 align="center"> Todos los jefes de las instalaciones del puerto con nombre ‘Mejillones’.</h3>

  <form align="center" action="consultas/consulta_jefes_de_mejillones.php" method="post">
    <br/><br/>
    <input type="submit" value="Buscar">
  </form>
  
  <br>
  <br>
  <br>

  <h3 align="center"> Todos los puertos que tienen al menos un astillero.</h3>

  <form align="center" action="consultas/consulta_puertos_con_astilleros.php" method="post">
    <input type="submit" value="Buscar">
  </form>
  <br>
  <br>
  <br>

  <h3 align="center"> La edad promedio de los trabajadores de cada puerto.</h3>

  <form align="center" action="consultas/consulta_edad_promedio.php" method="post">
    Altura Mínima:
    <input type="text" name="altura">
    <br/><br/>
    <input type="submit" value="Buscar">
  </form>
  <br>
  <br>
  <br>

  <h3 align="center"> El puerto que ha recibido mas barcos en Agosto del 2020.</h3>

  <form align="center" action="consultas/consulta_puerto_con_mas_barcos.php" method="post">
    <br/><br/>
    <input type="submit" value="Buscar">
  </form>
  <br>
  <br>
  <br>

  <h3 align="center">Todas las veces en que el barco ‘Calypso’ ha atracado en ‘Arica’.</h3>

  <form align="center" action="consultas/consulta_barco_calypso.php" method="post">
    <br/><br/>
    <input type="submit" value="Buscar">
  </form>
  <br>
  <br>
  <br>


</body>
</html>
