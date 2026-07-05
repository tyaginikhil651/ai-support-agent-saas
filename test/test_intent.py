from intent_classifier import detect_intent


tests = [

    "Need engineer tomorrow",

    "Book appointment",

    "Internet not working",

    "My service is down",

    "Check ticket TKT123",

    "What are your timings?",

    "Hello"
]

for t in tests:

    print("\nINPUT:", t)

    print(
        "INTENT:",
        detect_intent(t)
    )