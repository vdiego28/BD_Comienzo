<?php include('templates/header.html'); ?>

<body>
<?php
    require("config/conexion.php");

    $nombre = $_POST["nombre_usuario"];
    $contrasena = $_POST["contraseña_usuario"];

    $query = "SELECT nombre FROM Usuarios WHERE nombre = '%nombre%' AND contrasena = '%contrasena%'";
    $result = $db -> prepare($query);
    $result -> execute();
    $nombres = $result -> fetchAll();

    list($total) = mysql_fetch_row($result);

    if ($total==0) {

        <p> Lo siento pero no existe usuario con esta contraseña </p>
        <br>
        <form align="center" action="nueva_sesion.php" method="post">
        <br/><br/>
        <input type="submit" value="Registrarse">
        </form>
    }

    if ($total!=0) {
        <p> Todo en orden, puede ingresar </p>
        <form align="center" action="index.php" method="post">
        <br/></br>
        <input type="submit" value="Ingresar">
        </form>
    }

</body>
</html>