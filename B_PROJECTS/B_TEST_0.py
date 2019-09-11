import csv
import json
import os
import pathlib
import textwrap
import re

import guessit
import numpy
import pyfiglet
import pymediainfo

import matplotlib.pylab as plt

from ascii_graph import Pyasciigraph
from datetime import datetime
from tkinter import filedialog, Tk


index_folder = '~/{0}_MEDIA_INDEX'

username = None


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


def launch_media_index():
    print(pyfiglet.figlet_format('MEDIA_INDEX', font='cybermedium'))
    separator_3()

    try:

        global username
        username = input('ENTER YOUR USERNAME (CASE-SENSITIVE): ')
        separator_3()
        username_check_and_folder_creation()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
        launch_media_index()


def username_check_and_folder_creation():

    try:

        global movie_dir_input, tv_dir_input, movie_alt_dir_input, tv_alt_dir_input
        user_info_file = os.path.expanduser((index_folder + '/{0}_USER_INFO.json').format(username))

        if os.path.isfile(user_info_file):
            user_info_file_check = list(csv.reader(open(user_info_file, encoding='UTF-8', newline='')))
            movie_dir_input = user_info_file_check[1][1]
            tv_dir_input = user_info_file_check[2][1]
            movie_alt_dir_input = user_info_file_check[3][1]
            tv_alt_dir_input = user_info_file_check[4][1]

        else:
            os.makedirs(os.path.expanduser((index_folder + '/').format(username)), exist_ok=True)
            os.makedirs(os.path.expanduser((index_folder + '/FILES').format(username)), exist_ok=True)
            os.makedirs(os.path.expanduser((index_folder + '/GRAPHS').format(username)), exist_ok=True)
            os.makedirs(os.path.expanduser((index_folder + '/SEARCH').format(username)), exist_ok=True)
            directory_selection()

    except (OSError, TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
        separator_3()


def directory_selection():
    try:

        global movie_dir_input, tv_dir_input, movie_alt_dir_input, tv_alt_dir_input
        user_info_file = os.path.expanduser((index_folder + '/{0}_USER_INFO.json').format(username))

        print('ENTER PATH OF MOVIE DIRECTORY, IF NONE HIT CANCEL: ')
        movie_dir_input = tk_gui_file_browser_window()
        print('\n', str(movie_dir_input))

        separator_3()
        print('ENTER PATH OF TV DIRECTORY, IF NONE HIT CANCEL: ')
        tv_dir_input = tk_gui_file_browser_window()
        print('\n', str(tv_dir_input))

        separator_3()
        print('ALTERNATE DIRECTORIES? - Y/N: ')

        separator_3()
        alternate_directory_prompt = input('ENTER: Y or N: ').lower()
        separator_3()

        if alternate_directory_prompt == str('y'):

            movie_alt_directories_list = list()
            print('ENTER ALTERNATE MOVIE DIRECTORIES, WHEN COMPLETE, HIT CANCEL: ')
            separator_3()

            movie_alt_dir_input = tk_gui_file_browser_window()

            while movie_alt_dir_input != '':
                movie_alt_directories_list.append(movie_alt_dir_input)
                movie_alt_dir_input = tk_gui_file_browser_window()

            print('DIRECTORIES ENTERED: ', '\n', '\n', movie_alt_directories_list)

            tv_alt_directories_list = list()
            separator_3()
            print('ENTER ALTERNATE TV DIRECTORIES, WHEN COMPLETE, HIT CANCEL: ')
            separator_3()

            tv_alt_dir_input = tk_gui_file_browser_window()

            while tv_alt_dir_input != '':
                tv_alt_directories_list.append(tv_alt_dir_input)
                tv_alt_dir_input = tk_gui_file_browser_window()

            print('DIRECTORIES ENTERED: ', '\n', '\n', tv_alt_directories_list)
            separator_3()

            user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input,
                              'tv_dir:': tv_dir_input, 'movie_alt_dir:': movie_alt_directories_list,
                              'tv_alt_dir:': tv_alt_directories_list}

            with open(user_info_file, 'w', encoding='UTF-8') as json_file:
                for user_data in user_info_dict.items():
                    json.dump(user_data, json_file, ensure_ascii=False, indent=4)

        elif alternate_directory_prompt != str('y'):

            print('NO ALTERNATE DIRECTORIES')
            separator_3()

            user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input,
                              'tv_dir:': tv_dir_input, 'movie_alt_dir:': '', 'tv_alt_dir:': ''}

            with open(user_info_file, 'w', encoding='UTF-8') as json_file:
                for user_data in user_info_dict.items():
                    json.dump(user_data, json_file, ensure_ascii=False, indent=4)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n')
        separator_3()


def test():
    tst_username = 'TST'
    user_info_file = os.path.expanduser((index_folder + '/{0}_USER_INFO.json').format(tst_username))

    with open(user_info_file) as json_file:
        user_info_data = json.load(json_file)
        for info in user_info_data:
            print(info)


launch_media_index()
