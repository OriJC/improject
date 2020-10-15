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
        output = reset_output();
        runtime = create_list_item("Runtime: " + data['runtime']);
        message = create_list_item("Message: " + data['message']);
        output.appendChild(runtime);
        output.appendChild(message);

        reason_list = data['reason'];
        if (Array.isArray(reason_list) && reason_list.length) {
            /* First create a big list */
            /* output
             * |- runtime
             * |- message
             * |- reason
             */
            reason = document.createElement("ul");
            reason.setAttribute("id", "reason");
            reason.setAttribute("class", "list-group");
            reason.setAttribute("style", "padding-top: 0.5em;");

            title_for_reason = create_list_item('Reasons:', bold = true);
            reason.append(title_for_reason);

            if (Array.isArray(reason_list[0])) {
                /* if reason_list has a list within a list */
                /* |- reason
                 *    |- submodule 1
                 */
                reason_list.forEach(function (item, index, array) {

                    submodule = document.createElement('ul');
                    submodule.setAttribute("id", "submodule");
                    submodule.setAttribute("class", "list-group");
                    submodule.setAttribute("style", "padding-top: 0.5em;");

                    display_index = index + 1;
                    title_for_submodule = create_list_item('Submodule ' + display_index + ":", bold = true);
                    submodule.append(title_for_submodule);

                    item.forEach(function (item, index, array) {
                        /* |- reason
                         *    |- submodule 1
                         *       |- reason_nodes 1
                         */
                        reason_nodes = create_list_item(item);
                        submodule.append(reason_nodes);
                    })

                    reason.append(submodule);
                })
            } else {
                /* if reason_list has only a list */
                /* |- reason
                 *    |- reason_nodes 1
                 */
                title_for_reason = create_list_item('Reasons:', bold = true);
                output.append(title_for_reason);
                reason_list.forEach(function (item, index, array) {
                    reason_nodes = create_list_item(item);
                    reason.append(reason_nodes);
                })
            }
            output.append(reason);
        }

        /* refreshing the answers */
        current_element = document.getElementById("ttrpart");
        insertAfter(output, current_element);
    }).fail(function (jqXHR, textStatus, error) {
        if (document.getElementById("output")) {
            document.getElementById("output").remove();
        }
        output = reset_output();
        output.appendChild(document.createTextNode("Error getting data from the server"));
        current_element = document.getElementById("ttrpart");
        insertAfter(output, current_element);
    });

}

function reset_output() {
    if (document.getElementById("output")) {
        document.getElementById("output").remove();
    }
    output = document.createElement("ul");
    output.setAttribute("id", "output");
    output.setAttribute("class", "list-group");
    return output;
}

function create_list_item(text_content, bold = false) {
    list_item = document.createElement("li");
    list_item.textContent = text_content;
    list_item.setAttribute("class", "list-group-item");
    if (bold) {
        list_item.setAttribute("style", "font-weight: bold;");
    }
    return list_item;
}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}