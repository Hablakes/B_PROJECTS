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
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from difflib import SequenceMatcher
from lxml import html
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


def compare_results(results_one, results_two):
    output_one = []

    for line in results_one:
        if line not in results_two:
            output_one.append('REMOVAL: ' + line)

    for line in results_two:
        if line not in results_one:
            output_one.append('ADDITION: ' + line)

    return output_one


def create_media_information_indices():
    create_movie_information_index()


def create_movie_information_index():
    movie_results_list = {}

    movie_scan_start = time.time()

    with open(os.path.expanduser((index_folder + '/MOVIE_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as m_f_p:
        movie_index = csv.reader(m_f_p)

        for movie_file in sorted(movie_index):
            try:

                if not movie_file[0].split('/', 1)[-1].lower().endswith('.nfo'):

                    movie_filename_key = movie_file[0].split('/')[-1]
                    movie_folder_key = movie_file[0].split('/')[-2]
                    movie_file_type_key = movie_filename_key.rsplit('.')[-1]

                    if movie_file[0] not in movie_results_list:
                        movie_results_list[movie_file[0]] = {}

                    try:

                        if re.findall(r'\([1-2]\d{3}\)', movie_filename_key):
                            movie_title_key = movie_filename_key.split('(')[0]
                        elif re.findall(r'\(\d{4}\)', movie_filename_key):
                            movie_title_key = movie_filename_key.split('(')[0]
                        else:
                            movie_title_key = guessit.guessit(movie_filename_key)
                            movie_title_key = movie_title_key.get('title')

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('ERROR / TITLE: ', e)
                        print('-' * 100, '\n')
                        continue

                    movie_results_list[movie_file[0]]['MEDIA-PATH'] = movie_file[0]
                    movie_results_list[movie_file[0]]['MEDIA-TYPE'] = str('MOVIE')
                    movie_results_list[movie_file[0]]['FOLDER-NAME'] = movie_folder_key
                    movie_results_list[movie_file[0]]['FILE-NAME'] = movie_filename_key
                    movie_results_list[movie_file[0]]['FILE-TYPE'] = movie_file_type_key
                    movie_results_list[movie_file[0]]['MOVIE-TITLE'] = movie_title_key

                    try:

                        if re.findall(r'\(\d{4}\)', movie_filename_key):
                            movie_year_key = re.findall(r'\(\d{4}\)', movie_filename_key)

                            if type(movie_year_key) is list:
                                movie_results_list[movie_file[0]]['YEAR'] = movie_year_key[0][1:-1]

                            elif type(movie_year_key) is not list:
                                movie_results_list[movie_file[0]]['YEAR'] = movie_year_key[1:-1]

                        else:
                            movie_results_list[movie_file[0]]['YEAR'] = str('NO YEAR FOUND IN TITLE')

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('ERROR / YEAR: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        if re.findall(r'\d{3}x\d{2}', movie_filename_key):
                            movie_resolution_key = \
                                movie_filename_key.rsplit('.')[-2].rsplit(' ')[-1]
                            movie_resolution_no_parenthesis_key = movie_resolution_key[1:-1]

                            movie_results_list[movie_file[0]]['RESOLUTION'] = movie_resolution_no_parenthesis_key

                        else:
                            movie_results_list[movie_file[0]]['RESOLUTION'] = str('NO RESOLUTION FOUND IN TITLE')

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('ERROR / RESOLUTION: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        movie_file_size = os.path.getsize(movie_file[0])
                        movie_file_size_in_mb = (int(movie_file_size) / 1048576)
                        movie_file_size_in_mb_rounded = str(round(movie_file_size_in_mb, 2))
                        movie_hash = str(str(movie_filename_key) + '_' + str(movie_file_size))

                        movie_results_list[movie_file[0]]['FILE-SIZE'] = movie_file_size_in_mb_rounded
                        movie_results_list[movie_file[0]]['MOVIE-HASH'] = movie_hash

                    except OSError as e:
                        print('ERROR / FILE-SIZE: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        movie_media_info = pymediainfo.MediaInfo.parse(movie_file[0])

                    except OSError as e:
                        print('ERROR / PY_MEDIA_INFO: ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        for track in movie_media_info.tracks:

                            if track.track_type == 'General':
                                duration_integer = track.duration
                                movie_results_list[movie_file[0]]['RUN-TIME'] = duration_integer

                        if movie_results_list[movie_file[0]]['RESOLUTION'] == str('NO RESOLUTION FOUND IN TITLE'):

                            for track in movie_media_info.tracks:

                                if track.track_type == 'Video':
                                    movie_results_list[movie_file[0]]['RESOLUTION'] = \
                                        str(track.width) + 'x' + str(track.height)

                    except (KeyError, OSError, TypeError, ValueError) as e:
                        print('ERROR / PY_MEDIA_INFO (TRACKS): ', e)
                        print('-' * 100, '\n')
                        continue

                    try:

                        movie_to_search = r'https://www.imdb.com/search/title/?title=' + str(movie_title_key).lower()
                        movie_response = requests.get(movie_to_search, timeout=5)
                        movie_imdb_page = BeautifulSoup(movie_response.text, 'html.parser')
                        movie_body_text = movie_imdb_page.find('div', class_='lister list detail sub-list')
                        movie_title_and_id_sections = movie_body_text.find_all(class_='lister-item mode-advanced')

                    except (Exception, KeyError, OSError, TypeError, ValueError) as e:
                        print('ERROR / IMDB SEARCH: ', e)
                        print('-' * 100, '\n')
                        continue

                    for search_results in movie_title_and_id_sections:
                        title = search_results.h3.a.text

                        movie_search_confidence = round(
                            match_similar_strings(title.lower(), str(movie_title_key).lower()), 2)

                        if float(movie_search_confidence) >= 0.85:
                            if movie_results_list[movie_file[0]]['YEAR'] == str('NO YEAR FOUND IN TITLE'):
                                year = search_results.find('span', class_='lister-item-year text-muted unbold')
                                movie_results_list[movie_file[0]]['YEAR'] = year.text
                            movie_title = title
                            certificate = search_results.find('span', class_='certificate')
                            genre = search_results.find('span', class_='genre')
                            imdb_id = search_results.img['data-tconst']
                            plot_section = search_results.find_all('p')
                            plot = plot_section[1]
                            rating = search_results.strong

                            movie_results_list[movie_file[0]]['IMDB-ID'] = imdb_id
                            movie_results_list[movie_file[0]]['TITLE'] = movie_title
                            movie_results_list[movie_file[0]]['CERTIFICATE'] = certificate.text
                            movie_results_list[movie_file[0]]['GENRE(S)'] = genre.text
                            movie_results_list[movie_file[0]]['PLOT'] = plot.text
                            movie_results_list[movie_file[0]]['RATING'] = rating.text
                            movie_results_list[movie_file[0]]['SEARCH-CONFIDENCE'] = movie_search_confidence
                            break

                    print('PATH: ', movie_results_list[movie_file[0]]['MEDIA-PATH'])
                    print('TYPE: ', movie_results_list[movie_file[0]]['MEDIA-TYPE'])
                    print('FOLDER: ', movie_results_list[movie_file[0]]['FOLDER-NAME'])
                    print('FILE-NAME: ', movie_results_list[movie_file[0]]['FILE-NAME'])
                    print('FILE-TYPE: ', movie_results_list[movie_file[0]]['FILE-TYPE'])
                    print('MOVIE-TITLE: ', movie_results_list[movie_file[0]]['MOVIE-TITLE'])
                    if movie_results_list[movie_file[0]]['YEAR']:
                        print('YEAR: ', movie_results_list[movie_file[0]]['YEAR'])
                    if movie_results_list[movie_file[0]]['RESOLUTION']:
                        print('RESOLUTION: ', movie_results_list[movie_file[0]]['RESOLUTION'])
                    if movie_results_list[movie_file[0]]['FILE-SIZE']:
                        print('FILE-SIZE: ', movie_results_list[movie_file[0]]['FILE-SIZE'])
                    if movie_results_list[movie_file[0]]['RUN-TIME']:
                        print('RUN-TIME: ', movie_results_list[movie_file[0]]['RUN-TIME'])
                    if movie_results_list[movie_file[0]]['IMDB-ID']:
                        print('IMDB-ID: ', movie_results_list[movie_file[0]]['IMDB-ID'])
                    if movie_results_list[movie_file[0]]['TITLE']:
                        print('TITLE: ', movie_results_list[movie_file[0]]['TITLE'])
                    if movie_results_list[movie_file[0]]['CERTIFICATE']:
                        print('CERTIFICATE: ', movie_results_list[movie_file[0]]['CERTIFICATE'])
                    if movie_results_list[movie_file[0]]['GENRE(S)']:
                        print('GENRE(S): ', movie_results_list[movie_file[0]]['GENRE(S)'])
                    if movie_results_list[movie_file[0]]['PLOT']:
                        print('PLOT: ', movie_results_list[movie_file[0]]['PLOT'])
                    if movie_results_list[movie_file[0]]['PLOT']:
                        print('RATING: ', movie_results_list[movie_file[0]]['RATING'])
                    if movie_results_list[movie_file[0]]['RATING']:
                        print('SEARCH-CONFIDENCE: ', movie_results_list[movie_file[0]]['SEARCH-CONFIDENCE'])
                    if movie_results_list[movie_file[0]]['MOVIE-HASH']:
                        print('MOVIE-HASH: ', movie_results_list[movie_file[0]]['MOVIE-HASH'])
                    separator_2()

            except (IOError, KeyError, TypeError, ValueError) as e:
                print('INPUT ERROR: ', e, '\n', 'MOVIE FILE(S): ', movie_file[0])
                print('-' * 100, '\n')
                continue

    with open(os.path.expanduser((index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as m_i_i:

        csv_writer = csv.DictWriter(m_i_i, ['MEDIA-PATH', 'MEDIA-TYPE', 'FOLDER-NAME', 'FILE-NAME', 'FILE-TYPE',
                                            'MOVIE-TITLE', 'YEAR', 'RESOLUTION', 'RESOLUTION', 'FILE-SIZE', 'RUN-TIME',
                                            'IMDB-ID', 'TITLE', 'CERTIFICATE', 'GENRE(S)', 'PLOT', 'RATING',
                                            'SEARCH-CONFIDENCE', 'MOVIE-HASH'])

        for movie_row in movie_results_list.values():
            csv_writer.writerow(movie_row)

    movie_scan_end = time.time()
    readable_movie_scan_time = round(movie_scan_end - movie_scan_start, 2)
    print('MOVIE INFORMATION SCAN COMPLETE - TIME ELAPSED: ', readable_movie_scan_time, 'Seconds')
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
        username = 'TEST'
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
    print('3) CREATE / UPDATE MEDIA INFORMATION INDICES     4) COMPARE TWO USERS INFORMATION INDICES', '\n')
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

        elif lmi_input_action == 4:

            try:

                print('CONFIRM: ')
                separator_1()
                print('1) COMPARE USER(S) INFORMATION INDICES               0) MAIN MENU')
                separator_3()
                comparison_scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if comparison_scan_sub_input == 0:
                    media_index_home()

                elif comparison_scan_sub_input == 1:
                    select_users_indices_to_compare()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


def select_users_indices_to_compare():
    try:

        print('\n', 'SELECT THE MOVIE_INFORMATION_INDICES TO COMPARE: ')
        separator_3()

        print('SELECT USER MOVIE INFORMATION INDEX: ')
        m_0 = tk_gui_file_selection_window()

        print('SELECT COMPARISON MOVIE INFORMATION INDEX: ')
        m_1 = tk_gui_file_selection_window()

        print('SELECT USER TV INFORMATION INDEX: ')
        t_0 = tk_gui_file_selection_window()

        print('SELECT COMPARISON TV INFORMATION INDEX: ')
        t_1 = tk_gui_file_selection_window()
        separator_3()

        with open(m_0, 'r', encoding='UTF-8') as movies_0, open(m_1, 'r', encoding='UTF-8') as movies_1:
            user_movie_results = movies_0.readlines()
            comparison_movie_results = movies_1.readlines()

            with open(os.path.expanduser(
                    (index_folder + '/FILES/MOVIE_COMPARISON_INDEX.csv').format(username)),
                    'w', encoding='UTF-8', newline='') as outFile_m:
                for line in compare_results(user_movie_results, comparison_movie_results):
                    outFile_m.write(line)

        with open(t_0, 'r', encoding='UTF-8') as tv_0, open(t_1, 'r', encoding='UTF-8') as tv_1:
            user_tv_results = tv_0.readlines()
            comparison_tv_results = tv_1.readlines()

            with open(os.path.expanduser(
                    (index_folder + '/FILES/TV_COMPARISON_INDEX.csv').format(username)),
                    'w', encoding='UTF-8', newline='') as outFile_t:
                for line in compare_results(user_tv_results, comparison_tv_results):
                    outFile_t.write(line)

    except (OSError, TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
        separator_3()

    print('COMPLETE: COMPARISON FILE(S) CAN BE FOUND IN THE USER MEDIA-INDEX FOLDER, FILES SUB-FOLDER')
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


def tk_gui_file_selection_window():
    root = Tk()
    root.withdraw()
    root.update()
    selected_file = filedialog.askopenfilename()
    root.destroy()
    return selected_file


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
