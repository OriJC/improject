function reset_output() {
    /* To remove the outputs if any
     * Return a element ul 
     */
    reset();

    var output = document.createElement("ul");
    output.setAttribute("id", "output");
    output.setAttribute("class", "list-group");
    return output; 
}

function create_list_item(text_content, bold=false, success=false) {
    /* Create a list item in Element for DOM */
    var list_item = document.createElement("li");
    list_item.textContent = text_content;
    if (success) {
        list_item.setAttribute("class", "list-group-item list-group-item-success");
    } else {
        list_item.setAttribute("class", "list-group-item");
    }
    if (bold) {
        /* Set the item as bold */
        list_item.setAttribute("style", "font-weight: bold;");
    }
    return list_item;
}

function create_parent_item(element_type, id, class_type){
    var node = document.createElement(element_type);
    node.setAttribute("id", id);
    node.setAttribute("class", class_type);

    return node;
}

function insertAfter(newNode, existingNode) {
    /* Insert object after existingNode */
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

function submit_post() {
    /* Get the values in textarea and button */
    var axioms = document.getElementById("axioms").value;
    axioms = axioms.replace(/\n/g, " ");
    var query = document.getElementById("query").value;
    var UseCase = document.getElementById("UseCase").value;
    var up = new FormData();

    /* Appending data */
    up.append('axioms', axioms);
    up.append('query', query);
    up.append('UseCase', UseCase);

    /* Create the loading animation */
    loading_animation = create_parent_item(element_type="div", id="spinner", class_type='spinner-border ml-auto');
    loading_animation.setAttribute('role', "status");
    if (document.getElementById('send_tts')) {
        current_element = document.getElementById('send_tts');
    } else {
        current_element = document.getElementById("reset");
    }
    insertAfter(loading_animation, current_element);

    /* Posting data to app.py */
    $.ajax({
        type: 'POST',
        url: '/TTR',
        data: up,
        processData: false,
        contentType: false
    }).done(function (data) {
        /* Accept the data output and print it at the bottom of the page */
        output = reset_output();
        runtime = create_list_item("Runtime: " + data['runtime'] + " second(s)");
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
        
            reason = create_parent_item("ul", "reason", "list-group");
            reason.setAttribute("style", "padding-top: 0.5em;");

            title_for_reason = create_list_item('Reasons:', bold=true);
            reason.append(title_for_reason);

            if (Array.isArray(reason_list[0])) {
                /* if reason_list has a list within a list */
                /* |- reason
                 *    |- submodule 1
                 */
                reason_list.forEach(function (item, index, array) {

                    submodule = create_parent_item(element_type='ul', id='submodule', class_type='list-group');
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
                reason_list.forEach(function (item, index, array) {
                    reason_nodes = create_list_item(item);
                    reason.append(reason_nodes);
                })
            }

            output.append(reason);
        }

        conclusion_list = data['conclusion'];
        if (Array.isArray(conclusion_list) && conclusion_list.length) {
            conclusions = create_parent_item(element_type='ul', id='conclusions', class_type='list-group');
            conclusions.setAttribute("style", "padding-top: 0.5em;");
            
            conclusion_title = create_list_item("Conclusion", bold=true, success=true);
            conclusions.append(conclusion_title);

            conclusion_list.forEach(function(item) {
                conclusion_node = create_list_item(item);
                conclusion_node.setAttribute('class', 'list-group-item conclusion_node');
                conclusions.append(conclusion_node);
            })

            output.append(conclusions);

            // Create a button if there is a conclusion
            send_button = create_parent_item(element_type='button', id='send_tts', class_type='btn btn-success');
            send_button.setAttribute("onclick", "send_tts();");
            send_button.textContent = "Speak";

            insertAfter(send_button, document.getElementById('reset'));
        }

        /* refreshing the answers */
        current_element = document.getElementById("ttrpart");
        if (document.getElementById('spinner')) {
            document.getElementById('spinner').remove();
        }
        insertAfter(output, current_element);
    }).fail(function (jqXHR, textStatus, error) {
        /* If the server somehow didn't succesfully send the data */
        reset();

        output = reset_output();
        output.appendChild(document.createTextNode("Error getting data from the server"));
        current_element = document.getElementById("ttrpart");
        insertAfter(output, current_element);
    });

}