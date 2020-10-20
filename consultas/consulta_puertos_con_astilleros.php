<?php include('../templates/header.html');   ?>

<body>

<?php
  #Llama a conexión, crea el objeto PDO y obtiene la variable $db
  require("../config/conexion.php");

	

 	$query = "SELECT DISTINCT Puertos.nombre_puerto 
   FROM Puertos, Instalaciones 
   WHERE Puertos.nombre_puerto = Instalaciones.nombre_puerto 
   GROUP BY Puertos.nombre_puerto;";
	$result = $db -> prepare($query);
	$result -> execute();
	$puertos = $result -> fetchAll();
  ?>

	<table>
    <tr>
      <th>Nombre puerto</th>
    </tr>
  <?php
	foreach ($puertos as $resultado) {
  		echo "<tr> <td>$resultado[0]</td> </tr>";
	}
  ?>
	</table>

<?php include('../templates/footer.html'); ?>
