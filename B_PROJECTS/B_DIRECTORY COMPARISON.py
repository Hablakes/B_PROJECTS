import os

import pyfiglet

from tkinter import filedialog, Tk


def main():
    while True:
        interface()


def interface():
    separator_3()
    print(pyfiglet.figlet_format('DIRECTORY', font='cybermedium'))
    print(pyfiglet.figlet_format('COMPARISON TOOLS', font='cybermedium'))
    separator_3()
    print('1) COMPARE MEDIA FROM TWO DIRECTORIES:       2) COMPARE TEXT LIST AGAINST DIRECTORIES', '\n', '\n'
          '3) CHECK A SINGLE DIRECTORY FOR POTENTIAL DOUBLES', '\n', '\n'
          '0) MAIN MENU')

    separator_3()
    user_input = input('ENTER OPTION #: ')
    separator_3()

    try:
        if int(user_input) == 1:
            scan_and_compare_directories()

        elif int(user_input) == 2:
            scan_and_compare_text_list_to_directory()

        elif int(user_input) == 3:
            scan_single_directory_for_doubles()

        elif int(user_input) == 0:
            exit()

    except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
        print(e, '\n', ('-' * 100), '\n', 'INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
        return


def scan_and_compare_directories():
    separator_3()
    print('1) DISPLAY MEDIA IF ALREADY IN DATABASE:         2) DISPLAY MEDIA IF NOT ALREADY IN DATABASE: ', '\n', '\n'
          '0) MAIN MENU')

    separator_3()
    user_input = input('ENTER OPTION #: ')
    separator_3()

    directory_one_found_items = []
    directory_two_found_items = []

    print('SELECT DIRECTORY (1): ', '\n')
    first_directory_selected = [tk_gui_get_directory_to_scan()]

    print('SELECT DIRECTORY (2): ', '\n')
    second_directory_selected = [tk_gui_get_directory_to_scan()]

    for items in os.listdir(first_directory_selected[0]):
        if items in os.listdir(second_directory_selected[0]):
            directory_one_found_items.append(items)

    for items in os.listdir(first_directory_selected[0]):
        if items not in os.listdir(second_directory_selected[0]):
            directory_two_found_items.append(items)

    try:
        if int(user_input) == 1:

            print('DUPLICATES FOUND: ', '\n', '\n')
            for items in directory_one_found_items:
                print(items)

        elif int(user_input) == 2:

            print('NEW MEDIA FOUND: ', '\n', '\n')
            for items in directory_two_found_items:
                print(items)

        elif int(user_input) == 0:
            interface()

    except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
        print(e, '\n', ('-' * 100), '\n', 'INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
        return


def scan_and_compare_text_list_to_directory():
    separator_3()
    print('1) DISPLAY MEDIA IF ALREADY IN DATABASE:         2) DISPLAY MEDIA IF NOT ALREADY IN DATABASE: ', '\n', '\n'
          '0) MAIN MENU')

    separator_3()
    user_input = input('ENTER OPTION #: ')
    separator_3()

    text_list = []
    items_found_in_db_from_text_list = []
    items_not_found_in_db_from_text_list = []

    print('SELECT TEXT LIST: ', '\n')
    list_selected = [tk_gui_file_selection_window()]

    print('SELECT DIRECTORY: ', '\n')
    directory_selected = [tk_gui_get_directory_to_scan()]

    try:
        with open(list_selected[0], 'r') as f:
            for items in f.read().splitlines():
                text_list.append(items)

    except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
        print(e, '\n', ('-' * 100), '\n', 'INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
        return

    for items in text_list:
        if items in os.listdir(directory_selected[0]):
            items_found_in_db_from_text_list.append(items)

    for items in text_list:
        if items not in os.listdir(directory_selected[0]):
            items_not_found_in_db_from_text_list.append(items)

    try:
        if int(user_input) == 1:

            print('MEDIA FILES FROM TEXT LIST THAT ARE IN THE DATABASE: ', '\n', '\n')
            for items in items_found_in_db_from_text_list:
                print(items)

        elif int(user_input) == 2:

            print('MEDIA FILES FROM TEXT LIST THAT ARE NOT IN THE DATABASE: ', '\n', '\n')
            for items in items_not_found_in_db_from_text_list:
                print(items)

        elif int(user_input) == 0:
            interface()

    except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
        print(e, '\n', ('-' * 100), '\n', 'INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
        return


def scan_single_directory_for_doubles():
    directory_contents_dictionary = {}

    print('SELECT DIRECTORY: ', '\n')
    directory_selected = [tk_gui_get_directory_to_scan()]

    for items in os.listdir(directory_selected[0]):
        formatted_items = items.lower()[:-7]
        if formatted_items not in directory_contents_dictionary:
            directory_contents_dictionary[formatted_items] = []
        directory_contents_dictionary[formatted_items].append(items)

    print(directory_contents_dictionary)


def separator_1():
    print('-' * 100)


def separator_2():
    for items in '\n', '-' * 100:
        print(items)


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


def tk_gui_get_directory_to_scan():
    root = Tk()
    root.withdraw()
    root.update()
    selected_directory = filedialog.askdirectory()
    root.destroy()
    print("DIRECTORY INPUT: ", selected_directory)
    separator_3()
    return selected_directory


def tk_gui_file_selection_window():
    root = Tk()
    root.withdraw()
    root.update()
    selected_file = filedialog.askopenfilename()
    root.destroy()
    print("TEXT LIST INPUT: ", selected_file)
    separator_3()

    return selected_file


if __name__ == '__main__':
    main()
