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

from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from datetime import datetime
from difflib import SequenceMatcher
from tkinter import filedialog, Tk

date_string = str(datetime.today().strftime('%Y_%m_%d'))

extensions = ('.3gp', '.asf', '.asx', '.avc', '.avi', '.bdmv', '.bin', '.bivx', '.dat', '.disc', '.divx', '.dv',
              '.dvr-ms', '.evo', '.fli', '.flv', '.h264', '.img', '.iso', '.m2ts', '.m2v', '.m4v', '.mkv', '.mov',
              '.mp4', '.mpeg', '.mpg', '.mt2s', '.mts', '.nfo', '.nrg', '.nsv', '.nuv', '.ogm', '.pva', '.qt', '.rm',
              '.rmvb', '.strm', '.svq3', '.ts', '.ty', '.viv', '.vob', '.vp3', '.wmv', '.xvid', '.webm')

index_folder = '~/{0}_MEDIA_INDEX'

new_user_movies_dirs = '/FILES/NEW_MOVIE_VIDEO_FILES_PATHS.csv'
new_user_tv_dirs = '/FILES/NEW_TV_VIDEO_FILES_PATHS.csv'

new_user_movies_index = '/FILES/NEW_MOVIES_INFORMATION_INDEX.csv'
new_user_tv_index = '/FILES/NEW_TV_INFORMATION_INDEX.csv'

user_movies_dirs = '/MOVIE_VIDEO_FILES_PATHS.csv'
user_tv_dirs = '/TV_VIDEO_FILES_PATHS.csv'

user_movies_index = '/MOVIES_INFORMATION_INDEX.csv'
user_tv_index = '/TV_INFORMATION_INDEX.csv'

username = None


def main():
    separator_3()
    launch_media_index()

    while True:
        media_index_home()


def change_directory_selection():
    print(pyfiglet.figlet_format('CHANGE_DIRECTORY', font='cybermedium'))
    separator_3()
    directory_selection()


def compare_completed_results(results_one, results_two):
    output_one = []

    for line in results_one:
        if line not in results_two:
            output_one.append('REMOVAL: ' + line)

    for line in results_two:
        if line not in results_one:
            output_one.append('ADDITION: ' + line)

    return output_one


def compare_individual_files():
    pass


def create_media_information_indices():
    create_media_title_index()
    create_information_index_movies()
    create_information_index_tv()


def create_media_title_index():
    movie_title_items = []
    tv_title_items = []

    naming_scan_start = time.time()

    try:

        if movie_dir_input != '':
            movie_dir_list = os.listdir(movie_dir_input)

            for movie_found in sorted(movie_dir_list):
                movie_scrape_info = guessit.guessit(movie_found)
                title_item_check = ['MOVIE', str(movie_scrape_info.get('title')), str(movie_scrape_info.get('year'))]

                if ',' in title_item_check[2]:
                    title_item_check.append(title_item_check[2][-5:-1])
                    title_item_check.remove(title_item_check[2])
                movie_title_items.append(title_item_check)

        if movie_alt_dir_input != '':
            found_alt_movie_directories_list = []

            for alternate_movie_directories in movie_alt_dir_input:
                movie_alt_dir_list = os.listdir(alternate_movie_directories)

                for found_alt_movie_directories in movie_alt_dir_list:
                    found_alt_movie_directories_list.append(found_alt_movie_directories)
                for movie_found in sorted(found_alt_movie_directories_list):
                    movie_scrape_info = guessit.guessit(movie_found)
                    title_item_check = ['MOVIE', str(movie_scrape_info.get('title')),
                                        str(movie_scrape_info.get('year'))]

                    if ',' in title_item_check[2]:
                        title_item_check.append(title_item_check[2][-5:-1])
                        title_item_check.remove(title_item_check[2])
                    movie_title_items.append(title_item_check)

        if tv_dir_input != '':
            tv_dir_list = os.listdir(tv_dir_input)

            for tv_found in sorted(tv_dir_list):
                tv_scrape_info = guessit.guessit(tv_found)
                title_item_check = ['TV', str(tv_scrape_info.get('title')), str(tv_scrape_info.get('year'))]

                if ',' in title_item_check[2]:
                    title_item_check.append(title_item_check[2][-5:-1])
                    title_item_check.remove(title_item_check[2])
                tv_title_items.append(title_item_check)

        if tv_alt_dir_input != '':
            found_alt_tv_directories_list = []

            for alternate_tv_directories in tv_alt_dir_input:
                tv_alt_dir_list = os.listdir(alternate_tv_directories)

                for found_alt_tv_directories in tv_alt_dir_list:
                    found_alt_tv_directories_list.append(found_alt_tv_directories)
                for tv_found in sorted(found_alt_tv_directories_list):
                    tv_scrape_info = guessit.guessit(tv_found)
                    title_item_check = ['TV', str(tv_scrape_info.get('title')), str(tv_scrape_info.get('year'))]

                    if ',' in title_item_check[2]:
                        title_item_check.append(title_item_check[2][-5:-1])
                        title_item_check.remove(title_item_check[2])
                    tv_title_items.append(title_item_check)

        with open(os.path.expanduser((index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)), 'w',
                  encoding='UTF-8', newline='') as m_t_i:
            csv_writer = csv.writer(m_t_i)
            for file_row in movie_title_items:
                csv_writer.writerow(file_row)

            for file_row in tv_title_items:
                csv_writer.writerow(file_row)

    except (OSError, TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INCORRECT DIRECTORY INPUT(S), PLEASE RETRY')
        separator_3()

    naming_scan_end = time.time()
    readable_naming_scan_time = round(naming_scan_end - naming_scan_start, 2)
    print('MEDIA TITLES SCAN COMPLETE - TIME ELAPSED: ', readable_naming_scan_time, 'Seconds')
    separator_3()


def create_information_index_movies(input_file, output_file):
    movie_results_list = {}

    movie_scan_start = time.time()

    with open(os.path.expanduser((index_folder + input_file).format(username)),
              encoding='UTF-8') as m_f_p:
        movie_index = csv.reader(m_f_p)

        for movie_file in sorted(movie_index):

            try:

                movie_filename_key = movie_file[0].rsplit('/', 1)[-1]
                movie_title_key = movie_file[0].rsplit('/')[-2]
                title_folder_year = movie_title_key[-5:-1]

                if not movie_filename_key.lower().endswith('.nfo'):

                    if movie_file[0] not in movie_results_list:
                        movie_results_list[movie_file[0]] = {}

                    movie_results_list[movie_file[0]]['MEDIA-PATH'] = movie_file[0]

                    movie_results_list[movie_file[0]]['MEDIA-TYPE'] = str('MOVIE')

                    movie_results_list[movie_file[0]]['FOLDER-NAME'] = movie_title_key

                    movie_results_list[movie_file[0]]['FILE-NAME'] = movie_filename_key

                    try:

                        movie_file_size = os.path.getsize(movie_file[0])
                        movie_file_size_in_mb = (int(movie_file_size) / 1048576)
                        movie_file_size_in_mb_rounded = str(round(movie_file_size_in_mb, 2))

                        movie_results_list[movie_file[0]]['FILE-SIZE'] = movie_file_size_in_mb_rounded

                    except OSError as e:
                        print('FILE-SIZE ERROR: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        movie_title = guessit.guessit(movie_filename_key, options={'type': 'movie'})
                        movie_title_to_query = movie_title.get('title')
                        movie_title_year = movie_title.get('year')

                        movie_results_list[movie_file[0]]['GUESSIT-SEARCH-TERM'] = movie_title_to_query

                        if movie_title_year:
                            movie_results_list[movie_file[0]]['YEAR'] = movie_title_year
                        else:
                            movie_results_list[movie_file[0]]['YEAR'] = title_folder_year

                    except OSError as e:
                        print('GUESSIT ERROR: ', e)
                        print('-' * 100, '\n')
                        continue

                    movie_results_list[movie_file[0]]['FILE-TYPE'] = movie_file[0].rsplit('.')[-1]

                    try:

                        movie_media_info = pymediainfo.MediaInfo.parse(movie_file[0])

                    except OSError as e:
                        print('PY_MEDIA_INFO ERROR: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        for track in movie_media_info.tracks:

                            if track.track_type == 'General':
                                movie_results_list[movie_file[0]]['RUN-TIME'] = track.duration
                                track_duration = str(round(track.duration, 2))

                                if track.count_of_text_streams:
                                    movie_results_list[movie_file[0]]['SUBTITLE-TRACKS'] = track.count_of_text_streams
                                else:
                                    movie_results_list[movie_file[0]]['SUBTITLE-TRACKS'] = str('NO EMBEDDED SUB-TITLES')

                            elif track.track_type == 'Audio':
                                movie_results_list[movie_file[0]]['AUDIO-TRACKS'] = [track.language,
                                                                                     track.commercial_name,
                                                                                     track.codec_id]

                            elif track.track_type == 'Video':
                                movie_results_list[movie_file[0]]['ASPECT-RATIO'] = \
                                    track.other_display_aspect_ratio[0].replace(':', 'x')

                                movie_results_list[movie_file[0]]['VIDEO-CODEC'] = track.encoded_library_name

                                movie_results_list[movie_file[0]]['RESOLUTION'] = \
                                    str(track.width) + 'x' + str(track.height)

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('PY_MEDIA_INFO ERROR (TRACKS): ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        movie_hash = str(str(movie_file_size) + '_' + str(movie_filename_key) + '_' +
                                         str(track_duration))

                        movie_results_list[movie_file[0]]['MOVIE-HASH-CODE'] = movie_hash

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('MEDIA FILE HASH CODE ERROR: ', e)
                        print('-' * 100, '\n')
                        continue

            except (IOError, KeyError, TypeError, ValueError) as e:
                print('INPUT ERROR: ', e, '\n', 'MOVIE FILE(S): ', movie_file[0])
                print('-' * 100, '\n')
                continue

    with open(os.path.expanduser((index_folder + output_file).format(username)), 'w',
              encoding='UTF-8', newline='') as m_i_i:

        csv_writer = csv.DictWriter(m_i_i, ['MEDIA-PATH', 'MEDIA-TYPE', 'FOLDER-NAME', 'FILE-NAME', 'FILE-SIZE',
                                            'GUESSIT-SEARCH-TERM', 'YEAR', 'FILE-TYPE', 'RUN-TIME', 'AUDIO-TRACKS', 
                                            'SUBTITLE-TRACKS', 'ASPECT-RATIO', 'VIDEO-CODEC', 'RESOLUTION', 
                                            'MOVIE-HASH-CODE'])

        for movie_row in movie_results_list.values():
            csv_writer.writerow(movie_row)

    movie_scan_end = time.time()
    readable_movie_scan_time = round(movie_scan_end - movie_scan_start, 2)
    print('MOVIE INFORMATION SCAN COMPLETE - TIME ELAPSED: ', readable_movie_scan_time, 'Seconds')
    separator_3()


def create_information_index_tv(input_file, output_file):
    tv_results_list = {}

    tv_scan_start = time.time()

    with open(os.path.expanduser((index_folder + input_file).format(username)),
              encoding='UTF-8') as m_f_p:
        tv_index = csv.reader(m_f_p)

        for tv_file in sorted(tv_index):

            try:

                tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
                tv_title_key = tv_file[0].rsplit('/')[-2]
                title_folder_year = tv_title_key[-5:-1]

                if not tv_filename_key.lower().endswith('.nfo'):

                    if tv_file[0] not in tv_results_list:
                        tv_results_list[tv_file[0]] = {}

                    tv_results_list[tv_file[0]]['MEDIA-PATH'] = tv_file[0]

                    tv_results_list[tv_file[0]]['MEDIA-TYPE'] = str('TV SHOW')

                    tv_results_list[tv_file[0]]['FOLDER-NAME'] = tv_title_key

                    tv_results_list[tv_file[0]]['FILE-NAME'] = tv_filename_key

                    try:

                        tv_file_size = os.path.getsize(tv_file[0])
                        tv_file_size_in_mb = (int(tv_file_size) / 1048576)
                        tv_file_size_in_mb_rounded = str(round(tv_file_size_in_mb, 2))

                        tv_results_list[tv_file[0]]['FILE-SIZE'] = tv_file_size_in_mb_rounded

                    except OSError as e:
                        print('FILE-SIZE ERROR: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        tv_title = guessit.guessit(tv_filename_key, options={'type': 'episode'})
                        tv_title_to_query = tv_title.get('title')
                        tv_episode_name = tv_title.get('episode_title')
                        tv_title_year = tv_title.get('year')
                        g_season_number = tv_title.get('season')
                        g_episode_number = tv_title.get('episode')

                        tv_results_list[tv_file[0]]['GUESSIT-SEARCH-TERM'] = tv_title_to_query

                        if tv_title_year:
                            tv_results_list[tv_file[0]]['YEAR'] = tv_title_year
                        else:
                            tv_results_list[tv_file[0]]['YEAR'] = title_folder_year

                        tv_results_list[tv_file[0]]['SEASON #'] = g_season_number

                        tv_results_list[tv_file[0]]['EPISODE #'] = g_episode_number

                        tv_results_list[tv_file[0]]['EPISODE-TITLE'] = tv_episode_name

                    except OSError as e:
                        print('GUESSIT ERROR: ', e)
                        print('-' * 100, '\n')
                        continue

                    tv_results_list[tv_file[0]]['FILE-TYPE'] = tv_file[0].rsplit('.')[-1]

                    try:

                        tv_media_info = pymediainfo.MediaInfo.parse(tv_file[0])

                    except OSError as e:
                        print('PY_MEDIA_INFO ERROR: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        for track in tv_media_info.tracks:

                            if track.track_type == 'General':
                                tv_results_list[tv_file[0]]['RUN-TIME'] = track.duration
                                track_duration = str(round(track.duration, 2))

                                if track.count_of_text_streams:
                                    tv_results_list[tv_file[0]]['SUBTITLE-TRACKS'] = track.count_of_text_streams
                                else:
                                    tv_results_list[tv_file[0]]['SUBTITLE-TRACKS'] = str('NO EMBEDDED SUB-TITLES')

                            elif track.track_type == 'Audio':
                                tv_results_list[tv_file[0]]['AUDIO-TRACKS'] = [track.language, track.commercial_name,
                                                                               track.codec_id]

                            elif track.track_type == 'Video':
                                tv_results_list[tv_file[0]]['ASPECT-RATIO'] = \
                                    track.other_display_aspect_ratio[0].replace(':', 'x')

                                tv_results_list[tv_file[0]]['VIDEO-CODEC'] = track.encoded_library_name

                                tv_results_list[tv_file[0]]['RESOLUTION'] = \
                                    str(track.width) + 'x' + str(track.height)

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('PY_MEDIA_INFO ERROR (TRACKS): ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        tv_hash = str(str(tv_file_size) + '_' + str(tv_filename_key) + '_' + str(track_duration))

                        tv_results_list[tv_file[0]]['TV-HASH-CODE'] = tv_hash

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('MEDIA FILE HASH CODE ERROR: ', e)
                        print('-' * 100, '\n')
                        continue

            except (IOError, KeyError, TypeError, ValueError) as e:
                print('INPUT ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                print('-' * 100, '\n')
                continue

    with open(os.path.expanduser((index_folder + output_file).format(username)), 'w',
              encoding='UTF-8', newline='') as m_i_i:

        csv_writer = csv.DictWriter(m_i_i, ['MEDIA-PATH', 'MEDIA-TYPE', 'FOLDER-NAME', 'FILE-NAME', 'FILE-SIZE',
                                            'GUESSIT-SEARCH-TERM', 'YEAR', 'SEASON #', 'EPISODE #', 'EPISODE-TITLE',
                                            'FILE-TYPE', 'RUN-TIME', 'AUDIO-TRACKS', 'SUBTITLE-TRACKS', 'ASPECT-RATIO',
                                            'VIDEO-CODEC', 'RESOLUTION', 'TV-HASH-CODE'])

        for tv_row in tv_results_list.values():
            csv_writer.writerow(tv_row)

    tv_scan_end = time.time()
    readable_tv_scan_time = round(tv_scan_end - tv_scan_start, 2)
    print('TV INFORMATION SCAN COMPLETE - TIME ELAPSED: ', readable_tv_scan_time, 'Seconds')
    separator_3()


def directory_selection(user_type):

    if user_type == 1:

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

            if alternate_directory_prompt == 'y':

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
                movie_alt_dir_input = movie_alt_directories_list
                tv_alt_dir_input = tv_alt_directories_list
                user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input,
                                  'tv_dir:': tv_dir_input, 'movie_alt_dir:': movie_alt_dir_input,
                                  'tv_alt_dir:': tv_alt_dir_input}

                with open(user_info_file, 'w', encoding='UTF-8') as json_file:
                    json.dump(user_info_dict, json_file, ensure_ascii=False, indent=4, sort_keys=True)

            elif alternate_directory_prompt != 'y':

                print('NO ALTERNATE DIRECTORIES')
                separator_3()
                movie_alt_dir_input = ''
                tv_alt_dir_input = ''
                user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input,
                                  'tv_dir:': tv_dir_input, 'movie_alt_dir:': movie_alt_dir_input,
                                  'tv_alt_dir:': tv_alt_dir_input}

                with open(user_info_file, 'w', encoding='UTF-8') as json_file:
                    json.dump(user_info_dict, json_file, ensure_ascii=False, indent=4, sort_keys=True)

        except (TypeError, ValueError) as e:
            print('\n', 'INPUT ERROR: ', e, '\n')
            separator_3()

    elif user_type == 2:

        try:

            print('ENTER PATH OF MOVIE DIRECTORY TO COMPARE NEW FILES, IF NONE HIT CANCEL: ')
            new_movie_dir_input = tk_gui_file_browser_window()
            print('\n', str(new_movie_dir_input))
            separator_3()

            print('ENTER PATH OF TV DIRECTORY TO COMPARE NEW FILES, IF NONE HIT CANCEL: ')
            new_tv_dir_input = tk_gui_file_browser_window()
            print('\n', str(new_tv_dir_input))
            separator_3()

        except (TypeError, ValueError) as e:
            print('\n', 'INPUT ERROR: ', e, '\n')
            separator_3()


def graph_options_advanced(terminal_graph_options_int):
    m_4k_found_list = []
    m_1080_found_list = []
    m_720_found_list = []
    m_640_found_list = []
    m_empty_response_list = []
    movies_total_list = []

    tv_4k_found_list = []
    tv_1080_found_list = []
    tv_720_found_list = []
    tv_640_found_list = []
    tv_empty_response_list = []
    tv_total_list = []

    with open(os.path.expanduser((index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as m_i_i:
        movie_files_results_list = list(csv.reader(m_i_i))
    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as t_i_i:
        tv_files_results_list = list(csv.reader(t_i_i))

        for res in movie_files_results_list:
            if re.findall(r'[2-9]\d{3}x', res[13]):
                m_4k_found_list.append(res)

            elif re.findall(r'19\d{2}x', res[13]):
                m_1080_found_list.append(res)

            elif re.findall(r'1[0-8]\d{2}x', res[13]):
                m_720_found_list.append(res)

            elif re.findall(r'\d{3}x', res[13]):
                m_640_found_list.append(res)

            else:
                m_empty_response_list.append(+1)
            movies_total_list.append(+1)

        movies_graph_terminal_results = [('4k', float(len(m_4k_found_list))),
                                         ('1080p', float(len(m_1080_found_list))),
                                         ('720p', float(len(m_720_found_list))),
                                         ('640p', float(len(m_640_found_list)))]

        for res in tv_files_results_list:
            if re.findall(r'[2-9]\d{3}x', res[16]):
                tv_4k_found_list.append(res)

            elif re.findall(r'19\d{2}x', res[16]):
                tv_1080_found_list.append(res)

            elif re.findall(r'1[0-8]\d{2}x', res[16]):
                tv_720_found_list.append(res)

            elif re.findall(r'\d{3}x', res[16]):
                tv_640_found_list.append(res)

            else:
                tv_empty_response_list.append(+1)
            tv_total_list.append(+1)

        tv_shows_graph_terminal_results = [('4k', float(len(tv_4k_found_list))),
                                           ('1080p', float(len(tv_1080_found_list))),
                                           ('720p', float(len(tv_720_found_list))),
                                           ('640p', float(len(tv_640_found_list)))]

        graph_color_pattern = [IBlu, BCya, Blu, Pur]

        if terminal_graph_options_int == 5:
            color_movies_graph_terminal_results = vcolor(movies_graph_terminal_results, graph_color_pattern)
            graph = Pyasciigraph()
            for line in graph.graph('MOVIES: RESOLUTION PERCENTAGES: ', color_movies_graph_terminal_results):
                print('\n', line)
            separator_3()

        elif terminal_graph_options_int == 6:
            color_tv_shows_graph_terminal_results = vcolor(tv_shows_graph_terminal_results, graph_color_pattern)
            graph = Pyasciigraph()
            for line in graph.graph('TV SHOWS: RESOLUTION PERCENTAGES: ', color_tv_shows_graph_terminal_results):
                print('\n', line)
            separator_3()


def graph_options_base(terminal_graph_options_int):
    movie_years_dict = {}
    movie_decades_dict = {}
    tv_years_dict = {}
    tv_decades_amount_dict = {}
    movie_year_totals_dict = {}
    movie_decades_totals_dict = {}
    tv_year_totals_dict = {}
    tv_decades_totals_dict = {}

    graph_color_pattern = [IBlu, BCya, Blu, Pur]

    with open(os.path.expanduser((index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)),
              encoding='UTF-8') as m_t_i:
        media_index_list = list(csv.reader(m_t_i))

        for title_item in media_index_list:
            title_item_year = re.split(r'(.+) \((\d{4})\)', title_item[2], flags=0)
            title_item_year_int = int(title_item_year[0])
            title_item_decade_int = int(title_item_year[0][:-1] + '0')

            if title_item_year_int in range(1900, 2100, 1):
                if 'MOVIE' in title_item:
                    if title_item_year_int not in movie_years_dict:
                        movie_years_dict[title_item_year_int] = []
                    movie_years_dict[title_item_year_int].append(title_item)

                    if title_item_decade_int not in movie_decades_dict:
                        movie_decades_dict[title_item_decade_int] = []
                    movie_decades_dict[title_item_decade_int].append(title_item)

                if 'TV' in title_item:
                    if title_item_year_int not in tv_years_dict:
                        tv_years_dict[title_item_year_int] = []
                    tv_years_dict[title_item_year_int].append(title_item)

                    if title_item_decade_int not in tv_decades_amount_dict:
                        tv_decades_amount_dict[title_item_decade_int] = []
                    tv_decades_amount_dict[title_item_decade_int].append(title_item)

        if terminal_graph_options_int == 1:
            for movie_year_values, value in sorted(movie_years_dict.items()):
                movie_year_totals_dict[movie_year_values] = len(value)
            movie_data = sorted(movie_year_totals_dict.items())
            movie_years_terminal_graph_list = []

            for key, value in movie_data:
                movie_years_terminal_graph_list.append((str(key), value))

            color_movie_years_terminal_graph_list = vcolor(movie_years_terminal_graph_list, graph_color_pattern)
            graph = Pyasciigraph()

            for line in graph.graph('MOVIES: YEAR AMOUNTS: ', color_movie_years_terminal_graph_list):
                print('\n', line)
            separator_3()

        elif terminal_graph_options_int == 2:
            for tv_year_values, value in sorted(tv_years_dict.items()):
                tv_year_totals_dict[tv_year_values] = len(value)
            tv_data = sorted(tv_year_totals_dict.items())
            tv_years_terminal_graph_list = []

            for key, value in tv_data:
                tv_years_terminal_graph_list.append((str(key), value))

            color_tv_years_terminal_graph_list = vcolor(tv_years_terminal_graph_list, graph_color_pattern)
            graph = Pyasciigraph()

            for line in graph.graph('TV SHOWS: YEAR AMOUNTS: ', color_tv_years_terminal_graph_list):
                print('\n', line)
            separator_3()

        elif terminal_graph_options_int == 3:
            for movie_year_values, value in sorted(movie_decades_dict.items()):
                movie_decades_totals_dict[movie_year_values] = len(value)
            movie_decades_terminal_graph_list = []

            for key, value in movie_decades_totals_dict.items():
                movie_decades_terminal_graph_list.append((str(key), value))

            color_movie_decades_terminal_graph_list = vcolor(movie_decades_terminal_graph_list, graph_color_pattern)
            graph = Pyasciigraph()

            for line in graph.graph('MOVIES: DECADE AMOUNTS: ', color_movie_decades_terminal_graph_list):
                print('\n', line)
            separator_3()

        elif terminal_graph_options_int == 4:
            for tv_year_values, value in sorted(tv_decades_amount_dict.items()):
                tv_decades_totals_dict[tv_year_values] = len(value)
            tv_decades_terminal_graph_list = []

            for key, value in tv_decades_totals_dict.items():
                tv_decades_terminal_graph_list.append((str(key), value))

            color_tv_decades_terminal_graph_list = vcolor(tv_decades_terminal_graph_list, graph_color_pattern)
            graph = Pyasciigraph()

            for line in graph.graph('TV SHOWS: DECADE AMOUNTS: ', color_tv_decades_terminal_graph_list):
                print('\n', line)
            separator_3()


def launch_media_index():
    print(pyfiglet.figlet_format('MEDIA_INDEX', font='cybermedium'))
    separator_3()

    try:

        global username
        username = input('ENTER YOUR USERNAME (CASE-SENSITIVE): ')

        if username == '':
            separator_3()
            print('USERNAME CANNOT BE LEFT BLANK: ')
            separator_3()
            launch_media_index()
        separator_3()
        username_check_and_folder_creation()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
        launch_media_index()


def match_similar_strings(a, b):
    return SequenceMatcher(None, a, b).ratio()


def media_index_home(user_type):
    print(pyfiglet.figlet_format('MEDIA_INDEX', font='cybermedium'))
    separator_3()

    print('1) ADD / CHANGE DATABASE DIRECTORIES                 2) CREATE PATH INDICES', '\n')
    print('3) CREATE / UPDATE MEDIA INFORMATION INDICES         4) COMPARISON OPTIONS')
    separator_3()
    print('5) MEDIA LIBRARY TOTALS                              6) QUERY DETAILED MEDIA INFORMATION', '\n')
    print('7) TERMINAL GRAPH OPTIONS                            8) TIME INFORMATION QUERIES', '\n')
    print('9) SORTING OPTIONS')
    separator_2()
    print('0) EXIT MEDIA-INDEX')
    separator_3()

    try:

        lmi_input = input('ENTER #: ')
        separator_3()
        lmi_input_action = int(lmi_input)

        if lmi_input_action == 0:
            exit()

        elif lmi_input_action == 1:

            try:

                print('CONFIRM: ')
                separator_1()
                print('1) CHANGE DATABASE DIRECTORIES                       '
                      '2) SELECT DIRECTORIES FOR NEW FILES TO COMPARE')
                separator_2()
                print('0) MAIN MENU')
                separator_3()
                db_scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if db_scan_sub_input == 0:
                    media_index_home()

                elif db_scan_sub_input == 1:
                    change_directory_selection(user_type=1)

                elif db_scan_sub_input == 2:
                    change_directory_selection(user_type=2)

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif lmi_input_action == 2:

            try:

                print('CONFIRM: ')
                separator_1()
                print('THIS OPERATION MAY TAKE A LONG TIME (SEVERAL MINUTES FOR LARGE LIBRARIES)')
                separator_2()
                print('1) CONTINUE WITH MEDIA PATH(S) SCAN                  0) MAIN MENU')
                separator_3()
                path_scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if path_scan_sub_input == 0:
                    media_index_home()

                elif path_scan_sub_input == 1:
                    walk_directories_and_create_indices()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif lmi_input_action == 3:

            try:

                print('CONFIRM: ')
                separator_1()
                print('THIS OPERATION CAN TAKE A LONG TIME (SEVERAL HOURS FOR LARGE LIBRARIES)')
                separator_2()
                print('1) CONTINUE WITH MEDIA INFORMATION SCAN              0) MAIN MENU')
                separator_3()
                information_scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if information_scan_sub_input == 0:
                    media_index_home()

                elif information_scan_sub_input == 1:
                    create_media_information_indices()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif lmi_input_action == 4:

            try:

                print('CONFIRM: ')
                separator_1()
                print('1) COMPARE USER(S) INFORMATION INDICES               2) COMPARE NEW FILE(S) AGAINST DB')
                separator_2()
                print('0) MAIN MENU')
                separator_3()
                comparison_scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if comparison_scan_sub_input == 0:
                    media_index_home()

                elif comparison_scan_sub_input == 1:
                    pass

                elif comparison_scan_sub_input == 2:
                    pass

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif lmi_input_action == 5:
            total_media_library_amount()

        elif lmi_input_action == 6:
            media_queries_sub_menu()

        elif lmi_input_action == 7:
            terminal_graph_options_sub_menu()

        elif lmi_input_action == 8:
            time_queries_sub_menu()

        elif lmi_input_action == 9:
            sort_options_sub_menu()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


def media_queries_sub_menu():
    print(pyfiglet.figlet_format('MEDIA_QUERIES', font='cybermedium'))
    separator_3()

    print('SEARCH FOR TITLES OF:                            1) MOVIES       2) TV SHOWS', '\n')
    print('SEARCH FOR TITLES OF:                            3) TV SHOW EPISODES')
    separator_2()
    print('SEARCH FOR DETAILED INFORMATION OF:              4) MOVIES (BY MOVIE TITLE)', '\n')
    print('SEARCH FOR DETAILED INFORMATION OF:              5) TV SHOWS (BY EPISODE TITLE)')
    separator_2()
    print('                                                 6) TOTAL NUMBER (#) OF EPISODES IN A TV SHOW')
    separator_2()
    print('0) MAIN MENU')
    separator_3()

    try:

        title_search_type = int(input('ENTER #: '))
        separator_3()

        if title_search_type == 0:
            media_index_home()

        elif title_search_type == 1:
            movie_title_query_input = str(input('QUERY MOVIES: ').lower())
            separator_3()
            search_titles(title_search_type=1, movie_title_query=movie_title_query_input,
                          tv_show_query='')

        elif title_search_type == 2:
            tv_show_query_input = str(input('ENTER SEARCH QUERY (TV SHOWS): ').lower())
            separator_3()
            search_titles(title_search_type=2, movie_title_query='',
                          tv_show_query=tv_show_query_input)

        elif title_search_type == 3:
            tv_show_query_input = str(input('ENTER SEARCH QUERY (TV SHOWS): ').lower())
            separator_3()
            search_titles(title_search_type=3, movie_title_query='',
                          tv_show_query=tv_show_query_input)

        elif title_search_type == 4:
            movie_title_query_input = str(input('ENTER SEARCH QUERY (MOVIES): ').lower())
            separator_3()
            query_movie_information_index(movie_query=movie_title_query_input)

        elif title_search_type == 5:
            tv_episode_query_input = str(input('ENTER SEARCH QUERY (TV SHOWS): ').lower())
            separator_3()
            query_tv_information_index(tv_episode_query=tv_episode_query_input)

        elif title_search_type == 6:
            total_tv_episodes_in_show()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


def query_file_type_totals(terminal_graph_options_int):
    movie_extensions_dictionary = {}
    movie_extensions_totals = {}
    tv_extensions_dictionary = {}
    tv_extensions_totals = {}

    graph_color_pattern = [IBlu, BCya, Blu, Pur]

    with open(os.path.expanduser((index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as m_i_i:
        movie_files_results_list = list(csv.reader(m_i_i))
    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as t_i_i:
        tv_files_results_list = list(csv.reader(t_i_i))

        for file_type in movie_files_results_list:
            if ',' not in file_type[7]:

                if file_type[7] not in movie_extensions_dictionary:
                    movie_extensions_dictionary[file_type[7]] = []
                movie_extensions_dictionary[file_type[7]].append(file_type[7])

        if terminal_graph_options_int == 7:

            for file_type_values, value in sorted(movie_extensions_dictionary.items()):
                movie_extensions_totals[file_type_values] = len(value)
            file_type_totals_terminal_graph_list = []

            for key, value in movie_extensions_totals.items():
                file_type_totals_terminal_graph_list.append((str(key), value))

            color_file_type_totals_terminal_graph_list = vcolor(file_type_totals_terminal_graph_list,
                                                                graph_color_pattern)
            graph = Pyasciigraph()

            for line in graph.graph('MOVIES: FILE-TYPE AMOUNTS: ', color_file_type_totals_terminal_graph_list):
                print('\n', line)
            separator_3()

        for file_type in tv_files_results_list:
            if ',' not in file_type[10]:
                if file_type[10] not in tv_extensions_dictionary:
                    tv_extensions_dictionary[file_type[10]] = []
                tv_extensions_dictionary[file_type[10]].append(file_type[10])

        if terminal_graph_options_int == 8:

            for file_type_values, value in sorted(tv_extensions_dictionary.items()):
                tv_extensions_totals[file_type_values] = len(value)
            file_type_totals_terminal_graph_list = []

            for key, value in tv_extensions_totals.items():
                file_type_totals_terminal_graph_list.append((str(key), value))

            color_file_type_totals_terminal_graph_list = vcolor(file_type_totals_terminal_graph_list,
                                                                graph_color_pattern)
            graph = Pyasciigraph()

            for line in graph.graph('TV SHOWS: FILE-TYPE AMOUNTS: ', color_file_type_totals_terminal_graph_list):
                print('\n', line)
            separator_3()


def query_movie_information_index(movie_query):
    with open(os.path.expanduser((index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as m_i_i:
        mv_files_results_list = csv.reader(m_i_i)

        try:

            for movie_file in mv_files_results_list:
                if str(movie_query.lower()) in str(movie_file[2].lower()):

                    separator_2()
                    print('MOVIE PATH: ', '\n', movie_file[0])
                    separator_2()
                    print('MEDIA TYPE: ', '\n', movie_file[1])
                    separator_2()
                    print('MOVIE FOLDER NAME: ', '\n', movie_file[2])
                    separator_2()
                    print('MOVIE FILE-NAME: ', '\n', movie_file[3])
                    separator_2()
                    if int(len(movie_file[4])) != 0:
                        print('FILE-SIZE: ', '\n', movie_file[4], 'MB')
                        separator_2()
                    print('GUESSIT-SEARCH-TERM: ', '\n', movie_file[5])
                    separator_2()
                    print('MOVIE YEAR: ', '\n', movie_file[6])
                    separator_2()
                    print('MOVIE FILE-TYPE: ', '\n', movie_file[7])
                    separator_2()
                    if int(len(movie_file[8])) != 0:
                        print('RUN-TIME: ', '\n', int(movie_file[8]) // 60000, 'MINUTES')
                        separator_2()
                    print('MOVIE AUDIO-TRACKS: ', '\n', movie_file[9])
                    separator_2()
                    print('MOVIE SUBTITLE TRACKS: ', '\n', movie_file[10])
                    separator_2()
                    print('MOVIE ASPECT-RATIO: ', '\n', movie_file[11])
                    separator_2()
                    print('MOVIE VIDEO-CODEC: ', '\n', movie_file[12])
                    separator_2()
                    print('MOVIE RESOLUTION: ', '\n', movie_file[13])
                    separator_2()
                    print('MOVIE HASH-CODE: ', '\n', movie_file[14])
                    separator_2()

            separator_2()

        except (TypeError, ValueError) as e:
            print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID QUERY, PLEASE RETRY')
            separator_3()


def query_tv_information_index(tv_episode_query):
    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as t_i_i:
        tv_files_results_list = csv.reader(t_i_i)

        try:

            for tv_file in tv_files_results_list:
                if str(tv_episode_query.lower()) in str(tv_file[3].lower()):

                    separator_2()
                    print('TV SHOW PATH: ', '\n', tv_file[0])
                    separator_2()
                    print('MEDIA TYPE: ', '\n', tv_file[1])
                    separator_2()
                    print('TV SHOW FOLDER NAME: ', '\n', tv_file[2])
                    separator_2()
                    print('TV SHOW FILE-NAME: ', '\n', tv_file[3])
                    separator_2()
                    if int(len(tv_file[4])) != 0:
                        print('FILE-SIZE: ', '\n', tv_file[4], 'MB')
                        separator_2()
                    print('GUESSIT-SEARCH-TERM: ', '\n', tv_file[5])
                    separator_2()
                    print('TV SHOW YEAR: ', '\n', tv_file[6])
                    separator_2()
                    print('TV SHOW SEASON #: ', '\n', tv_file[7])
                    separator_2()
                    print('TV SHOW EPISODE #: ', '\n', tv_file[8])
                    separator_2()
                    print('TV SHOW EPISODE TITLE: ', '\n', tv_file[9])
                    separator_2()
                    print('TV SHOW FILE-TYPE: ', '\n', tv_file[10])
                    separator_2()
                    if int(len(tv_file[11])) != 0:
                        print('RUN-TIME: ', '\n', int(tv_file[11]) // 60000, 'MINUTES')
                        separator_2()
                    print('TV SHOW AUDIO-TRACKS: ', '\n', tv_file[12])
                    separator_2()
                    print('TV SHOW SUBTITLE TRACKS: ', '\n', tv_file[13])
                    separator_2()
                    print('TV SHOW ASPECT-RATIO: ', '\n', tv_file[14])
                    separator_2()
                    print('TV SHOW VIDEO-CODEC: ', '\n', tv_file[15])
                    separator_2()
                    print('TV SHOW RESOLUTION: ', '\n', tv_file[16])
                    separator_2()
                    print('TV SHOW HASH-CODE: ', '\n', tv_file[17])
                    separator_2()

            separator_2()

        except (TypeError, ValueError) as e:
            print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID QUERY, PLEASE RETRY')
            separator_3()


def search_titles(title_search_type, movie_title_query, tv_show_query):
    episode_information_list = []
    episode_information_search_list = []
    episode_folder_titles_dictionary = {}
    episode_folder_titles_list = []

    with open(os.path.expanduser((index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)),
              encoding='UTF-8') as m_t_i:
        media_index_list = list(csv.reader(m_t_i))
    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as t_i_i:
        tv_files_results_list = csv.reader(t_i_i)

        if title_search_type == 1:

            try:

                print('SEARCH RESULTS: ')
                separator_1()
                print('MOVIES: ', '\n')

                for movie_search_result in media_index_list:
                    if 'MOVIE' in movie_search_result[0]:
                        search_info = re.split(r'(.+) \((\d{4})\) \((.+)x(.+)\)\.(.+)', str(movie_search_result),
                                               flags=0)

                        if movie_title_query.lower() in search_info[0].lower():
                            print(search_info[0])
                separator_3()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
                separator_3()

        elif title_search_type == 2:

            try:

                print('SEARCH RESULTS: ')
                separator_1()
                print('TV SHOWS: ', '\n')

                for tv_search_result in media_index_list:
                    if 'TV' in tv_search_result[0]:
                        search_info = re.split(r'(.+) \((\d{4})\) \((.+)x(.+)\)\.(.+)', str(tv_search_result), flags=0)

                        if tv_show_query.lower() in search_info[0].lower():
                            print(search_info[0])
                separator_3()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
                separator_3()

        elif title_search_type == 3:

            try:

                for tv_file in tv_files_results_list:
                    tv_folder_key = tv_file[2]
                    tv_title_key = tv_folder_key[:-7]
                    tv_episode_name_key = tv_file[9]

                    if tv_show_query.lower() in tv_title_key.lower():

                        if str(tv_episode_name_key) == '':
                            tv_episode_name_key = 'MEDIA_INDEX - NO EPISODE TITLE'
                        episode_information_list.append([tv_title_key, tv_episode_name_key])

                        if tv_folder_key not in episode_folder_titles_dictionary:
                            episode_folder_titles_dictionary[tv_folder_key] = {}
                            episode_folder_titles_dictionary[tv_folder_key]['EPISODES'] = []
                        episode_folder_titles_dictionary[tv_folder_key]['EPISODES'].append(tv_episode_name_key)

                for enumeration_number, found_episodes in enumerate(episode_information_list):
                    found_tv_folder_key = found_episodes[0]
                    found_tv_episode_name_key = found_episodes[1]
                    episode_information_search_list.append([(str(enumeration_number) + ') '),
                                                            (str(found_tv_folder_key) + ' - '),
                                                            str(found_tv_episode_name_key)])
                print('TV SHOWS FOUND: ')
                separator_1()

                for found_tv_shows in episode_folder_titles_dictionary.keys():
                    episode_folder_titles_list.append(found_tv_shows)

                for show_titles in episode_folder_titles_list:
                    print('-', show_titles)

                separator_3()
                print('EPISODES FOUND: (IF NO LIST PRESENT, SELECT "0) MAIN MENU)"')
                separator_1()

                for search_results in episode_information_search_list:
                    print(''.join(search_results))

                separator_2()
                print('DETAILED EPISODE INFORMATION AVAILABLE: ')
                separator_1()
                print('0) MAIN MENU                                 1) QUERY AN EPISODES INFORMATION')
                separator_3()

                try:

                    title_search_sub_query_input = int(input('ENTER #: '))
                    separator_3()

                    if title_search_sub_query_input == 0:
                        media_index_home()

                    elif title_search_sub_query_input == 1:

                        episode_sub_query_input = int(input('ENTER EPISODE NUMBER (#): '))
                        episode_to_query = str(episode_information_search_list[episode_sub_query_input][2])
                        episode_to_query_lower = episode_to_query.lower()
                        separator_3()

                        print('QUERYING INFORMATION FOR EPISODE TITLED: ', episode_to_query)
                        separator_2()
                        query_tv_information_index(tv_episode_query=episode_to_query_lower)

                except (TypeError, ValueError) as e:
                    print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                    separator_3()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
                separator_3()


def select_users_indices_to_compare():
    try:

        print('\n', 'SELECT THE INFORMATION INDICES TO COMPARE: ')
        separator_3()

        print('SELECT USER MOVIE INFORMATION INDEX: ', '\n')
        m_0 = tk_gui_file_selection_window()
        print('SELECT COMPARISON MOVIE INFORMATION INDEX: ', '\n')
        m_1 = tk_gui_file_selection_window()
        print('SELECT USER TV INFORMATION INDEX: ', '\n')
        t_0 = tk_gui_file_selection_window()
        print('SELECT COMPARISON TV INFORMATION INDEX: ', '\n')
        t_1 = tk_gui_file_selection_window()
        separator_3()

        with open(m_0, 'r', encoding='UTF-8') as movies_0, open(m_1, 'r', encoding='UTF-8') as movies_1:
            user_movie_results = movies_0.readlines()
            comparison_movie_results = movies_1.readlines()

            with open(os.path.expanduser(
                    (index_folder + '/RESULTS/MOVIE_COMPARISON_INDEX.csv').format(username)),
                    'w', encoding='UTF-8', newline='') as outFile_m:
                for line in compare_completed_results(user_movie_results, comparison_movie_results):
                    outFile_m.write(line)

        with open(t_0, 'r', encoding='UTF-8') as tv_0, open(t_1, 'r', encoding='UTF-8') as tv_1:
            user_tv_results = tv_0.readlines()
            comparison_tv_results = tv_1.readlines()

            with open(os.path.expanduser(
                    (index_folder + '/RESULTS/TV_COMPARISON_INDEX.csv').format(username)),
                    'w', encoding='UTF-8', newline='') as outFile_t:
                for line in compare_completed_results(user_tv_results, comparison_tv_results):
                    outFile_t.write(line)

    except (OSError, TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
        separator_3()

    print('COMPLETE: COMPARISON FILE(S) CAN BE FOUND IN THE USER MEDIA-INDEX FOLDER, "RESULTS" SUB-FOLDER')
    separator_3()


def separator_1():
    print('-' * 100)


def separator_2():
    for items in '\n', '-' * 100:
        print(items)


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


def sort_function_base(sort_options_int):
    movie_info_list = []
    tv_info_list = []

    with open(os.path.expanduser((index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as m_i_i:
        movie_files_results_list = list(csv.reader(m_i_i))

    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as t_i_i:
        tv_files_results_list = list(csv.reader(t_i_i))

        for movie_info in movie_files_results_list:
            movie_title = movie_info[2]
            movie_size = movie_info[4]
            movie_time = movie_info[8].split('.')[-1]

            if movie_title == '':
                movie_title = 'MEDIA_INDEX - NO MOVIE TITLE'
            if movie_size == '':
                movie_size = '0'
            if movie_time == '':
                movie_time = '0'

            movie_time_total_readable_seconds = int(movie_time) // 1000
            movie_time_total_readable_minutes = int(movie_time_total_readable_seconds) // 60
            movie_info_list.append([movie_title, float(movie_size), float(movie_time_total_readable_minutes)])

        for tv_show_info in tv_files_results_list:
            tv_show_title = tv_show_info[2]
            episode_size = tv_show_info[4]
            episode_title = tv_show_info[9]
            episode_time = tv_show_info[11].split('.')[-1]

            if tv_show_title == '':
                tv_show_title = 'MEDIA_INDEX - NO TV SHOW TITLE'
            if episode_size == '':
                episode_size = '0'
            if episode_title == '':
                episode_title = 'MEDIA_INDEX - NO TV EPISODE TITLE'
            if episode_time == '':
                episode_time = '0'

            tv_time_total_readable_seconds = int(episode_time) // 1000
            tv_time_total_readable_minutes = int(tv_time_total_readable_seconds) // 60
            tv_info_list.append([tv_show_title, episode_title, float(episode_size),
                                 float(tv_time_total_readable_minutes)])

        movies_sorted_by_size = sorted(movie_info_list, key=lambda x: x[1])
        movies_sorted_by_size_r = sorted(movie_info_list, key=lambda x: x[1], reverse=True)
        movies_sorted_by_time = sorted(movie_info_list, key=lambda x: x[2])
        movies_sorted_by_time_r = sorted(movie_info_list, key=lambda x: x[2], reverse=True)
        tv_shows_sorted_by_size = sorted(tv_info_list, key=lambda x: x[2])
        tv_shows_sorted_by_size_r = sorted(tv_info_list, key=lambda x: x[2], reverse=True)
        tv_shows_sorted_by_time = sorted(tv_info_list, key=lambda x: x[3])
        tv_shows_sorted_by_time_r = sorted(tv_info_list, key=lambda x: x[3], reverse=True)

        if sort_options_int == 1:
            for movie_sizes in movies_sorted_by_size:
                print('\n', movie_sizes[0], '-', movie_sizes[1], ': MB')
            separator_3()

        elif sort_options_int == 2:
            for movie_sizes in movies_sorted_by_size_r:
                print('\n', movie_sizes[0], '-', movie_sizes[1], ': MB')
            separator_3()

        elif sort_options_int == 3:
            for movie_run_times in movies_sorted_by_time:
                print('\n', movie_run_times[0], '-', movie_run_times[2], ': Minutes')
            separator_3()

        elif sort_options_int == 4:
            for movie_run_times in movies_sorted_by_time_r:
                print('\n', movie_run_times[0], '-', movie_run_times[2], ': Minutes')
            separator_3()

        elif sort_options_int == 5:
            for episode_sizes in tv_shows_sorted_by_size:
                print('\n', episode_sizes[0], '-', episode_sizes[1], '-', episode_sizes[2], ': MB')
            separator_3()

        elif sort_options_int == 6:
            for episode_sizes in tv_shows_sorted_by_size_r:
                print('\n', episode_sizes[0], '-', episode_sizes[1], '-', episode_sizes[2], ': MB')
            separator_3()

        elif sort_options_int == 7:
            for episode_run_times in tv_shows_sorted_by_time:
                print('\n', episode_run_times[0], '-', episode_run_times[1], '-', episode_run_times[3], ': Minutes')
            separator_3()

        elif sort_options_int == 8:
            for episode_run_times in tv_shows_sorted_by_time_r:
                print('\n', episode_run_times[0], '-', episode_run_times[1], '-', episode_run_times[3], ': Minutes')
            separator_3()

    with open(os.path.expanduser((index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)),
              encoding='UTF-8') as m_t_i:
        media_index = list(csv.reader(m_t_i))

        sorted_titles = sorted(media_index, key=lambda x: (x[0], x[1]))
        sorted_titles_r = sorted(media_index, key=lambda x: (x[0], x[1]), reverse=True)
        sorted_years = sorted(media_index, key=lambda x: (x[0], x[2]))
        sorted_years_r = sorted(media_index, key=lambda x: (x[0], x[2]), reverse=True)

        if sort_options_int == 17:
            for title_item in sorted_titles:
                print('\n', title_item[0], ': Title -', title_item[1], ': Year -', title_item[2])
            separator_3()

        elif sort_options_int == 18:
            for title_item in sorted_titles_r:
                print('\n', title_item[0], ': Title -', title_item[1], ': Year -', title_item[2])
            separator_3()

        elif sort_options_int == 19:
            for title_item in sorted_years:
                print('\n', title_item[0], ': Title -', title_item[1], ': Year -', title_item[2])
            separator_3()

        elif sort_options_int == 20:
            for title_item in sorted_years_r:
                print('\n', title_item[0], ': Title -', title_item[1], ': Year -', title_item[2])
            separator_3()


def sort_function_for_tv_episodes(sort_options_int):
    tv_amounts_list = []
    tv_show_episodes_found_list = []
    tv_show_found_dict = {}
    tv_show_count_found_dict = {}
    tv_show_run_times_total_list = []
    tv_show_file_sizes_total_list = []

    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as t_i_i:
        tv_results_list = list(csv.reader(t_i_i))

        for tv_title in tv_results_list:
            tv_amounts_list.append(tv_title[2])
            if tv_title[0] not in tv_show_found_dict:
                tv_show_found_dict[tv_title[2]] = {}
                tv_show_found_dict[tv_title[2]]['RUN-TIMES'] = []
                tv_show_found_dict[tv_title[2]]['FILE-SIZES'] = []

            tv_run_times = tv_title[11]
            tv_file_sizes = tv_title[4]

            if tv_run_times == '':
                tv_run_times = 0
            if tv_file_sizes == '':
                tv_file_sizes = 0

            tv_show_found_dict[tv_title[2]]['RUN-TIMES'].append(float(tv_run_times))
            tv_show_found_dict[tv_title[2]]['FILE-SIZES'].append(float(tv_file_sizes))

        for found_tv_title in tv_amounts_list:
            tv_show_episodes_found_list.append(found_tv_title)
            tv_show_count_found_dict[found_tv_title] = tv_show_episodes_found_list.count(found_tv_title)

        for tv_show_keys, tv_show_values in tv_show_found_dict.items():
            show_run_time_total = sum(tv_show_values['RUN-TIMES'])
            show_run_time_total_seconds = show_run_time_total / 1000
            show_run_time_total_minutes = round(show_run_time_total_seconds / 60, 2)
            tv_show_run_times_total_list.append([tv_show_keys, show_run_time_total_minutes])

        for tv_show_keys, tv_show_values in tv_show_found_dict.items():
            show_file_size_total = sum(tv_show_values['FILE-SIZES'])
            tv_show_file_sizes_total_list.append([tv_show_keys, round(show_file_size_total, 2)])

        episode_titles_a = sorted(tv_show_count_found_dict.items(), key=lambda kv: kv[0])
        episode_titles_d = sorted(tv_show_count_found_dict.items(), key=lambda kv: kv[0], reverse=True)
        episode_amount_a = sorted(tv_show_count_found_dict.items(), key=lambda kv: kv[1])
        episode_amount_d = sorted(tv_show_count_found_dict.items(), key=lambda kv: kv[1], reverse=True)
        episode_times_a = sorted(tv_show_run_times_total_list, key=lambda x: x[1])
        episode_times_d = sorted(tv_show_run_times_total_list, key=lambda x: x[1], reverse=True)
        episode_sizes_a = sorted(tv_show_file_sizes_total_list, key=lambda x: x[1])
        episode_sizes_d = sorted(tv_show_file_sizes_total_list, key=lambda x: x[1], reverse=True)

        if sort_options_int == 9:
            for item in episode_sizes_a:
                print('\n', item[0], '-', item[1], ': MB Total')
            separator_3()

        elif sort_options_int == 10:
            for item in episode_sizes_d:
                print('\n', item[0], '-', item[1], ': MB Total')
            separator_3()

        elif sort_options_int == 11:
            for item in episode_times_a:
                print('\n', item[0], '-', item[1], ': Minutes Total')
            separator_3()

        elif sort_options_int == 12:
            for item in episode_times_d:
                print('\n', item[0], '-', item[1], ': Minutes Total')
            separator_3()

        elif sort_options_int == 13:
            for item in episode_titles_a:
                print('\n', item[0], '-', item[1], ': Episodes')
            separator_3()

        elif sort_options_int == 14:
            for item in episode_titles_d:
                print('\n', item[0], '-', item[1], ': Episodes')
            separator_3()

        elif sort_options_int == 15:
            for item in episode_amount_a:
                print('\n', item[0], '-', item[1], ': Episodes')
            separator_3()

        elif sort_options_int == 16:
            for item in episode_amount_d:
                print('\n', item[0], '-', item[1], ': Episodes')
            separator_3()


def sort_options_sub_menu():
    print(pyfiglet.figlet_format('SORT_OPTIONS', font='cybermedium'))
    separator_3()

    print('SORT MOVIES BY:                      SIZES:      1) ASCENDING    2) DESCENDING', '\n')
    print('                                     TIMES:      3) ASCENDING    4) DESCENDING')
    separator_2()
    print('SORT ALL TV EPISODES BY:             SIZES:      5) ASCENDING    6) DESCENDING', '\n')
    print('                                     TIMES:      7) ASCENDING    8) DESCENDING')
    separator_2()
    print('SORT TV SHOW TOTALS BY:              SIZES:      9) ASCENDING    10) DESCENDING', '\n')
    print('                                     TIMES:      11) ASCENDING   12) DESCENDING')
    separator_2()
    print('SORT NUMBER (#) OF TV EPISODES BY:   TITLES:     13) ASCENDING   14) DESCENDING', '\n')
    print('                                     AMOUNT:     15) ASCENDING   16) DESCENDING')
    separator_2()
    print('SORT MOVIE & TV SHOWS TOTALS BY:     TITLES:     17) ASCENDING   18) DESCENDING', '\n')
    print('                                     YEARS:      19) ASCENDING   20) DESCENDING')
    separator_2()

    print('0) MAIN MENU')
    separator_3()

    try:

        sort_input = input('ENTER #: ')
        separator_3()
        sort_options_int = int(sort_input)

        if sort_options_int == 0:
            media_index_home()

        elif 1 <= sort_options_int <= 8:
            sort_function_base(sort_options_int=sort_options_int)

        elif 9 <= sort_options_int <= 16:
            sort_function_for_tv_episodes(sort_options_int=sort_options_int)

        elif 17 <= sort_options_int <= 20:
            sort_function_base(sort_options_int=sort_options_int)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


def terminal_graph_options_sub_menu():
    print(pyfiglet.figlet_format('TERMINAL_GRAPHS', font='cybermedium'))
    separator_3()

    print('1) MOVIES (TITLES PER YEAR)                      2) TV SHOWS (TITLES PER YEAR)', '\n')
    print('3) MOVIES (TITLES PER DECADE)                    4) TV SHOWS (TITLES PER DECADE)')
    separator_2()
    print('5) MOVIES (RESOLUTIONS PERCENTAGES)              6) TV SHOWS (RESOLUTIONS PERCENTAGES)')
    separator_2()
    print('7) MOVIES (FILE-TYPE AMOUNTS)                    8) TV SHOWS (FILE-TYPE AMOUNTS)')
    separator_2()
    print('0) MAIN MENU')
    separator_3()

    try:

        terminal_graph_options = input('ENTER #: ')
        separator_3()
        terminal_graph_options_int = int(terminal_graph_options)

        if terminal_graph_options_int == 0:
            media_index_home()

        elif 1 <= terminal_graph_options_int <= 4:
            graph_options_base(terminal_graph_options_int=terminal_graph_options_int)

        elif 5 <= terminal_graph_options_int <= 6:
            graph_options_advanced(terminal_graph_options_int=terminal_graph_options_int)

        elif 7 <= terminal_graph_options_int <= 8:
            query_file_type_totals(terminal_graph_options_int=terminal_graph_options_int)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


def time_queries_sub_menu():
    print(pyfiglet.figlet_format('TIME_QUERIES', font='cybermedium'))
    separator_3()

    movie_times_list = []
    tv_times_list = []
    all_media_times_list = []
    time_queries_input_list = []

    try:

        print('                                                 1) QUERY DURATION INFORMATION FOR MOVIES', '\n')
        print('                                                 2) QUERY DURATION INFORMATION FOR TV SHOWS')
        separator_2()
        print('                                                 3) QUERY DURATION INFORMATION FOR ALL MEDIA')
        separator_2()
        print('0) MAIN MENU')
        separator_3()

        time_queries_input = input('ENTER #: ')
        separator_3()
        time_queries_input_int = int(time_queries_input)
        time_queries_input_list.append(time_queries_input_int)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()

    with open(os.path.expanduser((index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as m_i_i:
        movie_files_results_list = csv.reader(m_i_i)

        for movie_times in movie_files_results_list:
            movie_times_list.append(movie_times[8])
            all_media_times_list.append(movie_times[8])

    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as t_i_i:
        tv_files_results_list = csv.reader(t_i_i)

        for tv_show_times in tv_files_results_list:
            tv_times_list.append(tv_show_times[11])
            all_media_times_list.append(tv_show_times[11])

    movie_times_total = 0
    tv_times_total = 0

    for found_movie_times in movie_times_list:
        stripped_movie_time = found_movie_times.split('.')[-1]
        if stripped_movie_time == '':
            stripped_movie_time = 0

        movie_times_total = movie_times_total + int(stripped_movie_time)
    movie_times_total_readable_seconds = movie_times_total // 1000
    movie_times_total_readable_minutes = movie_times_total_readable_seconds // 60
    movie_times_total_readable_hours = movie_times_total_readable_minutes // 60
    movie_times_total_readable_years = movie_times_total_readable_hours / 8760
    rounded_movie_times_total_readable_years = round(movie_times_total_readable_years, 2)

    for found_tv_times in tv_times_list:
        stripped_tv_time = found_tv_times.split('.')[-1]
        if stripped_tv_time == '':
            stripped_tv_time = 0

        tv_times_total = tv_times_total + int(stripped_tv_time)
    tv_times_total_readable_seconds = tv_times_total // 1000
    tv_times_total_readable_minutes = tv_times_total_readable_seconds // 60
    tv_times_total_readable_hours = tv_times_total_readable_minutes // 60
    tv_times_total_readable_years = tv_times_total_readable_hours / 8760
    rounded_tv_times_total_readable_years = round(tv_times_total_readable_years, 2)

    all_media_times_total = int(movie_times_total) + int(tv_times_total)
    all_times_total_readable_seconds = all_media_times_total // 1000
    all_times_total_readable_minutes = all_times_total_readable_seconds // 60
    all_times_total_readable_hours = all_times_total_readable_minutes // 60
    all_times_total_readable_years = all_times_total_readable_hours / 8760
    rounded_all_times_total_readable_years = round(all_times_total_readable_years, 2)

    try:

        if int(time_queries_input_list[0]) == 0:
            media_index_home()

        elif int(time_queries_input_list[0]) == 1:

            print('TOTAL DURATION FOR ALL MOVIES (IN SECONDS): ', movie_times_total_readable_seconds)
            separator_1()
            print('TOTAL DURATION FOR ALL MOVIES (IN MINUTES): ', movie_times_total_readable_minutes)
            separator_1()
            print('TOTAL DURATION FOR ALL MOVIES (IN HOURS): ', movie_times_total_readable_hours)
            separator_2()
            print('TOTAL DURATION FOR ALL MOVIES (IN YEARS): ', rounded_movie_times_total_readable_years)
            separator_3()

        elif int(time_queries_input_list[0]) == 2:

            print('TOTAL DURATION FOR ALL TV SHOWS (IN SECONDS): ', tv_times_total_readable_seconds)
            separator_1()
            print('TOTAL DURATION FOR ALL TV SHOWS (IN MINUTES): ', tv_times_total_readable_minutes)
            separator_1()
            print('TOTAL DURATION FOR ALL TV SHOWS (IN HOURS): ', tv_times_total_readable_hours)
            separator_2()
            print('TOTAL DURATION FOR ALL TV SHOWS (IN YEARS): ', rounded_tv_times_total_readable_years)
            separator_3()

        elif int(time_queries_input_list[0]) == 3:

            print('TOTAL DURATION FOR ALL MOVIES (IN SECONDS): ', movie_times_total_readable_seconds)
            separator_1()
            print('TOTAL DURATION FOR ALL MOVIES (IN MINUTES): ', movie_times_total_readable_minutes)
            separator_1()
            print('TOTAL DURATION FOR ALL MOVIES (IN HOURS): ', movie_times_total_readable_hours)
            separator_2()
            print('TOTAL DURATION FOR ALL MOVIES (IN YEARS): ', rounded_movie_times_total_readable_years)
            separator_3()
            print('TOTAL DURATION FOR ALL TV SHOWS (IN SECONDS): ', tv_times_total_readable_seconds)
            separator_1()
            print('TOTAL DURATION FOR ALL TV SHOWS (IN MINUTES): ', tv_times_total_readable_minutes)
            separator_1()
            print('TOTAL DURATION FOR ALL TV SHOWS (IN HOURS): ', tv_times_total_readable_hours)
            separator_2()
            print('TOTAL DURATION FOR ALL TV SHOWS (IN YEARS): ', rounded_tv_times_total_readable_years)
            separator_3()
            print('TOTAL DURATION FOR ALL MEDIA (IN SECONDS): ', all_times_total_readable_seconds)
            separator_1()
            print('TOTAL DURATION FOR ALL MEDIA (IN MINUTES): ', all_times_total_readable_minutes)
            separator_1()
            print('TOTAL DURATION FOR ALL MEDIA (IN HOURS): ', all_times_total_readable_hours)
            separator_2()
            print('TOTAL DURATION FOR ALL MEDIA (IN YEARS): ', rounded_all_times_total_readable_years)
            separator_3()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


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


def total_media_library_amount():
    tv_amounts_list = []
    episode_amounts_list = []
    movie_amounts_list = []

    with open(os.path.expanduser((index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)),
              encoding='UTF-8') as m_t_i:
        media_index_list = list(csv.reader(m_t_i))
    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as t_f_p:
        tv_index_list = list(csv.reader(t_f_p))

        for counted_movie_title in media_index_list:
            if 'MOVIE' in counted_movie_title:
                movie_amounts_list.append(counted_movie_title)

        for counted_tv_title in media_index_list:
            if 'TV' in counted_tv_title:
                tv_amounts_list.append(counted_tv_title)

        for episodes in tv_index_list:
            if not episodes[0].lower().endswith('.nfo'):
                episode_amounts_list.append(+1)

        print('\n', 'TOTAL AMOUNT OF MOVIES: ', '\n')
        print(len(movie_amounts_list))
        separator_3()
        print('\n', 'TOTAL AMOUNT OF TV SHOWS: ', '\n')
        print(len(tv_amounts_list))
        print('\n', '\n', 'TOTAL AMOUNT OF TV EPISODES: ', '\n')
        print(len(episode_amounts_list))
        separator_3()
        print('\n', 'TOTAL AMOUNT OF ITEMS IN MEDIA-LIBRARY: ', '\n')
        print(len(movie_amounts_list) + len(episode_amounts_list))
        separator_3()


def total_tv_episodes_in_show():
    total_query_action_list = []
    tv_amounts = []
    tv_show_episodes_found = []
    tv_show_found = {}

    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)),
              encoding='UTF-8') as t_i_i:
        tv_results_list = list(csv.reader(t_i_i))

        try:

            tv_total_query_action = input('ENTER TV SHOW TITLE: ')
            separator_3()
            total_query_action_list.append(tv_total_query_action.lower())

        except (OSError, TypeError, ValueError) as e:
            print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')

        for tv_title in tv_results_list:
            tv_amounts.append(tv_title[2])

        for found_tv_title in tv_amounts:
            if total_query_action_list[0] in found_tv_title.lower():
                tv_show_episodes_found.append(found_tv_title)
                tv_show_found[found_tv_title] = tv_show_episodes_found.count(found_tv_title)

        for episode in tv_show_found.items():
            print('TITLE NAME: NUMBER (#) OF EPISODES: ', '\n', episode)
            separator_3()
        print('NUMBER (#) OF EPISODES TOTAL: ', sum(tv_show_found.values()))
        separator_3()


def username_check_and_folder_creation():
    try:

        global movie_dir_input, tv_dir_input, movie_alt_dir_input, tv_alt_dir_input
        user_info_file = os.path.expanduser((index_folder + '/{0}_USER_INFO.json').format(username))

        if os.path.isfile(user_info_file):
            with open(user_info_file) as u_i_f:
                user_data = json.load(u_i_f)
                _ = user_data['user:']
                movie_dir_input = user_data['movie_dir:']
                tv_dir_input = user_data['tv_dir:']
                movie_alt_dir_input = user_data['movie_alt_dir:']
                tv_alt_dir_input = user_data['tv_alt_dir:']

        else:
            os.makedirs(os.path.expanduser((index_folder + '/').format(username)), exist_ok=True)
            os.makedirs(os.path.expanduser((index_folder + '/FILES').format(username)), exist_ok=True)
            os.makedirs(os.path.expanduser((index_folder + '/GRAPHS').format(username)), exist_ok=True)
            os.makedirs(os.path.expanduser((index_folder + '/RESULTS').format(username)), exist_ok=True)
            os.makedirs(os.path.expanduser((index_folder + '/SEARCH').format(username)), exist_ok=True)
            directory_selection()

    except (OSError, TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
        separator_3()
        main()


def walk_directories_and_create_indices(input_file_0, input_file_1):
    movie_video_files_results = []
    tv_show_video_files_results = []

    path_scan_start = time.time()

    try:

        if movie_dir_input != '':
            for root, dirs, files in os.walk(movie_dir_input):
                directory = str(pathlib.Path(root).as_posix())
                if '/featurettes' not in directory.lower():
                    for movie_file in sorted(files):
                        if movie_file.lower().endswith(extensions):
                            movie_video_files_results.append([(pathlib.Path(root) / movie_file).as_posix()])

        if movie_alt_dir_input != '':
            for listed_alternate_movie_directories in movie_alt_dir_input:
                for root, dirs, files in os.walk(listed_alternate_movie_directories):
                    directory = str(pathlib.Path(root).as_posix())
                    if '/featurettes' not in directory.lower():
                        for alt_movie_file in sorted(files):
                            if alt_movie_file.lower().endswith(extensions):
                                movie_video_files_results.append([(pathlib.Path(root) / alt_movie_file).as_posix()])

        with open(os.path.expanduser((index_folder + input_file_0).format(username)), 'w',
                  encoding='UTF-8', newline='') as m_f_p:
            csv_writer = csv.writer(m_f_p)
            for movie_row in sorted(movie_video_files_results):
                csv_writer.writerow(movie_row)

        if tv_dir_input != '':
            for root, dirs, files in os.walk(tv_dir_input):
                directory = str(pathlib.Path(root).as_posix())
                if '/featurettes' not in directory.lower():
                    for tv_file in sorted(files):
                        if tv_file.lower().endswith(extensions):
                            tv_show_video_files_results.append([(pathlib.Path(root) / tv_file).as_posix()])

        if tv_alt_dir_input != '':
            for listed_alternate_tv_directories in tv_alt_dir_input:
                for root, dirs, files in os.walk(listed_alternate_tv_directories):
                    directory = str(pathlib.Path(root).as_posix())
                    if '/featurettes' not in directory.lower():
                        for alt_tv_file in sorted(files):
                            if alt_tv_file.lower().endswith(extensions):
                                tv_show_video_files_results.append([(pathlib.Path(root) / alt_tv_file).as_posix()])

        with open(os.path.expanduser((index_folder + input_file_1).format(username)), 'w',
                  encoding='UTF-8', newline='') as t_f_p:
            csv_writer = csv.writer(t_f_p)
            for tv_row in sorted(tv_show_video_files_results):
                csv_writer.writerow(tv_row)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n')
        separator_3()

    path_scan_end = time.time()
    readable_path_scan_time = round(path_scan_end - path_scan_start, 2)
    print('MEDIA PATHS SCAN COMPLETE - TIME ELAPSED: ', readable_path_scan_time, 'Seconds')
    separator_3()


if __name__ == '__main__':
    main()
