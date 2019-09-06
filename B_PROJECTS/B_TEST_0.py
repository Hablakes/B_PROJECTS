import csv
import os
import pathlib

from tkinter import filedialog, Tk


username = 'TEST'


def separator_1():
    print('-' * 100)


def separator_2():
    for items in '\n', '-' * 100:
        print(items)


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


def tk_gui_file_browser_window():
    root = Tk()
    root.withdraw()
    root.update()
    selected_directory = filedialog.askdirectory()
    root.destroy()
    return selected_directory


def tk_gui_file_selection_window():
    root = Tk()
    root.withdraw()
    root.update()
    selected_file = filedialog.askopenfilename()
    root.destroy()
    return selected_file


def directory_selection():

    try:

        print('ENTER PATH OF MOVIE DIRECTORY, IF NONE HIT CANCEL: ', '\n')
        movie_dir_input = tk_gui_file_browser_window()

        separator_3()

        print('ENTER PATH OF TV DIRECTORY, IF NONE HIT CANCEL: ', '\n')
        tv_dir_input = tk_gui_file_browser_window()

        separator_3()

        print('ALTERNATE DIRECTORIES? - Y/N: ')

        separator_3()
        alternate_directory_prompt = input('ENTER: Y or N: ').lower()
        separator_3()

        if alternate_directory_prompt == str('y'):

            movie_alt_directories_list = []
            tv_alt_directories_list = []

            print('ENTER PATH OF ALTERNATE MOVIE DIRECTORIES, WHEN COMPLETE, HIT CANCEL: ', '\n')
            separator_3()

            movie_alt_directories_list.append(tk_gui_file_browser_window())

            print('ENTER PATH OF ALTERNATE TV DIRECTORIES, WHEN COMPLETE, HIT CANCEL: ', '\n')
            separator_3()

            tv_alt_directories_list.append(tk_gui_file_browser_window())

            movie_alt_dir_input = list(movie_alt_directories_list)
            tv_alt_dir_input = list(tv_alt_directories_list)

            user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input, 'tv_dir:': tv_dir_input,
                              'movie_alt_dir:': movie_alt_dir_input, 'tv_alt_dir:': tv_alt_dir_input}

            print(user_info_dict)

        elif alternate_directory_prompt != str('y'):
            print('NO ALTERNATE DIRECTORIES')
            separator_3()

            user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input, 'tv_dir:': tv_dir_input,
                              'movie_alt_dir:': '', 'tv_alt_dir:': ''}

            print(user_info_dict)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n')


directory_selection()
