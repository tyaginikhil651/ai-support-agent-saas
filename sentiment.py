def detect_sentiment(message: str):

    msg = message.lower()

    negative_words = [
        "bad", "worst", "angry", "not working",
        "issue", "problem", "hate", "complain"
    ]

    positive_words = [
        "good", "great", "thanks", "awesome", "perfect"
    ]

    score = 0

    for w in positive_words:
        if w in msg:
            score += 1

    for w in negative_words:
        if w in msg:
            score -= 1

    return score