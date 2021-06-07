import os

import pyfiglet
from tkinter import filedialog, Tk


def main():
    create_test_folders()


def get_directory_to_scan():
    separator_2()
    print(pyfiglet.figlet_format('TEST', font='cybermedium'))
    print(pyfiglet.figlet_format('ENVIRONMENT', font='cybermedium'))
    separator_3()
    root = Tk()
    root.withdraw()
    root.update()
    selected_directory = filedialog.askdirectory()
    root.destroy()
    print("DIRECTORY INPUT: ", selected_directory)
    separator_3()
    return selected_directory


def create_test_folders():
    directory_selected_in_function = [get_directory_to_scan()]

    for items in os.listdir(directory_selected_in_function[0]):
        os.makedirs('/home/bx/Videos/TEMP/' + items, exist_ok=True)


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
