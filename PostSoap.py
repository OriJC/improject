"""Provides support for RACE messages"""

import xml.etree.ElementTree as ET

head = (
    f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\n"
    f"<env:Envelope xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\">\n"
    f"\t<env:Body>\n"
    f"\t\t<race:Request xmlns:race=\"http://attempto.ifi.uzh.ch/race\">\n"
)

tail = (
    f"\t\t</race:Request>\n"
    f"\t</env:Body>\n"
    f"</env:Envelope>"
)

# Namespace for POST
ns = {
    'env': "http://schemas.xmlsoap.org/soap/envelope/",
    'race': "http://attempto.ifi.uzh.ch/race"
}

def remove_same_sentence(sentences: list) -> list:
    '''
    @param: <list> of sentences
    @return: <list>
    {empty list | list is empty}
    {original list | only one object}
    {list with unique objects | otherwise} 
    ''' 
    if len(sentences) == 0:
        return []
    elif len(sentences) == 1:
        return sentences
    else:
        return list(dict.fromkeys(sentences))

def query_to_conclusion(query: str, changes: list) -> list:
    '''
    @param:
    - query: <str>
    - conclusion: <list>
    @return: <list> of <str>
    '''
    conclusion = []

    # Creating all the tails of the conclusion
    # TODO: Handle more types of substitution
    query = query.lower().replace('?', '.')
    if query.find("is somebody who") == 0:
        answer_tail = query.replace("is somebody who", '')
    elif query.find("who") == 0:
        answer_tail = query.replace("who", '')

    # Remove all the "... (at least x) ..."
    # Place the answer_tail into conclusion
    for change in changes:
        if change.find("(at least ") == -1:
            change_split = change.split()
            target = change_split[len(change_split) - 1]
            conclusion.append(target + answer_tail)
            
    # Return list
    return conclusion


def MessageForPost(action: str, story: str, query: str=None) -> str:
    '''
    Generate the POST message required
    '''
    body = ""
    if action == "check_consistency":
        body = (
            f"\t\t\t<race:Axioms>{story}</race:Axioms>\n"
            f"\t\t\t<race:Mode>{action}</race:Mode>\n"
        )
    elif action == "prove":
        body = (
            f"\t\t\t<race:Axioms>{story}</race:Axioms>\n"
            f"\t\t\t<race:Theorems>{query}</race:Theorems>\n"
            f"\t\t\t<race:Mode>{action}</race:Mode>\n"
        )
    elif action == "answer_query":
        body = (
            f"\t\t\t<race:Axioms>{story}</race:Axioms>\n"
            f"\t\t\t<race:Theorems>{query}</race:Theorems>\n"
            f"\t\t\t<race:Mode>{action}</race:Mode>\n"
        )

    post = (
        f"{head}"
        f"{body}"
        f"{tail}"
    )
    return post


def DecypherResponse(response: str, use_case: str, query: str):
    '''
    Inputs the string value of the xml message
    Outputs:
    - runtime: <Str> The runtime for the query
    - message: <Str> The corresponding message for the query
    - reason: <List> The list that contains one or more [str / list]
            that has the reason for said message 
    '''
    root = ET.fromstring(response)
    reply = (root[0])[0]  # Get the <race:Reply> tag from RACE
    runtime, message, reason, conclusion = '0', "", [], []
    if reply.find('race:Runtime', ns) is not None:
        runtime = reply.find('race:Runtime', ns).text

    if reply.find('race:Message', ns) is not None:
        '''
        error handling
        ---
        the error would normally accompany with the <race:Message> tag
        '''
        message_tag = reply.findall('race:Message', ns)

        if len(message_tag) == 1:
            '''
            if there is only one message
            '''
            errors = reply.find('race:Message', ns)
            message = "Message (Probably should fix it)"
            reason.append(errors.find('race:Importance', ns).text.upper() + ": " + errors.find('race:Type', ns).text)
            if errors.find('race:SentenceID', ns).text is not None:
                reason.append("Sentence ID: " + errors.find('race:SentenceID', ns).text)
            reason.append("Subject: " + errors.find('race:Subject', ns).text)
            reason.append("Description: " + errors.find('race:Description', ns).text)
        else:
            '''
            if there are multiple messages
            '''
            message = "Multiple messages (Probably should fix them)"
            message_tag = reply.findall('race:Message', ns)
            for each_message in message_tag:
                message_box = []
                message_box.append(each_message.find('race:Importance', ns).text.upper() + ": " + each_message.find('race:Type', ns).text)
                if each_message.find('race:SentenceID', ns).text is not None:
                    message_box.append("Sentence ID: " + each_message.find('race:SentenceID', ns).text)
                message_box.append("Subject: " + each_message.find('race:Subject', ns).text)
                message_box.append("Description: " + each_message.find('race:Description', ns).text)
                reason.append(message_box)

    elif use_case == "check_consistency":
        inconsistent_axioms = []
        proofs = reply.find('race:Proof', ns)

        if proofs is None:
            message = "Consistent"
        else:
            message = "Not consistent"
            used_axioms = proofs[0]
            for axioms in used_axioms:
                inconsistent_axioms.append(axioms.text)

        reason = inconsistent_axioms

    elif use_case == "prove":
        '''
        Am not sure what does
        <race:UsedAuxAxioms/>
        ---
        axiom_combo: list of all axioms inside one <race:UsedAxioms> tag
        ---
        - Output all the axioms required to examine the query into reason
        - Place the corresponding message into var:message
        '''

        proofs = reply.findall('race:Proof', ns)
        if len(proofs) == 0:
            message = "Not proven"
            reason_not = reply.find("race:WhyNot", ns)
            for rn in reason_not:
                reason.append(rn.text)
        else:
            message = "Proved"
            for proof in proofs:
                used_axioms = proof.find("race:UsedAxioms", ns)
                axiom_combo = []
                for axioms in used_axioms:
                    axiom_combo.append(axioms.text)
                reason.append(axiom_combo)

    elif use_case == "answer_query":
        '''
        let substitution happen automatically
        '''
        proofs = reply.findall('race:Proof', ns)
        changes = []
        if len(proofs) == 0:
            message = "Cannot be answered"
            reason_not = reply.find("race:WhyNot", ns)
            for rn in reason_not:
                reason.append(rn.text)
        else:
            message = "Answered"
            for proof in proofs:
                used_axioms = proof.find("race:UsedAxioms", ns)
                axiom_combo = []
                for axioms in used_axioms:
                    axiom_combo.append(axioms.text)
                    if axioms.text.find("Substitution:") == 0:
                        # Provide automatic substitution
                        changes.append(axioms.text)
                reason.append(axiom_combo)
            changes = remove_same_sentence(changes)
            ''' add sub fx '''
            conclusion = query_to_conclusion(query, changes)

    return runtime, message, reason, conclusion
