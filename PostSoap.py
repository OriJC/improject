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


def MessageForPost(action, story, query=None):
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


def DecypherResponse(response, use_case):
    '''
    Inputs the string value of the xml message
    Outputs:
    - runtime: <Str> The runtime for the query
    - message: <Str> The corresponding message for the query
    - reason: <List> The list that contains one or more [str / list]
            that has the reason for said message 
    '''
    root = ET.fromstring(response)
    reply = (root[0])[0] # Get the <race:Reply> tag from RACE
    runtime = reply.find('race:Runtime', ns).text
    message, reason = "", []

    if use_case == "check_consistency":
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
        proofs = reply.findall('race:Proof', ns)
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
                reason.append(axiom_combo)

    return runtime, message, reason
