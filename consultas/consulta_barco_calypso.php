<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php"); #Llama a conexión, crea el objeto PDO y obtiene la variable $db

  
  $query = "SELECT Permisos_carga_descarga.fecha_atraque 
  FROM Permisos_carga_descarga, Instalaciones, Barcos
  WHERE Barcos.nombre_barco = 'Calypso' 
  AND Instalaciones.nombre_puerto = 'Arica' 
  AND Permisos_carga_descarga.patente_barco = Barcos.patente_barco
  AND Permisos_carga_descarga.id_instalacion = Instalaciones.id_instalacion
  UNION
  SELECT Permisos_astillero.fecha_atraque 
  FROM Permisos_astillero, Instalaciones, Barcos
  WHERE Barcos.nombre_barco = 'Calypso' 
  AND Instalaciones.nombre_puerto = 'Arica' 
  AND Permisos_astillero.patente_barco = Barcos.patente_barco
  AND Permisos_astillero.id_instalacion = Instalaciones.id_instalacion;";


  
  $result = $db -> prepare($query);
  $result -> execute();
  $fecha = $result -> fetchAll(); #Obtiene todos los resultados de la consulta en forma de un arreglo
  ?>

  <table>
    <tr>
      <th>Fecha atraque</th>

    </tr>
  <?php
  foreach ($fecha as $p) {
    echo "<tr> <td>$p[0]</td>  </tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>
