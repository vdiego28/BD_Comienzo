<?php include('templates/header.html'); ?>
<?php $id_usuario = $_GET['ID']; ?>
        <h1>Aquí hacemos Requests a la API</h1>
        <h3>Ingrese los campos que desea</h3>
        <div class="api-requester">
            <form align="center" action="busqueda_texto_mensaje.php" method="get">
                <input type="hidden" name="ID" value="<?php echo $id_usuario ?>">
                <label for="desired">Busqueda Simple:</label><br>
                <input id="desired"> type="text" name="desired">
                <label for="required">Busqueda Exacta:</label><br>
                <input id="required" type="text" name="required">
                <label for="forbidden">No buscar:</label><br>
                <input id="forbidden" type="text" name="forbidden">
            <input type="submit" value="Buscar">
            </form>
        </div>
    </body>
</html>