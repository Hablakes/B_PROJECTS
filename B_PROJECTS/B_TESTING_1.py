from __future__ import unicode_literals

import csv
import json
import os
import pathlib
import re
import textwrap
import time

import guessit
import numpy
import pyfiglet
import pymediainfo
import youtube_dl

from datetime import datetime
from difflib import SequenceMatcher
from imdb import IMDb
from tkinter import filedialog, Tk

date_string = str(datetime.today().strftime('%Y_%m_%d'))

extensions = ('.3gp', '.asf', '.asx', '.avc', '.avi', '.bdmv', '.bin', '.bivx', '.dat', '.disc', '.divx', '.dv',
              '.dvr-ms', '.evo', '.fli', '.flv', '.h264', '.img', '.iso', '.m2ts', '.m2v', '.m4v', '.mkv', '.mov',
              '.mp4', '.mpeg', '.mpg', '.mt2s', '.mts', '.nfo', '.nrg', '.nsv', '.nuv', '.ogm', '.pva', '.qt', '.rm',
              '.rmvb', '.strm', '.svq3', '.ts', '.ty', '.viv', '.vob', '.vp3', '.wmv', '.xvid', '.webm')

index_folder = '~/{0}_MEDIA_INDEX'

username = 'TESTING'


def find_imdb_show(show_name):
    ia = IMDb()
    search_confidence_percentage = 0

    tv_imdb = ia.search_movie(show_name)

    possible_tv_show_matches_list = []

    for found_tv_plots in tv_imdb:
        if found_tv_plots['kind'] not in ('tv series', 'tv miniseries', 'tv movie'):
            continue

        search_confidence_percentage = match_similar_strings(show_name.lower(),
                                                             found_tv_plots['title'].lower())

        possible_tv_show_matches = \
            (found_tv_plots['title'], found_tv_plots.movieID, search_confidence_percentage)
        possible_tv_show_matches_list.append(possible_tv_show_matches)

    possible_tv_show_matches_list.sort(key=lambda x: x[2], reverse=True)

    if possible_tv_show_matches_list:
        tv_id = possible_tv_show_matches_list[0][1]
        tv_info_set = ia.get_movie(tv_id)
        return tv_info_set


def tv_show_imdb_check():
    tv_results_list = {}
    tv_overview_plots_dict = {}

    tv_folders_list = []

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as m_f_p:
        tv_index = csv.reader(m_f_p)

        for tv_file in sorted(tv_index):
            tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
            tv_title_key = tv_file[0].rsplit('/')[-2].split('(')[0]
            tv_title_and_year_key = tv_file[0].rsplit('/')[-2]
            tv_year_key = tv_file[0].rsplit('/')[-2].rsplit('(')[-1][:-1]

            if tv_title_key not in tv_folders_list:
                tv_folders_list.append(tv_title_key)

            if tv_file[0] not in tv_results_list:
                tv_results_list[tv_file[0]] = {}

            tv_results_list[tv_file[0]]['MEDIA-PATH'] = tv_file[0]
            tv_results_list[tv_file[0]]['MEDIA-TYPE'] = str('TV SHOW')
            tv_results_list[tv_file[0]]['FOLDER-NAME'] = tv_title_key
            tv_results_list[tv_file[0]]['FILE-NAME'] = tv_filename_key

    for found_tv_shows in tv_folders_list:
        found_result = find_imdb_show(found_tv_shows)
        if found_result:
            print(found_result), print(repr(found_result))
        else:
            print(found_tv_shows)

    separator_3()

    for found_tv_episodes in tv_results_list.items():
        print(found_tv_episodes)


def match_similar_strings(a, b):
    return SequenceMatcher(None, a, b).ratio()


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


tv_show_imdb_check()
# print(find_imdb_show('TEST SHOW'))
