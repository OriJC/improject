function send_tts() {
    /* send the data from conclusion to OwlToSpeech.html */
    var conclusion_data = "";

    var conclusion_nodes = document.getElementsByClassName("conclusion_node");
    for (var i = 0; i < conclusion_nodes.length; i++) {
        conclusion_data += conclusion_nodes[i].textContent + ' ';
    }
    document.cookie = conclusion_data + ";secure";
    location.href = "/TTS";
}