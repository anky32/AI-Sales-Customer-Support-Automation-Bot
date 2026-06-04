def qualify_lead(budget):

    budget = int(budget)

    if budget >= 5000:
        return 90

    elif budget >= 2000:
        return 70

    else:
        return 40