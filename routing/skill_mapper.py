def get_required_skill(intent):

    mapping = {

        "appointment": "appointments",

        "complaint": "technical",

        "billing": "billing",

        "internet": "network"
    }

    return mapping.get(
        intent,
        "technical"
    )