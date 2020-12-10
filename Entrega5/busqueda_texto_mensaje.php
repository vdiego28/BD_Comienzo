<?php include('../templates/header.html');   ?>

<body>
    <?php 
    # Aquí deberían manejar los casos en los que no se ingrese información en alguno de los inputs del form, por simplicidad  
    $desired = explode(",", $_GET['desired']);
    $required = explode(",",$_GET['required']);
    $forbidden =  explode(",", $_GET['forbidden']);
    $userId =  $_GET['ID'];

    $data = array(
        'desired' => $desired,
        'required' => $required,
        'forbidden' => $forbidden,
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
    $result = file_get_contents( 'https://miApi.herokuapp.com/text-search', false, $context );
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
                    $ch = curl_init();
                    $url = 'https://miApi.herokuapp.com/users/' . $message['receptant'];
                    curl_setopt($ch, CURLOPT_URL, $url);
                    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                    $res = curl_exec($ch);
                    curl_close($ch);
                    $receptant = json_decode($res, true);
        
                    echo "<tr> <td>" .  $message['date'] . "</td>";
                    echo "<td>" . $message['lat'] . "</td>";
                    echo "<td>" . $message['long'] . "</td>";
                    echo "<td>" . $receptant["name"] . "</td>";
                    echo "<td>" . $message['mid'] . "</td>";
                    echo "<td>" . $message['message'] . "</td> </tr>";
            }
            ?>
            </tr>
        </table>
    </div>

<?php include('../templates/footer.html'); ?>