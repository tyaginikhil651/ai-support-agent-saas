def router(state):

    intent = state.get(
        "intent",
        ""
    )

    if intent == "appointment":
        return "appointment"

    if intent == "complaint":
        return "complaint"

    return "complaint"