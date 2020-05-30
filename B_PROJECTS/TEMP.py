def make_change(c):
    change_values = [25, 10, 5, 1]
    change_needed = c
    change_given = []
    change_dictionary = {}

    while change_needed > 0:
        for coin in change_values:
            if coin <= change_needed:
                change_given.append(coin)
                change_needed -= coin
                break

    q = change_given.count(25)
    d = change_given.count(10)
    n = change_given.count(5)
    p = change_given.count(1)

    change_dictionary['q'] = q
    change_dictionary['d'] = d
    change_dictionary['n'] = n
    change_dictionary['p'] = p

    return change_dictionary


print(make_change(47))
