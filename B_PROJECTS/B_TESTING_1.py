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

username = None

tv_results_list = {}
tv_overview_plots_dict = {}


def match_similar_strings(a, b):
    return SequenceMatcher(None, a, b).ratio()


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


def create_tv_show_plot_overview_index():
    tv_folders_list = []

    with open(os.path.expanduser(r'C:\Users\botoole\TESTING_MEDIA_INDEX\TV_VIDEO_FILES_PATHS.csv'),
              encoding='UTF-8') as m_f_p:
        tv_index = csv.reader(m_f_p)

        for tv_file in sorted(tv_index):
            tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
            tv_title_key = tv_file[0].rsplit('/')[-2]

            if not tv_filename_key.lower().endswith('.nfo'):

                if tv_title_key not in tv_folders_list:
                    tv_folders_list.append(tv_title_key)

    for found_tv_shows in tv_folders_list:
        try:

            search_imdb_for_tv_shows(found_tv_shows)

        except (IOError, KeyError, TypeError, ValueError) as e:
            print('IMDB MATCH ERROR: TV SHOW FILE(S): ', tv_file[0])
            print('-' * 100, '\n')
            continue

        if found_tv_shows not in tv_overview_plots_dict:
            tv_overview_plots_dict[found_tv_shows] = {}
            tv_overview_plots_dict[found_tv_shows]['SHOW'] = found_tv_shows
            tv_overview_plots_dict[found_tv_shows]['PLOT'] = 'NO PLOT AVAILABLE'

    for found_items in tv_overview_plots_dict.items():
        print(found_items)


def search_imdb_for_tv_shows(item_to_search):
    ia = IMDb()

    item_info_set = None
    item_plot = None

    tv_imdb = ia.search_movie(item_to_search)
    possible_matches_list = []

    for found_items in tv_imdb:
        if found_items['kind'] != 'tv series':
            continue

        search_confidence_percentage = match_similar_strings(item_to_search.lower(), found_items['title'].lower())
        possible_matches = (found_items['title'], found_items.movieID, search_confidence_percentage)
        possible_matches_list.append(possible_matches)

    possible_matches_list.sort(key=lambda x: x[2], reverse=True)

    if possible_matches_list:
        item_id = possible_matches_list[0][1]
        item_info_set = ia.get_movie(item_id)

    try:

        if item_info_set:

            ia.update(item_info_set, 'episodes')
            item_title = item_info_set.get('title')
            item_year = item_info_set.get('year')

            if 'plot' in item_info_set:
                item_plot = item_info_set['plot']

            if item_title not in tv_overview_plots_dict:
                tv_overview_plots_dict[item_to_search] = {}
                tv_overview_plots_dict[item_to_search]['SHOW'] = str(str(item_title) + ' (' + str(item_year) + ')')
                tv_overview_plots_dict[item_to_search]['PLOT'] = item_plot[0].split('::')[0].strip()

    except (IOError, KeyError, TypeError, ValueError) as e:
        print('TV SHOW INFO ERROR: TV SHOW FILE(S): ', e)
        print('-' * 100, '\n')


create_tv_show_plot_overview_index()
