FAQS = {

    "delivery":
        "Delivery takes 3-5 business days.",

    "refund":
        "Refunds are processed within 7 days.",

    "support":
        "Customer support is available 24/7."
}


def search_faq(question):

    q = question.lower()

    for key, answer in FAQS.items():

        if key in q:
            return answer

    return None