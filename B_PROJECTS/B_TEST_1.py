def while_example_1():

    lines = list()
    testAnswer = input('Press y if you want to enter more lines: ')

    while testAnswer == 'y':
        line = input('Next line: ')
        lines.append(line)
        testAnswer = input('Press y if you want to enter more lines: ')

    print('Your lines were:')
    for line in lines:
        print(line)


def while_example_2():

    lines = list()

    print('Enter lines of text.')
    print('Enter an empty line to quit.')

    line = input('Next line: ')
    while line != '':
        lines.append(line)
        line = input('Next line: ')

    print('Your lines were:')

    for line in lines:
        print(line)


print('\n', '-' * 100, '\n')
while_example_1()
print('\n', '-' * 100, '\n')
while_example_2()
print('\n', '-' * 100, '\n')
