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


def tv_show_episode_information_index():
    tv_results_list = {}
    tv_folders_list = []

    tv_scan_start = time.time()

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as m_f_p:
        tv_index = csv.reader(m_f_p)

        for tv_file in sorted(tv_index):
            tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
            tv_title_key = tv_file[0].rsplit('/')[-2]

            if tv_title_key not in tv_folders_list:
                tv_folders_list.append(tv_title_key)

            if not tv_filename_key.lower().endswith('.nfo'):

                if tv_file[0] not in tv_results_list:
                    tv_results_list[tv_file[0]] = {}

                tv_results_list[tv_file[0]]['MEDIA-PATH'] = tv_file[0]
                tv_results_list[tv_file[0]]['MEDIA-TYPE'] = str('TV SHOW')
                tv_results_list[tv_file[0]]['FOLDER-NAME'] = tv_title_key
                tv_results_list[tv_file[0]]['FILE-NAME'] = tv_filename_key

                tv_file_size = os.path.getsize(tv_file[0])
                tv_file_size_in_mb = (int(tv_file_size) / 1048576)
                tv_file_size_in_mb_rounded = str(round(tv_file_size_in_mb, 2))
                tv_hash = str(str(tv_filename_key) + '_' + str(tv_file_size))
                g_tv_title = guessit.guessit(tv_filename_key, options={'type': 'episode'})
                g_tv_episode_title = g_tv_title.get('alternative_title')
                g_tv_title_to_query = g_tv_title.get('title')
                g_season_number = g_tv_title.get('season')
                g_episode_number = g_tv_title.get('episode')
                g_tv_episode_container = g_tv_title.get('container')

                tv_results_list[tv_file[0]]['FILE-SIZE'] = tv_file_size_in_mb_rounded
                tv_results_list[tv_file[0]]['TV-HASH'] = tv_hash
                tv_results_list[tv_file[0]]['FILE-TYPE'] = g_tv_episode_container

                if r"'" in g_tv_title_to_query:
                    formatted_tv_title_to_query = g_tv_title_to_query.rsplit(r"'", 1)
                    g_tv_title_to_query = ' '.join(formatted_tv_title_to_query)

                tv_media_info = pymediainfo.MediaInfo.parse(tv_file[0])

                for track in tv_media_info.tracks:
                    if track.track_type == 'General':
                        tv_results_list[tv_file[0]]['RUN-TIME'] = track.duration

                    elif track.track_type == 'Video':
                        tv_results_list[tv_file[0]]['RESOLUTION'] = str(track.width) + 'x' + str(track.height)

    for found_tv_shows in tv_folders_list:
        found_result = find_imdb_show(found_tv_shows)

        if found_result:

            IMDb().update(found_result, 'episodes')

            item_title = found_result.get('title')
            item_year = found_result.get('year')

            if item_title not in tv_results_list:
                pass


def tv_shows_overview_plots_index():
    tv_overview_plots_dict = {}
    tv_folders_list = []
    tv_overview_plots_nfo_list = []

    tv_scan_start = time.time()

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as m_f_p:
        tv_index = csv.reader(m_f_p)

        for tv_file in sorted(tv_index):
            tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
            tv_title_key = tv_file[0].rsplit('/')[-2].split('(')[0]

            if tv_title_key not in tv_folders_list:
                tv_folders_list.append(tv_title_key)

    for found_tv_shows in tv_folders_list:
        found_result = find_imdb_show(found_tv_shows)

        if found_result:

            item_title = found_result.get('title')
            item_year = found_result.get('year')

            if item_title not in tv_overview_plots_dict:
                tv_overview_plots_dict[found_tv_shows] = {}
                tv_overview_plots_dict[found_tv_shows]['SHOW'] = str(
                    str(item_title) + ' (' + str(item_year) + ')')

                if 'plot' in found_result:
                    item_plot = found_result['plot']
                    tv_overview_plots_dict[found_tv_shows]['PLOT'] = item_plot[0].split('::')[0].strip()

        if found_tv_shows not in tv_overview_plots_dict:
            tv_overview_plots_dict[found_tv_shows] = {}
            tv_overview_plots_dict[found_tv_shows]['SHOW'] = found_tv_shows
            tv_overview_plots_dict[found_tv_shows]['PLOT'] = 'NO PLOT AVAILABLE'

    tv_scan_end = time.time()
    readable_tv_scan_time = round(tv_scan_end - tv_scan_start, 2)
    print('TV PLOT INFORMATION SCAN COMPLETE - TIME ELAPSED: ', readable_tv_scan_time, 'Seconds')
    separator_3()


def match_similar_strings(a, b):
    return SequenceMatcher(None, a, b).ratio()


def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


tv_shows_overview_plots_index()
# print(find_imdb_show('TEST SHOW'))
