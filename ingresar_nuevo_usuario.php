<?php include('templates/header.html'); ?>

<body>
<p> Comprobando nueva sesion. </p>
<?php
    require("config/conexion.php");

    $nombre = $_POST["nombre_usuario"];
    $edad = $_POST["edad_usuario"];
    $pasaporte = $_POST["n_pasaporte_usuario"];
    $nacionalidad = $_POST["nacionalidad_usuario"];
    $contrasena = $_POST["contraseña_usuario"];

    $query = "SELECT nombre FROM Usuarios WHERE nombre = '%nombre%'";
    $result = $db -> prepare($query);
    $result -> execute();
    $nombres = $result -> fetchAll();

    list($total) = mysql_fetch_row($result);
    if (($total!=0) or (strlen($contrasena)<1) or (strlen($nacionalidad)<1) or ($edad<1) or (strlen($pasaporte)<1)):
        echo "<p> Existe un error con sus datos, intente otra vez. </p>"; ?>
        <form align="center" action="nueva_sesion.php" method="post">
        <br/></br>
        <input type="submit" value="Regresar">
        </form>
    <?php endif;

    if ($total==0):
        $agregar = "INSERT INTO usuarios VALUES ('%nombre%', '%edad%', '%pasaporte%','%nacionalidad%', '%contrasena%');";
        $result_crate = $db -> prepare($query);
        $result_create -> execute();
        echo "<p> Se creó el usuario con éxito. </p>"; ?>
        <br>
        <form align="center" action="index.php" method="post">
        <br/><br/>
        <input type="submit" value="ingresar">
        </form>
    <?php endif; ?>

</body>
</html>