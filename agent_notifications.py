def notify_agent(
    agent,
    ticket_id,
    issue
):

    print(
        f"""
        New Ticket Assigned

        Agent: {agent['name']}

        Ticket: {ticket_id}

        Issue: {issue}
        """
    )