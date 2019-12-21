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

import matplotlib.pylab as plt

from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
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


def main():
    separator_3()
    launch_media_index()

    while True:
        media_index_home()


def change_directory_selection():
    print(pyfiglet.figlet_format('CHANGE_DIRECTORY', font='cybermedium'))
    separator_3()
    directory_selection()


def create_media_information_indices():
    create_tv_information_index()


def create_tv_information_index():
    tv_results_list = {}
    tv_overview_plots_dict = {}

    tv_scan_start = time.time()
    ia = IMDb()

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as m_f_p:
        tv_index = csv.reader(m_f_p)

        for tv_file in sorted(tv_index):
            try:

                tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
                tv_title_key = tv_file[0].rsplit('/')[-2]

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
                        print('OS ERROR / FILE-SIZE: ', e)
                        print('-' * 100, '\n')
                        continue

                    tv_hash = str(str(tv_filename_key) + '_' + str(tv_file_size))
                    tv_results_list[tv_file[0]]['TV-HASH'] = tv_hash

                    try:

                        tv_title = guessit.guessit(tv_filename_key, options={'type': 'episode'})

                        tv_title_to_query = tv_title.get('title')

                        g_season_number = tv_title.get('season')
                        g_episode_number = tv_title.get('episode')
                        tv_results_list[tv_file[0]]['FILE-TYPE'] = tv_title.get('container')

                    except OSError as e:
                        print('OS ERROR / GUESSIT: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        if r"'s " in tv_title_to_query:
                            formatted_tv_title_to_query = tv_title_to_query.rsplit(r"'s ", 1)
                            tv_title_to_query = ' '.join(formatted_tv_title_to_query)

                    except OSError as e:
                        print('OS ERROR / TITLE FORMATTING: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        tv_media_info = pymediainfo.MediaInfo.parse(tv_file[0])

                    except OSError as e:
                        print('OS ERROR / PY_MEDIA_INFO: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        for track in tv_media_info.tracks:
                            if track.track_type == 'General':
                                duration_integer = track.duration
                                tv_results_list[tv_file[0]]['RUN-TIME'] = duration_integer

                            elif track.track_type == 'Video':
                                tv_results_list[tv_file[0]]['RESOLUTION'] = str(track.width) + 'x' + str(track.height)

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('OS ERROR / PY_MEDIA_INFO (TRACKS): ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        tv_imdb = ia.search_movie(tv_title_to_query)

                    except (IOError, KeyError, TypeError, ValueError) as e:
                        print('IMDB SEARCH ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                        print('-' * 100, '\n')
                        continue

                    try:

                        tv_id = tv_imdb[0].movieID

                    except (IOError, KeyError, TypeError, ValueError) as e:
                        print('IMDB ID# ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                        print('-' * 100, '\n')
                        continue

                    try:

                        tv_info_set = ia.get_movie(tv_id)

                    except (IOError, KeyError, TypeError, ValueError) as e:
                        print('IMDB INFOSET ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                        print('-' * 100, '\n')
                        continue

                    try:

                        search_confidence_percentage = match_similar_strings(tv_title_to_query.lower(),
                                                                             tv_imdb[0]['title'].lower())
                        tv_results_list[tv_file[0]]['SEARCH CONFIDENCE PERCENTAGE'] = search_confidence_percentage

                    except (IOError, KeyError, TypeError, ValueError) as e:
                        print('CONFIDENCE PERCENTAGE ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                        print('-' * 100, '\n')
                        continue

                    if float(search_confidence_percentage) >= 0.65:

                        try:

                            ia.update(tv_info_set, 'episodes')

                        except (IOError, KeyError, TypeError, ValueError) as e:
                            print('IMDB TV SHOW SEARCH ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                            print('-' * 100, '\n')
                            continue

                        try:

                            tv_show_title = tv_info_set['title']
                            tv_show_year = tv_info_set['year']
                            tv_show_plot = tv_info_set['plot']
                            episode_title = tv_info_set['episodes'][g_season_number][g_episode_number]['title']
                            episode_year = tv_info_set['episodes'][g_season_number][g_episode_number]['year']
                            episode_plot = tv_info_set['episodes'][g_season_number][g_episode_number]['plot']
                            episode_rating = tv_info_set['episodes'][g_season_number][g_episode_number]['rating']

                        except (IOError, KeyError, TypeError, ValueError) as e:
                            print('IMDB TV EPISODE SEARCH ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                            print('-' * 100, '\n')
                            continue

                        try:

                            if tv_show_title not in tv_overview_plots_dict:
                                tv_overview_plots_dict[tv_show_title] = {}
                                tv_overview_plots_dict[tv_show_title]['SHOW'] = str(str(tv_show_title) + ' (' +
                                                                                    str(tv_show_year) + ')')
                                tv_overview_plots_dict[tv_show_title]['PLOT'] = tv_show_plot[0].split('::')[0]

                        except (IOError, KeyError, TypeError, ValueError) as e:
                            print('TV SHOW OVERVIEW PLOT(S) ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                            print('-' * 100, '\n')
                            continue

                        try:

                            tv_results_list[tv_file[0]]['GUESSIT SEARCH TERM'] = tv_title_to_query
                            tv_results_list[tv_file[0]]['TV SHOW ID #'] = tv_id
                            tv_results_list[tv_file[0]]['TV SHOW TITLE'] = tv_show_title
                            tv_results_list[tv_file[0]]['SEASON #'] = g_season_number
                            tv_results_list[tv_file[0]]['EPISODE #'] = g_episode_number
                            tv_results_list[tv_file[0]]['EPISODE TITLE'] = episode_title
                            tv_results_list[tv_file[0]]['YEAR'] = episode_year
                            tv_results_list[tv_file[0]]['PLOT'] = episode_plot.split('::')[0]
                            tv_results_list[tv_file[0]]['RATING'] = round(episode_rating, 2)
                            tv_results_list[tv_file[0]]['RUN-TIME'] = duration_integer

                        except (IOError, KeyError, TypeError, ValueError) as e:
                            print('IMDB GENERAL INFO ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                            print('-' * 100, '\n')
                            continue

                        try:

                            tv_results_list[tv_file[0]]['GENRES'] = []
                            for genre in tv_info_set['genres']:
                                tv_results_list[tv_file[0]]['GENRES'].append(genre)

                        except (IOError, KeyError, TypeError, ValueError) as e:
                            print('IMDB GENRE ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                            print('-' * 100, '\n')
                            continue

                    else:

                        print('TV SHOW - NO MATCH -', tv_file[0])
                        separator_3()

                        tv_results_list[tv_file[0]]['GUESSIT SEARCH TERM'] = tv_title_to_query
                        tv_results_list[tv_file[0]]['TV SHOW ID #'] = []
                        tv_results_list[tv_file[0]]['TV SHOW TITLE'] = []
                        tv_results_list[tv_file[0]]['SEASON #'] = g_season_number
                        tv_results_list[tv_file[0]]['EPISODE #'] = g_episode_number
                        tv_results_list[tv_file[0]]['EPISODE TITLE'] = []
                        tv_results_list[tv_file[0]]['YEAR'] = []
                        tv_results_list[tv_file[0]]['PLOT'] = []
                        tv_results_list[tv_file[0]]['RATING'] = []
                        tv_results_list[tv_file[0]]['RUN-TIME'] = duration_integer
                        tv_results_list[tv_file[0]]['GENRES'] = []

                        try:

                            tv_show_title = tv_title_to_query

                            if tv_show_title not in tv_overview_plots_dict:
                                tv_overview_plots_dict[tv_show_title] = {}
                                tv_overview_plots_dict[tv_show_title]['SHOW'] = tv_title_to_query
                                tv_overview_plots_dict[tv_show_title]['PLOT'] = str('NO PLOT AVAILABLE')

                        except (IOError, KeyError, TypeError, ValueError) as e:
                            print('TV SHOW OVERVIEW PLOT(S) ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                            print('-' * 100, '\n')
                            continue

            except (IOError, KeyError, TypeError, ValueError) as e:
                print('INPUT ERROR: ', e, '\n', 'TV SHOW FILE(S): ', tv_file[0])
                print('-' * 100, '\n')
                continue

    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as m_i_i:

        csv_writer = csv.DictWriter(m_i_i, ['MEDIA-PATH', 'MEDIA-TYPE', 'FOLDER-NAME', 'FILE-NAME', 'FILE-SIZE',
                                            'FILE-TYPE', 'RESOLUTION', 'GUESSIT SEARCH TERM', 'TV SHOW ID #',
                                            'TV SHOW TITLE', 'SEASON #', 'EPISODE #', 'EPISODE TITLE', 'YEAR', 'PLOT',
                                            'RATING', 'RUN-TIME', 'GENRES', 'SEARCH CONFIDENCE PERCENTAGE', 'TV-HASH'])

        for tv_row in tv_results_list.values():
            csv_writer.writerow(tv_row)

    with open(os.path.expanduser((index_folder + '/TV_PLOTS_INDEX.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as t_p_i:
        csv_writer = csv.DictWriter(t_p_i, ['SHOW', 'PLOT'])
        for tv_row in tv_overview_plots_dict.values():
            csv_writer.writerow(tv_row)

    tv_scan_end = time.time()
    readable_tv_scan_time = round(tv_scan_end - tv_scan_start, 2)
    print('TV INFORMATION SCAN COMPLETE - TIME ELAPSED: ', readable_tv_scan_time, 'Seconds')
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


def media_index_home():
    print(pyfiglet.figlet_format('MEDIA_INDEX', font='cybermedium'))
    separator_3()

    print('1) ADD / CHANGE DATABASE DIRECTORIES             2) CREATE PATH INDICES', '\n')
    print('3) CREATE / UPDATE MEDIA INFORMATION INDICES', '\n')
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
                print('1) CHANGE DATABASE DIRECTORIES                       0) MAIN MENU')
                separator_3()
                db_scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if db_scan_sub_input == 0:
                    media_index_home()

                elif db_scan_sub_input == 1:
                    change_directory_selection()

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

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


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
            os.makedirs(os.path.expanduser((index_folder + '/SEARCH').format(username)), exist_ok=True)
            directory_selection()

    except (OSError, TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
        separator_3()
        main()


def walk_directories_and_create_indices():
    movie_video_files_results = []

    media_folders_to_skip = 'extras', 'featurettes', 'special features'

    path_scan_start = time.time()

    if movie_dir_input != '':
        for root, dirs, files in os.walk(movie_dir_input):
            directory = str(pathlib.Path(root).as_posix())
            if not directory.rsplit('/')[-1].lower() in media_folders_to_skip:
                for movie_file in sorted(files):
                    if movie_file.lower().endswith(extensions):
                        movie_video_files_results.append([(pathlib.Path(root) / movie_file).as_posix()])

    if movie_alt_dir_input != '':
        for listed_alternate_movie_directories in movie_alt_dir_input:
            for root, dirs, files in os.walk(listed_alternate_movie_directories):
                directory = str(pathlib.Path(root).as_posix())
                if not directory.rsplit('/')[-1].lower() in media_folders_to_skip:
                    for alt_movie_file in sorted(files):
                        if alt_movie_file.lower().endswith(extensions):
                            movie_video_files_results.append([(pathlib.Path(root) / alt_movie_file).as_posix()])

    with open(os.path.expanduser((index_folder + '/MOVIE_VIDEO_FILES_PATHS.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as m_f_p:
        csv_writer = csv.writer(m_f_p)
        for movie_row in sorted(movie_video_files_results):
            csv_writer.writerow(movie_row)

    tv_show_video_files_results = []

    if tv_dir_input != '':
        for root, dirs, files in os.walk(tv_dir_input):
            directory = str(pathlib.Path(root).as_posix())
            if not directory.rsplit('/')[-1].lower() in media_folders_to_skip:
                for tv_file in sorted(files):
                    if tv_file.lower().endswith(extensions):
                        tv_show_video_files_results.append([(pathlib.Path(root) / tv_file).as_posix()])

    if tv_alt_dir_input != '':
        for listed_alternate_tv_directories in tv_alt_dir_input:
            for root, dirs, files in os.walk(listed_alternate_tv_directories):
                directory = str(pathlib.Path(root).as_posix())
                if not directory.rsplit('/')[-1].lower() in media_folders_to_skip:
                    for alt_tv_file in sorted(files):
                        if alt_tv_file.lower().endswith(extensions):
                            tv_show_video_files_results.append([(pathlib.Path(root) / alt_tv_file).as_posix()])

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as t_f_p:
        csv_writer = csv.writer(t_f_p)
        for tv_row in sorted(tv_show_video_files_results):
            csv_writer.writerow(tv_row)

    path_scan_end = time.time()
    readable_path_scan_time = round(path_scan_end - path_scan_start, 2)
    print('MEDIA PATHS SCAN COMPLETE - TIME ELAPSED: ', readable_path_scan_time, 'Seconds')
    separator_3()


if __name__ == '__main__':
    main()
