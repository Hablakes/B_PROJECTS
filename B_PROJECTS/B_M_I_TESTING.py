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
    create_tv_show_information_index()


def create_tv_show_information_index():
    tv_scan_start = time.time()
    ia = IMDb()
    tv_overview_plots_nfo_list = []
    tv_episodes_plots_nfo_list = []

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as m_f_p:
        tv_index = csv.reader(m_f_p)

        for tv_file in sorted(tv_index):
            tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
            tv_title_key = tv_file[0].rsplit('/')[-2]

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

                search_confidence_percentage, tv_info_set = find_imdb_show(tv_title_key)
                try:

                    tv_info_set = None

                    tv_imdb = ia.search_movie(tv_title_key)

                    possible_tv_show_matches_list = []

                    for found_tv_plots in tv_imdb:
                        if found_tv_plots['kind'] != 'tv series':
                            continue

                        search_confidence_percentage = match_similar_strings(tv_title_key.lower(),
                                                                             found_tv_plots['title'].lower())

                        possible_tv_show_matches = \
                            (found_tv_plots['title'], found_tv_plots.movieID, search_confidence_percentage)
                        possible_tv_show_matches_list.append(possible_tv_show_matches)

                    possible_tv_show_matches_list.sort(key=lambda x: x[2], reverse=True)

                    if possible_tv_show_matches_list:

                        tv_id = possible_tv_show_matches_list[0][1]
                        tv_info_set = ia.get_movie(tv_id)

                        tv_results_list[tv_file[0]]['SEARCH CONFIDENCE PERCENTAGE'] = search_confidence_percentage

                except (IOError, KeyError, TypeError, ValueError) as e:
                    print('IMDB MATCH ERROR: TV SHOW FILE(S): ', e)
                    print('-' * 100, '\n')
                    continue

                tv_folders_list = []

                if tv_title_key not in tv_folders_list:
                    tv_folders_list.append(tv_title_key)

                try:

                    for found_tv_plots in tv_folders_list:

                        if tv_info_set:

                            ia.update(tv_info_set, 'episodes')
                            item_title = tv_info_set.get('title')
                            item_year = tv_info_set.get('year')

                            if 'plot' in tv_info_set:
                                item_plot = tv_info_set['plot']

                            if item_title not in tv_overview_plots_dict:
                                tv_overview_plots_dict[found_tv_plots] = {}
                                tv_overview_plots_dict[found_tv_plots]['SHOW'] = str(
                                    str(item_title) + ' (' + str(item_year) + ')')
                                tv_overview_plots_dict[found_tv_plots]['PLOT'] = item_plot[0].split('::')[0].strip()

                except (IOError, KeyError, TypeError, ValueError) as e:
                    print('TV SHOW OVERVIEW INFO ERROR: TV SHOW FILE(S): ', e)
                    print('-' * 100, '\n')

                if found_tv_plots not in tv_overview_plots_dict:
                    tv_overview_plots_dict[found_tv_plots] = {}
                    tv_overview_plots_dict[found_tv_plots]['SHOW'] = found_tv_plots
                    tv_overview_plots_dict[found_tv_plots]['PLOT'] = 'NO PLOT AVAILABLE'

                try:

                    if tv_info_set and float(search_confidence_percentage) >= 0.40:

                        ia.update(tv_info_set, 'episodes')
                        tv_show_title = tv_info_set.get('title')

                        if 'episodes' in tv_info_set:
                            episode_title = tv_info_set['episodes'][g_season_number][g_episode_number].get('title')
                            episode_year = tv_info_set['episodes'][g_season_number][g_episode_number].get('year')
                            episode_plot = tv_info_set['episodes'][g_season_number][g_episode_number].get('plot')
                            episode_rating = tv_info_set['episodes'][g_season_number][g_episode_number].get('rating')

                        tv_results_list[tv_file[0]]['GUESSIT SEARCH TERM'] = g_tv_title_to_query
                        tv_results_list[tv_file[0]]['TV SHOW ID #'] = tv_id
                        tv_results_list[tv_file[0]]['TV SHOW TITLE'] = tv_show_title
                        tv_results_list[tv_file[0]]['SEASON #'] = g_season_number
                        tv_results_list[tv_file[0]]['EPISODE #'] = g_episode_number
                        tv_results_list[tv_file[0]]['EPISODE TITLE'] = episode_title
                        tv_results_list[tv_file[0]]['YEAR'] = episode_year
                        tv_results_list[tv_file[0]]['PLOT'] = episode_plot.split('::')[0].strip()
                        tv_results_list[tv_file[0]]['RATING'] = round(episode_rating, 2)

                        tv_results_list[tv_file[0]]['GENRES'] = []
                        for genre in tv_info_set['genres']:
                            tv_results_list[tv_file[0]]['GENRES'].append(genre)

                    elif tv_info_set is None:

                        print('TV SHOW EPISODE - NO MATCH -', tv_file[0])
                        separator_3()

                        tv_results_list[tv_file[0]]['GUESSIT SEARCH TERM'] = g_tv_title_to_query
                        tv_results_list[tv_file[0]]['TV SHOW ID #'] = 'NO MATCH'
                        if g_tv_title_to_query:
                            tv_results_list[tv_file[0]]['TV SHOW TITLE'] = g_tv_title_to_query
                        else:
                            tv_results_list[tv_file[0]]['TV SHOW TITLE'] = 'NO MATCH'
                        if g_season_number:
                            tv_results_list[tv_file[0]]['SEASON #'] = g_season_number
                        else:
                            tv_results_list[tv_file[0]]['SEASON #'] = 'NO MATCH'
                        if g_episode_number:
                            tv_results_list[tv_file[0]]['EPISODE #'] = g_episode_number
                        else:
                            tv_results_list[tv_file[0]]['EPISODE #'] = 'NO MATCH'
                        if g_tv_episode_title:
                            tv_results_list[tv_file[0]]['EPISODE TITLE'] = g_tv_episode_title
                        else:
                            tv_results_list[tv_file[0]]['EPISODE TITLE'] = 'NO MATCH'
                        tv_results_list[tv_file[0]]['YEAR'] = 'NO MATCH'
                        tv_results_list[tv_file[0]]['PLOT'] = 'NO MATCH'
                        tv_results_list[tv_file[0]]['RATING'] = 'NO MATCH'
                        if not tv_results_list[tv_file[0]]['RUN-TIME']:
                            tv_results_list[tv_file[0]]['RUN-TIME'] = 'NO MATCH'
                        tv_results_list[tv_file[0]]['GENRES'] = 'NO MATCH'
                        tv_results_list[tv_file[0]]['SEARCH CONFIDENCE PERCENTAGE'] = 'NO MATCH'

                except (IOError, KeyError, TypeError, ValueError) as e:
                    print('TV SHOW INFO ERROR: TV SHOW FILE(S): ', e)
                    print('-' * 100, '\n')
                    continue

    for found_tv_plots in tv_overview_plots_dict.items():

        if str(found_tv_plots[1]['SHOW']).lower() == str(tv_title_key).lower():
            if str(found_tv_plots[1]['PLOT']).lower() == str('NO PLOT AVAILABLE').lower():
                tv_overview_plots_nfo_list.append(found_tv_plots)

    for plot_review_items in tv_overview_plots_nfo_list:

        with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
                  encoding='UTF-8') as m_f_p_2:
            tv_index = csv.reader(m_f_p_2)

            for checked_tv_file in sorted(tv_index):
                tv_filename_key = checked_tv_file[0].rsplit('/', 1)[-1]
                tv_title_key = checked_tv_file[0].rsplit('/')[-2]

                if str(tv_title_key).lower() in str(plot_review_items[0]).lower():
                    if str(tv_filename_key).lower() == str('tvshow.nfo').lower():
                        try:

                            with open(checked_tv_file[0]) as o_f:

                                for line in o_f.readlines():
                                    if '<plot>' in line:
                                        formatted_plot = remove_html_tags(line)
                                        tv_overview_plots_dict[tv_title_key]['PLOT'] = formatted_plot.strip()

                        except (IOError, KeyError, TypeError, ValueError) as e:
                            print('TV SHOW NFO SCRAPE ERROR: TV SHOW FILE(S): ', e)
                            print('-' * 100, '\n')
                            continue

    for found_tv_shows in tv_results_list.items():

        if str(found_tv_shows[1]['FOLDER-NAME']).lower() == str(tv_title_key).lower():
            if str(found_tv_shows[1]['PLOT']).lower() == str('NO MATCH').lower():
                print(found_tv_shows)

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


def find_imdb_show(show_name):
    ia = IMDb()
    search_confidence_percentage = 0

    tv_imdb = ia.search_movie(show_name)

    possible_tv_show_matches_list = []

    for found_tv_plots in tv_imdb:
        if found_tv_plots['kind'] != 'tv series':
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
        return search_confidence_percentage, tv_info_set
    return None


def launch_media_index():
    print(pyfiglet.figlet_format('MEDIA_INDEX', font='cybermedium'))
    separator_3()

    try:

        global username
        username = 'TESTING'
        # username = input('ENTER YOUR USERNAME (CASE-SENSITIVE): ')
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


def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


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
