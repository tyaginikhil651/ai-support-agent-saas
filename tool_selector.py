from intent_classifier import detect_intent


def choose_tool(message):

    intent = detect_intent(message)

    return {
        "tool": intent,
        "input": message
    }