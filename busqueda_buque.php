<?php include('../templates/header.html');   ?>

<body>
    <?php 
    # Aquí deberían manejar los casos en los que no se ingrese información en alguno de los inputs del form, por simplicidad  
    $palabras_clave = $_GET['palabras_clave'];
    $fecha_termino = $_GET['fecha_termino'];
    $fecha_inicio =  $_GET['fecha_inicio'];
    $userId =  $_GET['ID'];

    $data = array(
        'palabras_clave' => $palabras_clave,
        'fecha_termino' => $fecha_termino,
        'fecha_inicio' => $fecha_inicio,
        'userId' => intval($userId)
    );


    $options = array(
        'http' => array(
        'method'  => 'GET',
        'content' => json_encode( $data ),
        'header'=>  "Content-Type: application/json\r\n" .
                    "Accept: application/json\r\n"
        )
    );
    
    $context  = stream_context_create( $options );
    $result = file_get_contents( 'https://still-hollows-62050.herokuapp.com/busqueda-buque', false, $context );
    $response = json_decode($result, true);

    ?>

    <div class="container">
        <table>
            <thead>
            <tr>
                <th>Fecha</th>
                <th>Latitud</th>
                <th>Longitud</th>
                <th>Enviado a</th>
                <th>ID mensaje</th>
                <th>Mensaje</th>
            </tr>
            </thead>
            <tr>
            <?php foreach ($response as $message){
                    # Aquí se añade un ejemplo en el que se obtiene el usuario que recibe el mensaje
        
                    echo "<tr> <td>" .  $message['date'] . "</td>";
                    echo "<td>" . $message['lat'] . "</td>";
                    echo "<td>" . $message['long'] . "</td>";
                    echo "<td>" . $message["sender"] . "</td>";
                    echo "<td>" . $message['mid'] . "</td>";
                    echo "<td>" . $message['message'] . "</td> </tr>";
            }
            ?>
            </tr>
        </table>
    </div>

<?php include('../templates/footer.html'); ?>