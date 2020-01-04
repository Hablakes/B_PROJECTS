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
        return [tv_info_set, search_confidence_percentage]


def tv_show_episode_information_index():
    tv_results_list = {}
    tv_overview_plots_dict = {}

    tv_overview_plots_nfo_list = []

    tv_scan_start = time.time()

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as m_f_p:
        tv_index = csv.reader(m_f_p)

        for tv_file in sorted(tv_index):
            tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
            tv_title_key = tv_file[0].rsplit('/')[-2]

            if not tv_filename_key.lower().endswith('.nfo'):

                if tv_file[0] not in tv_results_list:
                    tv_results_list[tv_file[0]] = {}

                tv_file_size = os.path.getsize(tv_file[0])

                tv_results_list[tv_file[0]]['MEDIA-PATH'] = tv_file[0]
                tv_results_list[tv_file[0]]['MEDIA-TYPE'] = str('TV SHOW')
                tv_results_list[tv_file[0]]['FOLDER-NAME'] = tv_title_key
                tv_results_list[tv_file[0]]['FILE-NAME'] = tv_filename_key
                tv_results_list[tv_file[0]]['FILE-SIZE'] = str(round((int(tv_file_size) / 1048576), 2))
                tv_results_list[tv_file[0]]['TV-HASH'] = str(str(tv_filename_key) + '_' + str(tv_file_size))

                g_tv_title = guessit.guessit(tv_filename_key, options={'type': 'episode'})
                g_tv_title_to_query = g_tv_title.get('title')
                g_tv_episode_title = g_tv_title.get('alternative_title')
                g_season_number = g_tv_title.get('season')
                g_episode_number = g_tv_title.get('episode')

                tv_results_list[tv_file[0]]['FILE-TYPE'] = g_tv_title.get('container')

                if r"'" in g_tv_title_to_query:
                    g_tv_title_to_query = g_tv_title_to_query.replace("'", '')

                tv_media_info = pymediainfo.MediaInfo.parse(tv_file[0])

                for track in tv_media_info.tracks:
                    if track.track_type == 'General':
                        tv_results_list[tv_file[0]]['RUN-TIME'] = track.duration

                    elif track.track_type == 'Video':
                        tv_results_list[tv_file[0]]['RESOLUTION'] = str(track.width) + 'x' + str(track.height)

                if tv_title_key not in tv_overview_plots_dict:
                    tv_overview_plots_dict[tv_title_key] = {}

                found_result = find_imdb_show(g_tv_title_to_query)

                if found_result is not None:

                    IMDb().update(found_result[0], 'episodes')
                    tv_show_title = found_result[0].get('title')
                    item_year = found_result[0].get('year')

                    if 'plot' in found_result[0]:
                        tv_overview_plots_dict[tv_title_key]['SHOW'] = str(
                            str(tv_show_title) + ' (' + str(item_year) + ')')
                        item_plot = found_result[0]['plot']
                        tv_overview_plots_dict[tv_title_key]['PLOT'] = item_plot[0].split('::')[0].strip()

                    if 'episodes' in found_result[0]:
                        episode_title = found_result[0]['episodes'][g_season_number][g_episode_number].get('title')
                        episode_year = found_result[0]['episodes'][g_season_number][g_episode_number].get('year')
                        episode_plot = found_result[0]['episodes'][g_season_number][g_episode_number].get('plot')
                        episode_rating = found_result[0]['episodes'][g_season_number][g_episode_number].get('rating')

                        tv_results_list[tv_file[0]]['GUESSIT TV SHOW SEARCH TERM'] = g_tv_title_to_query
                        tv_results_list[tv_file[0]]['TV SHOW ID #'] = found_result[0].movieID
                        tv_results_list[tv_file[0]]['TV SHOW TITLE'] = tv_show_title
                        tv_results_list[tv_file[0]]['SEASON #'] = g_season_number
                        tv_results_list[tv_file[0]]['EPISODE #'] = g_episode_number
                        tv_results_list[tv_file[0]]['EPISODE TITLE'] = episode_title
                        tv_results_list[tv_file[0]]['YEAR'] = episode_year
                        tv_results_list[tv_file[0]]['PLOT'] = episode_plot.split('::')[0].strip()
                        tv_results_list[tv_file[0]]['RATING'] = round(episode_rating, 2)
                        tv_results_list[tv_file[0]]['GENRES'] = []
                        for genre in found_result[0]['genres']:
                            tv_results_list[tv_file[0]]['GENRES'].append(genre)
                        tv_results_list[tv_file[0]]['SEARCH CONFIDENCE PERCENTAGE'] = found_result[1]

                elif found_result is None:
                    tv_overview_plots_dict[tv_title_key]['SHOW'] = tv_title_key
                    tv_overview_plots_dict[tv_title_key]['PLOT'] = 'NO PLOT AVAILABLE'

                    tv_results_list[tv_file[0]]['GUESSIT TV SHOW SEARCH TERM'] = g_tv_title_to_query
                    tv_results_list[tv_file[0]]['TV SHOW ID #'] = 'NO ID # FOUND'
                    if g_tv_title_to_query:
                        tv_results_list[tv_file[0]]['TV SHOW TITLE'] = tv_title_key
                    else:
                        tv_results_list[tv_file[0]]['TV SHOW TITLE'] = 'NO TV SHOW TITLE FOUND'
                    if g_season_number:
                        tv_results_list[tv_file[0]]['SEASON #'] = g_season_number
                    else:
                        tv_results_list[tv_file[0]]['SEASON #'] = 'NO SEASON # FOUND'
                    if g_episode_number:
                        tv_results_list[tv_file[0]]['EPISODE #'] = g_episode_number
                    else:
                        tv_results_list[tv_file[0]]['EPISODE #'] = 'NO EPISODE # MATCHED'
                    if g_tv_episode_title:
                        tv_results_list[tv_file[0]]['EPISODE TITLE'] = g_tv_episode_title
                    else:
                        tv_results_list[tv_file[0]]['EPISODE TITLE'] = 'NO EPISODE TITLE FOUND'
                    tv_results_list[tv_file[0]]['YEAR'] = 'NO YEAR FOUND'
                    tv_results_list[tv_file[0]]['PLOT'] = 'NO PLOT FOUND'
                    tv_results_list[tv_file[0]]['RATING'] = 'NO RATING FOUND'
                    tv_results_list[tv_file[0]]['GENRES'] = 'NO GENRE(S) FOUND'
                    tv_results_list[tv_file[0]]['SEARCH CONFIDENCE PERCENTAGE'] = 'NO CONFIDENCE PERCENTAGE'

    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as m_i_i:

        csv_writer = csv.DictWriter(m_i_i, ['MEDIA-PATH', 'MEDIA-TYPE', 'FOLDER-NAME', 'FILE-NAME', 'FILE-SIZE',
                                            'TV-HASH', 'FILE-TYPE', 'RUN-TIME', 'RESOLUTION',
                                            'GUESSIT TV SHOW SEARCH TERM', 'TV SHOW ID #', 'TV SHOW TITLE', 'SEASON #',
                                            'EPISODE #', 'EPISODE TITLE', 'YEAR', 'PLOT', 'RATING', 'GENRES',
                                            'SEARCH CONFIDENCE PERCENTAGE'])

        for tv_row in tv_results_list.values():
            csv_writer.writerow(tv_row)

    with open(os.path.expanduser((index_folder + '/TV_PLOTS_INDEX.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as t_p_i:
        csv_writer = csv.DictWriter(t_p_i, ['SHOW', 'PLOT'])
        for tv_row in tv_overview_plots_dict.values():
            csv_writer.writerow(tv_row)

    tv_scan_end = time.time()
    readable_tv_scan_time = round(tv_scan_end - tv_scan_start, 2)
    separator_3()
    print('TV INFORMATION SCAN COMPLETE - TIME ELAPSED: ', readable_tv_scan_time, 'Seconds')
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


tv_show_episode_information_index()
