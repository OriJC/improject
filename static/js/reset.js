function reset(text_remain=true) {
    /**
     * reset the page elements for the page TextToRace.html
     * @param {boolean} text_remain whether to remain the text in the <textarea>
     */

    // if the text_remain is set to true then clear the text area
    if (!text_remain){
        $('textarea').val('');
    }

    // remove <output> <spinner> <send_tts>
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