<?php include('../templates/header.html');   ?>

<body>
<?php
  #Llama a conexión, crea el objeto PDO y obtiene la variable $db
  require("../config/conexion.php");

  

 	$query = "SELECT Personal.nombre, Personal.rut 
   FROM Personal, Instalaciones 
   WHERE Instalaciones.nombre_puerto = 'Mejillones' 
   AND Personal.rut = Instalaciones.rut_jefe;";
	$result = $db -> prepare($query);
	$result -> execute();
	$Jefes = $result -> fetchAll();
  ?>

	<table>
    <tr>
      <th>Personal</th>
      <th>rut</th>
    </tr>
  <?php
	foreach ($Jefes as $resultados) {
  		echo "<tr><td>$resultados[0]</td><td>$resultados[1]</td></tr>";
	}
  ?>
	</table>

<?php include('../templates/footer.html'); ?>
