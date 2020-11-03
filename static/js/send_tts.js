function send_tts() {
    /* send the data from TextToRace.html/conclusions to OwlToSpeech.html */
    var conclusion_data = "";
    
    // get the object <conclusion_node> from ttr 
    var conclusion_nodes = document.getElementsByClassName("conclusion_node");
    
    // for every object inside <conclusion_node> get the text
    for (var i = 0; i < conclusion_nodes.length; i++) {
        conclusion_data += conclusion_nodes[i].textContent + ' ';
    }
    // create a cookie data for the conclusions
    document.cookie = conclusion_data + ";secure";

    // turn the page to <url>/TTS
    location.href = "/TTS";
}