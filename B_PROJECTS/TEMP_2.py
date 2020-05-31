l1 = ['Ex Machina', 'The Matrix', 'Westworld', ]
l2 = ['Ex Machina', 'Ghost In The Shell', 'The Matrix', 'Westworld', 'ZTF']


def compare_completed_results(results_one, results_two):
    output_one = []

    for line in results_one:
        if line not in results_two:
            output_one.append('REMOVAL: ' + line)

    for line in results_two:
        if line not in results_one:
            output_one.append('ADDITION: ' + line)

    return output_one


print(compare_completed_results(l2, l1))

