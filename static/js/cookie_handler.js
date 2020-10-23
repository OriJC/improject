function set_text() {
    var conclusion = '';
    conclusion = document.cookie;
    if (conclusion == '') {
        conclusion = 'Waiting for input...';
    }
    $('textarea').val(conclusion);
    document.cookie = '';
}