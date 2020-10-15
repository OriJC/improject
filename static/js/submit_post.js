function submit_post() {
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
        /*
        Accept the data output and print it at the bottom of the page
        */
        if (document.getElementById("output")) {
            document.getElementById("output").remove();
        }
        output = document.createElement("div");
        output.setAttribute("id", "output");
        output.appendChild(document.createTextNode("Runtime: " + data['runtime']));
        output.appendChild(document.createTextNode("Message: " + data['message']));
        current_element = document.getElementById("ttrpart");
        insertAfter(output, current_element);
    }).fail(function (jqXHR, textStatus, error) {
        // something
    });

}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}