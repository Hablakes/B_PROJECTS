import csv
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


def directory_selection():

    try:
        user_info_file = os.path.expanduser((index_folder + '/{0}_USER_INFO.csv').format(username))

        print('ENTER PATH OF MOVIE DIRECTORY, IF NONE HIT CANCEL: ', '\n')
        movie_dir_input = tk_gui_file_browser_window()
        print('ENTER PATH OF TV DIRECTORY, IF NONE HIT CANCEL: ', '\n')
        tv_dir_input = tk_gui_file_browser_window()

        alternate_directory_prompt = input('ALTERNATE DIRECTORIES? - Y/N').lower()
        if alternate_directory_prompt == str('y'):

            print('ENTER PATH OF ALTERNATE MOVIE DIRECTORY, IF NONE HIT CANCEL: ', '\n')
            movie_alt_dir_input = tk_gui_file_browser_window()
            print('ENTER PATH OF ALTERNATE TV DIRECTORY, IF NONE HIT CANCEL: ', '\n')
            tv_alt_dir_input = tk_gui_file_browser_window()

            separator_3()
            user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input, 'tv_dir:': tv_dir_input,
                              'movie_alt_dir:': movie_alt_dir_input, 'tv_alt_dir:': tv_alt_dir_input}
            with open(user_info_file, 'w', encoding='UTF-8', newline='') as f:
                csv_writer = csv.writer(f)
                for user_data in user_info_dict.items():
                    csv_writer.writerow(user_data)

        elif alternate_directory_prompt != str('y'):
            separator_3()
            user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input, 'tv_dir:': tv_dir_input,
                              'movie_alt_dir:': '', 'tv_alt_dir:': ''}
            with open(user_info_file, 'w', encoding='UTF-8', newline='') as f:
                csv_writer = csv.writer(f)
                for user_data in user_info_dict.items():
                    csv_writer.writerow(user_data)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n')


def username_check_and_folder_creation():

    try:
        user_info_file = os.path.expanduser((index_folder + '/{0}_USER_INFO.csv').format(username))

        if os.path.isfile(user_info_file):
            user_info_file_check = list(csv.reader(open(user_info_file)))
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
