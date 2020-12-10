<?php include('templates/header.html'); ?>

<body>
    <h1 align='center'> Crear Usuario </h1>
    <p style="text-align:center";> Ingrese sus datos para crear un nuevo usuario. </p>

    <br>

    <form align="center" action="ingresar_nuevo_usuario.php">
        Nombre:
        <input type="text" name="nombre_usuario">
        </br>
        Edad:
        <input type="number" name="edad_usuario">
        <br/></br>
        Numero de Pasaporte:
        <input type="text" name="n_pasaporte_usuario">
        <br/></br>
        Nacionalidad:
        <input type="text" name="nacionalidad_usuario">
        <br/></br>
        Contraseña:
        <input type="text" name="contraseña_usuario">
        <br/></br>
        <input type="submit" value="Crear">
    </form>
    <br>

</body>