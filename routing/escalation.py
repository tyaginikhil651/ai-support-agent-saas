def needs_escalation(ticket):

    if ticket["priority"] == "High":
        return True

    return False

def estimate_resolution(priority):

    if priority == "High":
        return "2 Hours"

    if priority == "Medium":
        return "8 Hours"

    return "24 Hours"