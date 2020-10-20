<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php"); #Llama a conexión, crea el objeto PDO y obtiene la variable $db

  
  $query = "SELECT Puertos.nombre_puerto, Avg(personal.edad) 
  FROM Puertos, Personal, Instalaciones
  WHERE Personal.id_instalacion = Instalaciones.id_instalacion 
  AND Instalaciones.nombre_puerto = Puertos.nombre_puerto 
  GROUP BY Puertos.nombre_puerto;";
  
  $result = $db -> prepare($query);
  $result -> execute();
  $edad = $result -> fetchAll(); #Obtiene todos los resultados de la consulta en forma de un arreglo
  ?>

  <table>
    <tr>
      <th>Nombre de Puerto</th>
      <th>Edad</th>
    </tr>
  <?php
  foreach ($edad as $p) {
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> </tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>
