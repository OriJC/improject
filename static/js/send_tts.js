function send_tts() {
    /* send the data from conclusion to OwlToSpeech.html */
    var send_file = new FormData();
    var conclusion_data = "";

    var conclusion_nodes = document.getElementsByClassName("conclusion_node");
    for (var i = 0; i < conclusion_nodes.length; i++) {
        conclusion_data += conclusion_nodes[i].textContent + ' ';
    }

    send_file.append('conclusion', conclusion_data);

    $.ajax({
        type: 'POST',
        url: '/TTS', 
        data: send_file,
        processData: false,
        contentType: false,
    })
}