/**
 * some common functions required for all/partial html
 */

function insertAfter(newNode, existingNode) {
    /**
     * Insert newNode after existingNode  
     * @param {Object} newNode is being inserted
     * @param {Object} existingNode is the node that is 
     * being inserted after 
     */
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

function create_button(class_name, id_name, text) {
    /**
     * returning a button
     * @param {String} class_name is the class of the element
     * @param {String} id_name is the id of the element
     * @param {String} text is the inner text of the element
     * @returns {HTMLButtonElement}
     */
    let element = document.createElement("button");
    element.setAttribute('type', 'button');
    element.setAttribute('class', class_name);
    element.setAttribute('id', id_name);
    element.innerHTML = text;

    return element;
}