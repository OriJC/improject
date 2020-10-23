function send_tts() {
    /* send the data from conclusion to OwlToSpeech.html */
    // TODO: make sure a way to catch if there is no conclusion node
    // var send_file = new FormData();
    var conclusion_data = "";

    var conclusion_nodes = document.getElementsByClassName("conclusion_node");
    for (var i = 0; i < conclusion_nodes.length; i++) {
        conclusion_data += conclusion_nodes[i].textContent + ' ';
    }
    document.cookie = conclusion_data + ";secure";
    location.href = "/TTS";
    // send_file.append('conclusion', conclusion_data);

    /*
    $.ajax({
        type: 'POST',
        url: '/TTR-redirect',
        data: send_file,
        processData: false,
        contentType: false,
    }).done(function () {
        // location.href = "/TTS";
    });
    */
}