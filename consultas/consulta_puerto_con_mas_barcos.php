<?php include('../templates/header.html');   ?>

<body>

<?php
  #Llama a conexión, crea el objeto PDO y obtiene la variable $db
  require("../config/conexion.php");

	

 	$query = "SELECT Puertos.nombre_puerto, COUNT(Puertos.nombre_puerto) AS recibidos
   FROM Puertos, Instalaciones, Permisos_Carga_Descarga, Permisos_Astillero
   WHERE Puertos.nombre_puerto = Instalaciones.nombre_puerto 
   AND (Permisos_Carga_Descarga.id_instalacion = Instalaciones.id_instalacion 
   OR Permisos_Astillero.id_instalacion = Instalaciones.id_instalacion) 
   AND (EXTRACT(MONTH FROM Permisos_Astillero.fecha_atraque) = 8 
   OR EXTRACT(MONTH FROM Permisos_carga_descarga.fecha_atraque) = 8) 
   GROUP BY Puertos.nombre_puerto 
   ORDER BY recibidos DESC LIMIT 1;";
	$result = $db -> prepare($query);
	$result -> execute();
	$puerto = $result -> fetchAll();
  ?>

	<table>
    <tr>
      <th>Nombre puerto</th>
      <th>numero de recividos</th>
      
    </tr>
  <?php
	foreach ($puerto as $resultado) {
  		echo "<tr> <td>$resultado[0]</td> <td>$resultado[1]</td>  </tr>";
	}
  ?>
	</table>

<?php include('../templates/footer.html'); ?>
