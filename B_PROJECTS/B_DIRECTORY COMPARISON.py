import os

import pyfiglet

from fuzzywuzzy import fuzz
from tkinter import filedialog, Tk


def main():
    while True:
        interface()


def get_directory_to_scan():
    root = Tk()
    root.withdraw()
    root.update()
    selected_directory = filedialog.askdirectory()
    root.destroy()
    print("DIRECTORY INPUT: ", selected_directory)
    separator_3()
    return selected_directory


def interface():
    separator_1()
    print(pyfiglet.figlet_format('DIRECTORY', font='cybermedium'))
    print(pyfiglet.figlet_format('COMPARISON', font='cybermedium'))
    separator_3()
    print('1) COMPARE MEDIA FROM TWO DIRECTORIES', '\n', '\n'
          '0) MAIN MENU')

    separator_3()
    user_input = input('ENTER OPTION #: ')
    separator_3()

    try:
        if int(user_input) == 1:
            scan_and_compare_directories()

        elif int(user_input) == 0:
            exit()

    except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
        print(e, '\n', ('-' * 100), '\n', 'INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
        return


def scan_and_compare_directories():
    separator_3()
    print('1) DISPLAY MEDIA ALREADY IN DATABASE             2) DISPLAY MEDIA NOT ALREADY IN DATABASE', '\n', '\n'
          '0) MAIN MENU')

    separator_3()
    user_input = input('ENTER OPTION #: ')
    separator_3()

    first_directory_found_items_list = []
    second_directory_found_items_list = []

    print('DIRECTORY (1): ', '\n')
    first_directory_selected_in_function = [get_directory_to_scan()]

    print('DIRECTORY (2): ', '\n')
    second_directory_selected_in_function = [get_directory_to_scan()]

    try:
        if int(user_input) == 1:

            for items in os.listdir(first_directory_selected_in_function[0]):
                if items in os.listdir(second_directory_selected_in_function[0]):
                    first_directory_found_items_list.append(items)

            print('DUPLICATES FOUND: ', '\n', '\n')
            for folders in first_directory_found_items_list:
                print(folders)
            separator_3()

        elif int(user_input) == 2:

            for items in os.listdir(first_directory_selected_in_function[0]):
                if items not in os.listdir(second_directory_selected_in_function[0]):
                    first_directory_found_items_list.append(items)

            print('NEW MEDIA FOUND: ', '\n', '\n')
            for items in first_directory_found_items_list:
                print(items)
            separator_3()

        elif int(user_input) == 0:
            interface()

    except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
        print(e, '\n', ('-' * 100), '\n', 'INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
        return


def separator_1():
    print('-' * 100)


def separator_2():
    for items in '\n', '-' * 100:
        print(items)


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


if __name__ == '__main__':
    main()
