function set_text() {
    /**
     * set the <textarea> with the cookie created by send_tts.js
     */

    // get the document cookie and place it inside conclusion
    var conclusion = document.cookie;
    
    // if the conclusion is empty, place the default text
    if (conclusion == '') {
        conclusion = 'Waiting for input...';
    } else {
        // else place the cookie text into the <textarea>
        $('textarea').val(conclusion);

        // clear the cookie
        document.cookie = '';
    }
}