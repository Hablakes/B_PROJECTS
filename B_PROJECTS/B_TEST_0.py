import csv
import os
import pathlib
import textwrap

import re

import guessit
import pyfiglet
import pymediainfo

from ascii_graph import Pyasciigraph
import matplotlib.pylab as plt
import numpy as np
from tkinter import *
from tkinter import filedialog

username_input = 'bx'
media_index_folder = '~/BB_MEDIA_INDEX'

extensions = ('.3gp', '.asf', '.asx', '.avc', '.avi', '.bdmv', '.bin', '.bivx', '.dat', '.disc', '.divx', '.dv',
              '.dvr-ms', '.evo', '.fli', '.flv', '.h264', '.img', '.iso', '.m2ts', '.m2v', '.m4v', '.mkv', '.mov',
              '.mp4', '.mpeg', '.mpg', '.mt2s', '.mts', '.nfo', '.nrg', '.nsv', '.nuv', '.ogm', '.pva', '.qt', '.rm',
              '.rmvb', '.strm', '.svq3', '.ts', '.ty', '.viv', '.vob', '.vp3', '.wmv', '.xvid', '.webm')


def divider():
    for items in '\n', '-' * 100:
        print(items)


def separator():
    for items in '\n', '-' * 100, '\n':
        print(items)


def search_titles():
    media_index_list = list(csv.reader(open(os.path.expanduser(
        (media_index_folder + '/MEDIA_TITLE_INDEX.csv').format(username_input)), encoding='UTF-8')))
    tv_files_results_list = list(csv.reader(open(os.path.expanduser(
        (media_index_folder + '/TV_INFORMATION_INDEX.csv').format(username_input)), encoding='UTF-8')))
    tv_show_episodes_dictionary = {}

    tv_show_query_action = input('ENTER SEARCH QUERY (TV SHOWS): ')
    separator()
    tv_show_query_action_lower = str(tv_show_query_action.lower())

    for tv_file in tv_files_results_list:
        if tv_show_query_action_lower in tv_file[1].lower():
            print(tv_file[0], ': ', tv_file[3])


search_titles()
