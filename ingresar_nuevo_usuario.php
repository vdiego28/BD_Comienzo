<?php include('templates/header.html'); ?>

<body>
<?php
    require("config/conexion.php");

    $nombre = $_POST["nombre_usuario"];
    $edad = $_POST["edad_usuario"];
    $pasaporte = $_POST["n_pasaporte_usuario"];
    $nacionalidad = $_POST["nacionalidad_usuario"];
    $contraseña = $_POST["contraseña_usuario"];

    $query = "SELECT nombre FROM Usuarios WHERE nombre = '%nombre%'";
    $result = $db -> prepare($query);
    $result -> execute();
    $nombres = $result -> fetchAll();

    list($total) = mysql_fetch_row($result);
    if ($total==0) {
        <form align="center" action="index.php" method="post">
            <br/></br>
            <input type="submit" value="Ingresar">
        </form>
    }
    if ($total!=0) or (strlen($contraseña)<1) or (strlen($nacionalidad)<1) or ($edad<1) or ($pasaporte<1) {
        <form align="center" action="nueva_sesion.php" method="post">
            <br/></br>
            <input type="submit" value="Regresar">
        </form>
    }

</body>
</html>