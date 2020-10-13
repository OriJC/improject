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

ns = {
    'env': "http://schemas.xmlsoap.org/soap/envelope/",
    'race': "http://attempto.ifi.uzh.ch/race"
}


def MessageForPost(action, story, query=None):
    body = ""
    if action == "check_consistency":
        body = (
            f"\t\t\t<race:Axioms>{story}</race:Axioms>\n"
            f"\t\t\t<race:Mode>{action}</race:Mode>\n"
        )
    elif action == "proof":
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


def DecypherResponse(response):
    root = ET.fromstring(response)
    respect = root.findall('race:Reply', ns)
    print(respect)
    # have not finished
