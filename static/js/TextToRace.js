function uploadTextTTR() {
    var axioms = document.getElementById("axioms").value;
    axioms = axioms.replace(/\n/g, " ");
    var query = document.getElementById("query").value;
    var UseCase = document.getElementById("UseCase").value;
    var up = new FormData();

    up.append('axioms', axioms);
    up.append('query', query);
    up.append('UseCase', UseCase);

    $.ajax({
        type: 'POST',
        url: '/TTRA',
        data: up,
        processData: false,
        contentType: false
    }).done(function (data) {
        console.log("Text to Race upload successful!");
        if (data['result'] == true)
            console.log("Reload successfully!!!");
        else
            console.log("TTR Failed");

    }).fail(function (jqXHR, textStatus, error) {
        console.log("Upload text failed!");
    });

}