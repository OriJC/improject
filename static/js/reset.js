function reset(text_remain=true) {
    if (!text_remain){
        $('textarea').val('');
    }

    if (document.getElementById('output')) {
        document.getElementById('output').remove();
    }
    
    if (document.getElementById("spinner")) {
        document.getElementById('spinner').remove();
    }

    if (document.getElementById("send_tts")) {
        document.getElementById("send_tts").remove();
    }
}