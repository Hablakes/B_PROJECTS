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

username = None

date_string = str(datetime.today().strftime('%Y_%m_%d'))

index_folder = '~/{0}_MEDIA_INDEX'

extensions = ('.3gp', '.asf', '.asx', '.avc', '.avi', '.bdmv', '.bin', '.bivx', '.dat', '.disc', '.divx', '.dv',
              '.dvr-ms', '.evo', '.fli', '.flv', '.h264', '.img', '.iso', '.m2ts', '.m2v', '.m4v', '.mkv', '.mov',
              '.mp4', '.mpeg', '.mpg', '.mt2s', '.mts', '.nfo', '.nrg', '.nsv', '.nuv', '.ogm', '.pva', '.qt', '.rm',
              '.rmvb', '.strm', '.svq3', '.ts', '.ty', '.viv', '.vob', '.vp3', '.wmv', '.xvid', '.webm')


def main():
    separator_3()
    launch_media_index()

    while True:
        media_index_home()


def change_directory_selection():
    print(pyfiglet.figlet_format('CHANGE_DIRECTORY', font='cybermedium'))
    separator_3()
    directory_selection()


def compare_results(results_user, results_other):
    output = []

    for line in results_user:
        if line not in results_other:
            output.append('HAVE: ' + line)

    for line in results_other:
        if line not in results_user:
            output.append('DO NOT HAVE: ' + line)

    return output


def create_media_information_indices():
    create_movie_information_index()
    create_tv_information_index()


def create_movie_information_index():
    movie_index = csv.reader(open(os.path.expanduser(
        (index_folder + '/MOVIE_VIDEO_FILES_PATHS.csv').format(username)), encoding='UTF-8'))
    movie_results_list = {}

    for movie_file in sorted(movie_index):

        try:

            movie_title_key = movie_file[0].rsplit('/')[-2]
            movie_filename_key = movie_file[0].rsplit('/', 1)[-1]

            if not movie_filename_key.lower().endswith('.nfo'):
                if movie_title_key not in movie_results_list:
                    movie_results_list[movie_title_key] = {}

                try:

                    title = guessit.guessit(movie_filename_key, options={'type': 'movie'})

                except OSError as e:
                    print('OS ERROR: ', e)
                    continue

                try:

                    test = pymediainfo.MediaInfo.parse(movie_file[0])

                except OSError as e:
                    print('OS ERROR: ', e)
                    continue

                for track in test.tracks:
                    if track.track_type == 'General':
                        duration = track.other_duration
                        movie_results_list[movie_title_key]['RUN-TIME'] = duration[0]

                    elif track.track_type == 'Video':
                        movie_results_list[movie_title_key]['DIRECTORY'] = movie_title_key
                        movie_results_list[movie_title_key]['TITLE'] = title.get('title')
                        movie_results_list[movie_title_key]['YEAR'] = title.get('year')
                        movie_results_list[movie_title_key]['RESOLUTION'] = str(track.width) + 'x' + str(track.height)
                        movie_results_list[movie_title_key]['FILE-TYPE'] = title.get('container')
                        movie_results_list[movie_title_key]['FILENAME'] = movie_filename_key

            elif movie_filename_key.lower().endswith('.nfo'):

                try:

                    with open(str(movie_file[0])) as f:
                        for line_item in f.readlines():
                            if '<plot>' in line_item:
                                movie_results_list[movie_title_key]['PLOT'] = line_item

                            elif '<rating>' in line_item:
                                movie_results_list[movie_title_key]['RATING'] = line_item

                except Exception as e:
                    print('ERROR: ', e, '\n', 'FILE: ', movie_file[0])
                    print('-' * 100)
                    continue

        except (OSError, TypeError, ValueError) as e:
            print('INPUT ERROR: ', e, '\n', 'FILE: ', movie_file[0])
            print('-' * 100)
            continue

    with open(os.path.expanduser((index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as f:

        csv_writer = csv.DictWriter(f, ['DIRECTORY', 'TITLE', 'YEAR', 'RESOLUTION', 'FILE-TYPE', 'PLOT', 'RATING',
                                        'RUN-TIME', 'FILENAME'])
        for movie_row in movie_results_list.values():
            csv_writer.writerow(movie_row)


def create_tv_information_index():
    tv_index = csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)), encoding='UTF-8'))
    tv_results_list = {}
    tv_show_plots_dictionary = {}

    for tv_file in sorted(tv_index):

        try:

            tv_title_key = tv_file[0].rsplit('/', 1)[-1][:-4]
            tv_folder_title = tv_file[0].rsplit('/')[-2]
            tv_folder_year = tv_folder_title.rsplit('(')[-1][:-1]
            tv_filename_key = tv_file[0].rsplit('/', 1)[-1]

            if str(tv_filename_key.lower()) == str('tvshow.nfo'):
                tv_show_plots_dictionary[tv_folder_title] = {}
                tv_show_plots_dictionary[tv_folder_title]['SHOW'] = tv_folder_title

                try:

                    with open(tv_file[0]) as f:
                        for line in f.readlines():
                            if '<plot>' in line:
                                tv_show_plots_dictionary[tv_folder_title]['PLOT'] = line

                except Exception as e:
                    print('ERROR: ', e, '\n', 'FILE: ', tv_file[0])
                    print('-' * 100)
                    continue
            elif not tv_filename_key.lower().endswith('.nfo'):

                if tv_title_key not in tv_results_list:
                    tv_results_list[tv_title_key] = {}

                try:

                    title = guessit.guessit(tv_filename_key, options={'type': 'episode'})

                except OSError as e:
                    print('OS ERROR: ', e)
                    continue

                try:

                    test = pymediainfo.MediaInfo.parse(tv_file[0])

                except OSError as e:
                    print('OS ERROR: ', e)
                    continue

                for track in test.tracks:

                    if track.track_type == 'General':
                        duration = track.other_duration
                        tv_results_list[tv_title_key]['RUN-TIME'] = duration[0]

                    elif track.track_type == 'Video':
                        tv_results_list[tv_title_key]['DIRECTORY'] = tv_folder_title
                        tv_results_list[tv_title_key]['TITLE'] = title.get('title')
                        tv_results_list[tv_title_key]['YEAR'] = tv_folder_year
                        tv_results_list[tv_title_key]['EPISODE TITLE'] = title.get('episode_title')
                        tv_results_list[tv_title_key]['SEASON'] = title.get('season')
                        tv_results_list[tv_title_key]['EPISODE NUMBER'] = title.get('episode')
                        tv_results_list[tv_title_key]['RESOLUTION'] = str(track.width) + 'x' + str(track.height)
                        tv_results_list[tv_title_key]['FILE-TYPE'] = title.get('container')
                        tv_results_list[tv_title_key]['FILENAME'] = tv_filename_key

            elif tv_filename_key.lower().endswith('.nfo'):

                if tv_title_key not in tv_results_list:
                    tv_results_list[tv_title_key] = {}

                if str(tv_filename_key.lower()) != str('tvshow.nfo'):

                    try:

                        with open(tv_file[0]) as f:
                            for line in f.readlines():
                                if '<plot>' in line:
                                    tv_results_list[tv_title_key]['PLOT'] = line

                                elif '<rating>' in line:
                                    tv_results_list[tv_title_key]['RATING'] = line

                    except Exception as e:
                        print('ERROR: ', e, '\n', 'FILE: ', tv_file[0])
                        print('-' * 100)
                        continue

        except (OSError, TypeError, ValueError) as e:
            print('INPUT ERROR: ', e, '\n', 'FILE: ', tv_file[0])
            print('-' * 100)
            continue

    with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as f:
        csv_writer = csv.DictWriter(f, ['DIRECTORY', 'TITLE', 'YEAR', 'EPISODE TITLE', 'SEASON', 'EPISODE NUMBER',
                                        'RESOLUTION', 'FILE-TYPE', 'PLOT', 'RATING', 'RUN-TIME', 'FILENAME'])
        for tv_row in tv_results_list.values():
            csv_writer.writerow(tv_row)

    with open(os.path.expanduser((index_folder + '/TV_PLOTS_INDEX.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as f:
        csv_writer = csv.DictWriter(f, ['SHOW', 'PLOT'])
        for tv_row in tv_show_plots_dictionary.values():
            csv_writer.writerow(tv_row)


def directory_selection():

    try:

        user_info_file = os.path.expanduser((index_folder + '/{0}_USER_INFO.csv').format(username))

        separator_3()
        print('ENTER PATH OF MOVIE DIRECTORY, IF NONE HIT CANCEL: ')
        movie_directory_input_main = tk_gui_file_browser_window()
        print('\n', str(movie_directory_input_main))

        separator_3()
        print('ENTER PATH OF TV DIRECTORY, IF NONE HIT CANCEL: ')
        tv_directory_input_main = tk_gui_file_browser_window()
        print('\n', str(tv_directory_input_main))

        separator_3()
        print('ALTERNATE DIRECTORIES? - Y/N: ')

        separator_3()
        alternate_directory_prompt = input('ENTER: Y or N: ').lower()
        separator_3()

        if alternate_directory_prompt == str('y'):

            movie_alt_directories_list = list()
            print('ENTER ALTERNATE MOVIE DIRECTORIES: ')
            separator_3()

            movie_directory_input_line = tk_gui_file_browser_window()

            while movie_directory_input_line != '':
                movie_alt_directories_list.append(movie_directory_input_line)
                movie_directory_input_line = tk_gui_file_browser_window()

            movie_directories_input_alternate = list(movie_alt_directories_list)
            print('DIRECTORIES ENTERED: ', '\n', '\n', movie_directories_input_alternate)

            tv_alt_directories_list = list()
            separator_3()
            print('ENTER ALTERNATE TV DIRECTORIES: ')
            separator_3()

            tv_directory_input_line = tk_gui_file_browser_window()

            while tv_directory_input_line != '':
                tv_alt_directories_list.append(tv_directory_input_line)
                tv_directory_input_line = tk_gui_file_browser_window()

            tv_directories_input_alternate = list(tv_alt_directories_list)
            print('DIRECTORIES ENTERED: ', '\n', '\n', tv_directories_input_alternate)

            user_info_dict = {'user:': username, 'movie_dir:': movie_directory_input_main,
                              'tv_dir:': tv_directory_input_main, 'movie_alt_dir:': movie_directories_input_alternate,
                              'tv_alt_dir:': tv_directories_input_alternate}

            with open(user_info_file, 'w', encoding='UTF-8', newline='') as f:
                csv_writer = csv.writer(f)
                for user_data in user_info_dict.items():
                    csv_writer.writerow(user_data)

        elif alternate_directory_prompt != str('y'):

            print('NO ALTERNATE DIRECTORIES')
            separator_3()

            user_info_dict = {'user:': username, 'movie_dir:': movie_directory_input_main,
                              'tv_dir:': tv_directory_input_main, 'movie_alt_dir:': '', 'tv_alt_dir:': ''}

            with open(user_info_file, 'w', encoding='UTF-8', newline='') as f:
                csv_writer = csv.writer(f)
                for user_data in user_info_dict.items():
                    csv_writer.writerow(user_data)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n')


def graph_options_advanced(user_name, picture_graph_options_int, terminal_graph_options_int):
    movie_files_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(user_name)), encoding='UTF-8')))
    tv_files_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_INFORMATION_INDEX.csv').format(user_name)), encoding='UTF-8')))
    m_ten_eighty_found_list = []
    m_seven_twenty_found_list = []
    m_standard_def_found_list = []
    m_empty_response_list = []
    movies_total_list = []
    tv_ten_eighty_found_list = []
    tv_seven_twenty_found_list = []
    tv_standard_def_found_list = []
    tv_empty_response_list = []
    tv_total_list = []

    for res in movie_files_results_list:
        if re.findall(r'19\d{2}x', res[3]):
            m_ten_eighty_found_list.append(res)

        elif re.findall(r'1[0-8]\d{2}x', res[3]):
            m_seven_twenty_found_list.append(res)

        elif re.findall(r'\d{3}x', res[3]):
            m_standard_def_found_list.append(res)

        else:
            m_empty_response_list.append(+1)
        movies_total_list.append(+1)
    movies_graph_terminal_results = [('1080p', float(len(m_ten_eighty_found_list))),
                                     ('720p', float(len(m_seven_twenty_found_list))),
                                     ('SD (Below 720p)', float(len(m_standard_def_found_list)))]
    movie_data = [float(len(m_ten_eighty_found_list)), float(len(m_seven_twenty_found_list)),
                  float(len(m_standard_def_found_list))]

    for res in tv_files_results_list:
        if re.findall(r'19\d{2}x', res[6]):
            tv_ten_eighty_found_list.append(res)

        elif re.findall(r'1[0-8]\d{2}x', res[6]):
            tv_seven_twenty_found_list.append(res)

        elif re.findall(r'\d{3}x', res[6]):
            tv_standard_def_found_list.append(res)

        else:
            tv_empty_response_list.append(+1)
        tv_total_list.append(+1)
    tv_shows_graph_terminal_results = [('1080p', float(len(tv_ten_eighty_found_list))),
                                       ('720p', float(len(tv_seven_twenty_found_list))),
                                       ('SD (Below 720p)', float(len(tv_standard_def_found_list)))]
    tv_data = [float(len(tv_ten_eighty_found_list)), float(len(tv_seven_twenty_found_list)),
               float(len(tv_standard_def_found_list))]

    def format_data(percent, all_values):
        absolute = int(percent / 100. * numpy.sum(all_values))
        return '{:.1f}%\n({:d})'.format(percent, absolute)

    labels = ['1080p', '720p', 'SD (Below 720p)']
    colors = ['#85c1e9', '#a569bd', '#808b96']

    if picture_graph_options_int == 5:
        fig, ax = plt.subplots(figsize=(20, 10), subplot_kw=dict(aspect='equal'))
        wedges, texts, auto_texts = ax.pie(movie_data, autopct=lambda pct: format_data(pct, movie_data),
                                           shadow=True, colors=colors, textprops=dict(color='black'))

        ax.legend(wedges, labels,
                  title='RESOLUTIONS',
                  loc='center left',
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(auto_texts, size=9, weight='bold')
        ax.set_title('MOVIE_RESOLUTION_RESULTS')
        plt_path = os.path.expanduser('~/{0}_MEDIA_INDEX/GRAPHS/MOVIE_RESOLUTION_RESULTS_'.format(user_name) +
                                      date_string + '.png')
        plt.savefig(plt_path)
        print('GRAPH SAVED: ', plt_path)
        separator_3()
        plt.show()

    elif terminal_graph_options_int == 5:

        graph = Pyasciigraph()
        for line in graph.graph('MOVIES: RESOLUTION PERCENTAGES: ', movies_graph_terminal_results):
            print('\n', line)
        separator_3()

    elif picture_graph_options_int == 6:

        fig, ax = plt.subplots(figsize=(20, 10), subplot_kw=dict(aspect='equal'))
        wedges, texts, auto_texts = ax.pie(tv_data, autopct=lambda pct: format_data(pct, tv_data),
                                           shadow=True, colors=colors, textprops=dict(color='black'))

        ax.legend(wedges, labels,
                  title='RESOLUTIONS',
                  loc='center left',
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(auto_texts, size=9, weight='bold')
        ax.set_title('TV_SHOW_RESOLUTION_RESULTS')
        plt_path = os.path.expanduser('~/{0}_MEDIA_INDEX/GRAPHS/TV_RESOLUTION_RESULTS_'.format(user_name) +
                                      date_string + '.png')
        plt.savefig(plt_path)
        print('GRAPH SAVED: ', plt_path)
        separator_3()
        plt.show()

    elif terminal_graph_options_int == 6:

        graph = Pyasciigraph()
        for line in graph.graph('TV SHOWS: RESOLUTION PERCENTAGES: ', tv_shows_graph_terminal_results):
            print('\n', line)
        separator_3()


def graph_options_base(user_name, picture_graph_options_int, terminal_graph_options_int):
    media_index_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/MEDIA_TITLE_INDEX.csv').format(user_name)), encoding='UTF-8')))
    movie_years_dict = {}
    movie_decades_dict = {}
    tv_years_dict = {}
    tv_decades_amount_dict = {}
    movie_year_totals_dict = {}
    movie_decades_totals_dict = {}
    tv_year_totals_dict = {}
    tv_decades_totals_dict = {}

    for title_item in media_index_list:
        title_item_year = re.split(r'(.+) \((\d{4})\)', title_item[2], flags=0)
        title_item_year_int = int(title_item_year[0])
        title_item_decade_int = int(title_item_year[0][:-1] + '0')

        if title_item_year_int in range(1900, 2100, 1):
            if str('MOVIE') in title_item:
                if title_item_year_int not in movie_years_dict:
                    movie_years_dict[title_item_year_int] = []
                movie_years_dict[title_item_year_int].append(title_item)

                if title_item_decade_int not in movie_decades_dict:
                    movie_decades_dict[title_item_decade_int] = []
                movie_decades_dict[title_item_decade_int].append(title_item)

            if str('TV') in title_item:
                if title_item_year_int not in tv_years_dict:
                    tv_years_dict[title_item_year_int] = []
                tv_years_dict[title_item_year_int].append(title_item)

                if title_item_decade_int not in tv_decades_amount_dict:
                    tv_decades_amount_dict[title_item_decade_int] = []
                tv_decades_amount_dict[title_item_decade_int].append(title_item)

    if picture_graph_options_int == 1:

        for year_values, value in sorted(movie_years_dict.items()):
            movie_year_totals_dict[year_values] = len(value)
        x, y = zip(*sorted(movie_year_totals_dict.items()))
        plt.bar(x, y)
        plt_path = os.path.expanduser('~/{0}_MEDIA_INDEX/GRAPHS/MOVIE_YEAR_RESULTS_'.format(user_name) +
                                      date_string + '.png')
        plt.savefig(plt_path)
        print('GRAPH SAVED: ', plt_path)
        separator_3()
        plt.show()

    elif terminal_graph_options_int == 1:

        for movie_year_values, value in sorted(movie_years_dict.items()):
            movie_year_totals_dict[movie_year_values] = len(value)
        movie_data = sorted(movie_year_totals_dict.items())
        movie_years_terminal_graph_list = []

        for key, value in movie_data:
            movie_years_terminal_graph_list.append((str(key), value))
        graph = Pyasciigraph()

        for line in graph.graph('MOVIES: YEAR AMOUNTS: ', movie_years_terminal_graph_list):
            print('\n', line)
        separator_3()

    elif picture_graph_options_int == 2:

        for year_values, value in sorted(tv_years_dict.items()):
            tv_year_totals_dict[year_values] = len(value)
        x, y = zip(*sorted(tv_year_totals_dict.items()))
        plt.bar(x, y)
        plt_path = os.path.expanduser('~/{0}_MEDIA_INDEX/GRAPHS/TV_YEAR_RESULTS_'.format(user_name) +
                                      date_string + '.png')
        plt.savefig(plt_path)
        print('GRAPH SAVED: ', plt_path)
        separator_3()
        plt.show()

    elif terminal_graph_options_int == 2:

        for tv_year_values, value in sorted(tv_years_dict.items()):
            tv_year_totals_dict[tv_year_values] = len(value)
        tv_data = sorted(tv_year_totals_dict.items())
        tv_years_terminal_graph_list = []

        for key, value in tv_data:
            tv_years_terminal_graph_list.append((str(key), value))
        graph = Pyasciigraph()

        for line in graph.graph('TV SHOWS: YEAR AMOUNTS: ', tv_years_terminal_graph_list):
            print('\n', line)
        separator_3()

    elif picture_graph_options_int == 3:

        for year_values, value in sorted(movie_decades_dict.items()):
            movie_decades_totals_dict[year_values] = len(value)
        x, y = zip(*movie_decades_totals_dict.items())
        plt.bar(x, y, width=5)
        plt_path = os.path.expanduser('~/{0}_MEDIA_INDEX/GRAPHS/MOVIE_DECADE_RESULTS_'.format(user_name) +
                                      date_string + '.png')
        plt.savefig(plt_path)
        print('GRAPH SAVED: ', plt_path)
        separator_3()
        plt.show()

    elif terminal_graph_options_int == 3:

        for movie_year_values, value in sorted(movie_decades_dict.items()):
            movie_decades_totals_dict[movie_year_values] = len(value)
        movie_decades_terminal_graph_list = []

        for key, value in movie_decades_totals_dict.items():
            movie_decades_terminal_graph_list.append((str(key), value))
        graph = Pyasciigraph()

        for line in graph.graph('MOVIES: DECADE AMOUNTS: ', movie_decades_terminal_graph_list):
            print('\n', line)
        separator_3()

    elif picture_graph_options_int == 4:

        for year_values, value in sorted(tv_decades_amount_dict.items()):
            tv_decades_totals_dict[year_values] = len(value)
        x, y = zip(*tv_decades_totals_dict.items())
        plt.bar(x, y, width=5)
        plt_path = os.path.expanduser('~/{0}_MEDIA_INDEX/GRAPHS/TV_DECADE_RESULTS_'.format(user_name) +
                                      date_string + '.png')
        plt.savefig(plt_path)
        print('GRAPH SAVED: ', plt_path)
        separator_3()
        plt.show()

    elif terminal_graph_options_int == 4:

        for tv_year_values, value in sorted(tv_decades_amount_dict.items()):
            tv_decades_totals_dict[tv_year_values] = len(value)
        tv_decades_terminal_graph_list = []

        for key, value in tv_decades_totals_dict.items():
            tv_decades_terminal_graph_list.append((str(key), value))
        graph = Pyasciigraph()

        for line in graph.graph('TV SHOWS: DECADE AMOUNTS: ', tv_decades_terminal_graph_list):
            print('\n', line)
        separator_3()


def launch_media_index():
    print(pyfiglet.figlet_format('MEDIA_INDEX', font='cybermedium'))
    separator_3()

    try:

        global username
        username = input('ENTER YOUR USERNAME (CASE-SENSITIVE): ')
        separator_3()
        username_check_and_folder_creation()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
        launch_media_index()


def library_total_amount():
    media_index_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)), encoding='UTF-8')))
    tv_index_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)), encoding='UTF-8')))
    tv_amounts_list = []
    episode_amounts_list = []
    movie_amounts_list = []

    for counted_movie_title in media_index_list:
        if str('MOVIE') in counted_movie_title:
            movie_amounts_list.append(counted_movie_title)

    for counted_tv_title in media_index_list:
        if str('TV') in counted_tv_title:
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


def media_index_home():
    username_check_and_folder_creation()
    print(pyfiglet.figlet_format('MEDIA_INDEX', font='cybermedium'))
    separator_3()

    print('1) CHANGE DATABASE DIRECTORIES                   2) CREATE PATH INDICES', '\n')
    print('3) CREATE TITLE INDEX                            4) CREATE MEDIA INFORMATION INDICES', '\n')
    print('5) COMPARE TWO USERS INFORMATION INDICES         6) DISPLAY LIBRARY TOTALS', '\n')
    print('7) MEDIA INFORMATION QUERIES                     8) SORT OPTIONS', '\n')
    print('9) PICTURE GRAPH OPTIONS                         10) TERMINAL GRAPH OPTIONS', '\n')
    print('11) SAVED SEARCHES')
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
                print('0) MAIN MENU                             1) CHANGE DATABASE DIRECTORIES')
                separator_3()
                scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if scan_sub_input == 0:
                    media_index_home()

                elif scan_sub_input == 1:
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
                print('0) MAIN MENU                             1) CONTINUE WITH MEDIA PATH(S) SCAN')
                separator_3()
                scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if scan_sub_input == 0:
                    media_index_home()

                elif scan_sub_input == 1:
                    walk_directories_and_create_indices()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif lmi_input_action == 3:

            try:

                print('CONFIRM: ')
                separator_1()
                print('THIS OPERATION CAN TAKE A LONG TIME (SEVERAL MINUTES FOR LARGE LIBRARIES)')
                separator_2()
                print('0) MAIN MENU                             1) CONTINUE BUILDING TITLE INDEX')
                separator_3()
                scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if scan_sub_input == 0:
                    media_index_home()
                elif scan_sub_input == 1:
                    scrape_media_folders_for_csv()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif lmi_input_action == 4:

            try:

                print('CONFIRM: ')
                separator_1()
                print('THIS OPERATION CAN TAKE A LONG TIME (SEVERAL HOURS FOR LARGE LIBRARIES)')
                separator_2()
                print('0) MAIN MENU                             1) CONTINUE WITH MEDIA INFORMATION SCAN')
                separator_3()
                scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if scan_sub_input == 0:
                    media_index_home()

                elif scan_sub_input == 1:
                    create_media_information_indices()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif lmi_input_action == 5:

            try:

                print('CONFIRM: ')
                separator_1()
                print('0) MAIN MENU                             1) COMPARE USER(S) INFORMATION INDICES')
                separator_3()
                scan_sub_input = int(input('ENTER #: '))
                separator_3()

                if scan_sub_input == 0:
                    media_index_home()

                elif scan_sub_input == 1:
                    select_users_indices_to_compare()

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif lmi_input_action == 6:
            library_total_amount()

        elif lmi_input_action == 7:
            media_queries_sub_menu()

        elif lmi_input_action == 8:
            sort_options_sub_menu()

        elif lmi_input_action == 9:
            picture_graph_options_sub_menu()

        elif lmi_input_action == 10:
            terminal_graph_options_sub_menu()

        elif lmi_input_action == 11:
            saved_searches()

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
    print('                                                 6) SEARCH PLOTS FOR KEYWORD(S)')
    separator_2()
    print('                                                 7) QUERY TOTAL NUMBER (#) OF EPISODES IN A TV SHOW')
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

            tv_episode_query_input = str(input('ENTER SEARCH QUERY (MOVIES): ').lower())
            separator_3()
            query_tv_information_index(tv_episode_query=tv_episode_query_input)

        elif title_search_type == 6:

            plot_search_list = []

            try:

                print('SEARCH PLOTS OF:                             1) MOVIES       2) TV SHOW EPISODES', '\n')
                print('                                             3) MOVIES AND TV SHOW EPISODES')
                separator_2()
                print('                                             4) TV SHOW GENERAL OVERVIEW')
                separator_2()
                print('0) MAIN MENU')
                separator_3()
                plot_search_int = int(input('ENTER #: '))
                plot_search_list.append(plot_search_int)
                separator_3()
                plot_search_type_input = plot_search_list[0]

                if int(plot_search_list[0]) == 0:
                    media_index_home()

                else:

                    try:

                        plot_search = input('KEYWORD(S): ')
                        plot_search_list.append(plot_search.lower())
                        separator_3()

                    except (OSError, TypeError, ValueError) as e:
                        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')
                        separator_3()
                plot_search_keywords_input = plot_search_list[1]
                search_plots(plot_search_type=plot_search_type_input, plot_search_keywords=plot_search_keywords_input)

            except (TypeError, ValueError) as e:
                print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
                separator_3()

        elif title_search_type == 7:

            total_tv_episodes_in_show_title()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


def picture_graph_options_sub_menu():
    print(pyfiglet.figlet_format('PICTURE_GRAPHS', font='cybermedium'))
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

        picture_graph_options = input('ENTER #: ')
        separator_3()
        picture_graph_options_int = int(picture_graph_options)

        if picture_graph_options_int == 0:
            media_index_home()

        elif 1 <= picture_graph_options_int <= 4:

            graph_options_base(username, picture_graph_options_int=picture_graph_options_int,
                               terminal_graph_options_int='')

        elif 5 <= picture_graph_options_int <= 6:

            graph_options_advanced(username, picture_graph_options_int=picture_graph_options_int,
                                   terminal_graph_options_int='')

        elif 7 <= picture_graph_options_int <= 8:

            query_file_type_totals(username, picture_graph_options_int=picture_graph_options_int,
                                   terminal_graph_options_int='')

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


def query_file_type_totals(user_name, picture_graph_options_int, terminal_graph_options_int):
    movie_files_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(user_name)), encoding='UTF-8')))
    tv_files_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_INFORMATION_INDEX.csv').format(user_name)), encoding='UTF-8')))
    movie_extensions_dictionary = {}
    movie_extensions_totals = {}
    tv_extensions_dictionary = {}
    tv_extensions_totals = {}

    for file_type in movie_files_results_list:
        if str(',') not in file_type[4]:

            if file_type[4] not in movie_extensions_dictionary:
                movie_extensions_dictionary[file_type[4]] = []
            movie_extensions_dictionary[file_type[4]].append(file_type[4])
    movie_file_type_totals = {}

    if picture_graph_options_int == 7:

        for movie_file_type_values, value in sorted(movie_extensions_dictionary.items()):
            movie_file_type_totals[movie_file_type_values] = len(value)
        x, y = zip(*sorted(movie_file_type_totals.items()))
        plt.bar(x, y)
        plt_path = os.path.expanduser('~/{0}_MEDIA_INDEX/GRAPHS/MOVIE_FILETYPE_RESULTS_'.format(user_name) +
                                      date_string + '.png')
        plt.savefig(plt_path)
        print('GRAPH SAVED: ', plt_path)
        separator_3()
        plt.show()

    elif terminal_graph_options_int == 7:

        for file_type_values, value in sorted(movie_extensions_dictionary.items()):
            movie_extensions_totals[file_type_values] = len(value)
        file_type_totals_terminal_graph_list = []

        for key, value in movie_extensions_totals.items():
            file_type_totals_terminal_graph_list.append((str(key), value))
        graph = Pyasciigraph()

        for line in graph.graph('MOVIES: FILE-TYPE AMOUNTS: ', file_type_totals_terminal_graph_list):
            print('\n', line)
        separator_3()

    for file_type in tv_files_results_list:
        if str(',') not in file_type[7]:
            if file_type[7] not in tv_extensions_dictionary:
                tv_extensions_dictionary[file_type[7]] = []
            tv_extensions_dictionary[file_type[7]].append(file_type[7])
    tv_file_type_totals = {}

    if picture_graph_options_int == 8:

        for tv_file_type_values, value in sorted(tv_extensions_dictionary.items()):
            tv_file_type_totals[tv_file_type_values] = len(value)
        x, y = zip(*sorted(tv_file_type_totals.items()))
        plt.bar(x, y)
        plt_path = os.path.expanduser('~/{0}_MEDIA_INDEX/GRAPHS/TV_FILETYPE_RESULTS_'.format(user_name) +
                                      date_string + '.png')
        plt.savefig(plt_path)
        print('GRAPH SAVED: ', plt_path)
        separator_3()
        plt.show()

    elif terminal_graph_options_int == 8:

        for file_type_values, value in sorted(tv_extensions_dictionary.items()):
            tv_extensions_totals[file_type_values] = len(value)
        file_type_totals_terminal_graph_list = []

        for key, value in tv_extensions_totals.items():
            file_type_totals_terminal_graph_list.append((str(key), value))
        graph = Pyasciigraph()

        for line in graph.graph('TV SHOWS: FILE-TYPE AMOUNTS: ', file_type_totals_terminal_graph_list):
            print('\n', line)
        separator_3()


def query_movie_information_index(movie_query):
    mv_files_results_list = csv.reader(open(os.path.expanduser(
        (index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)), encoding='UTF-8'))

    try:

        for movie_file in mv_files_results_list:
            if str(movie_query.lower()) in str(movie_file[1].lower()):

                separator_2()
                print('MOVIE FOLDER: ', '\n', movie_file[0])
                separator_2()
                print('MOVIE TITLE: ', '\n', movie_file[1])
                separator_2()
                print('MOVIE YEAR: ', '\n', movie_file[2])
                separator_2()
                print('MOVIE RESOLUTION: ', '\n', movie_file[3])
                separator_2()
                print('MOVIE FILE-TYPE: ', '\n', movie_file[4])
                separator_2()

                if int(len(movie_file[7])) != 0:
                    print('RUN-TIME: ', '\n', movie_file[7])
                    separator_2()

                if int(len(movie_file[6])) != 0:

                    print('RATING: ', '\n')
                    if '</rating>' not in movie_file[6]:
                        mv_rating = re.findall('<rating>(.*?)', movie_file[6])
                        print(mv_rating[0])
                        separator_2()

                    elif '</rating>' in movie_file[6]:
                        mv_rating = re.findall('<rating>(.*?)</rating>', movie_file[6])
                        print(mv_rating[0])
                        separator_2()

                if int(len(movie_file[5])) != 0:

                    print('PLOT: ', '\n')
                    if '</plot>' not in movie_file[5]:
                        mv_plot = re.findall('<plot>(.*?)', movie_file[5])
                        print(textwrap.fill(mv_plot[0], 100))
                        separator_2()

                    elif '</plot>' in movie_file[5]:
                        mv_plot = re.findall('<plot>(.*?)</plot>', movie_file[5])
                        print(textwrap.fill(mv_plot[0], 100))
                        separator_2()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID QUERY, PLEASE RETRY')
        separator_3()


def query_tv_information_index(tv_episode_query):
    tv_files_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), encoding='UTF-8')))

    try:

        for tv_file in tv_files_results_list:
            if str(tv_episode_query.lower()) in str(tv_file[3].lower()):

                separator_2()
                print('TV SHOW FOLDER: ', '\n', tv_file[0])
                separator_2()
                print('TV SHOW TITLE: ', '\n', tv_file[1])
                separator_2()
                print('TV SHOW YEAR: ', '\n', tv_file[2])
                separator_2()
                print('TV SHOW EPISODE TITLE: ', '\n', tv_file[3])
                separator_2()
                print('SEASON NUMBER: ', '\n', tv_file[4])
                separator_2()
                print('EPISODE NUMBER: ', '\n', tv_file[5])
                separator_2()
                print('RESOLUTION: ', '\n', tv_file[6])
                separator_2()
                print('FILE-TYPE: ', '\n', tv_file[7])
                separator_2()

                if int(len(tv_file[10])) != 0:

                    print('RUN-TIME: ', '\n', tv_file[10])
                    separator_2()

                if int(len(tv_file[9])) != 0:

                    print('RATING: ', '\n')
                    if '</rating>' not in tv_file[9]:
                        tv_rating = re.findall('<rating>(.*?)', tv_file[9])
                        print(tv_rating[0])
                        separator_2()

                    elif '</rating>' in tv_file[9]:
                        tv_rating = re.findall('<rating>(.*?)</rating>', tv_file[9])
                        print(tv_rating[0])
                        separator_2()

                if int(len(tv_file[8])) != 0:

                    print('PLOT: ', '\n')
                    if '</plot>' not in tv_file[8]:
                        tv_plot = re.findall('<plot>(.*?)', tv_file[8])
                        print(textwrap.fill(tv_plot[0], 100))
                        separator_2()

                    elif '</plot>' in tv_file[8]:
                        tv_plot = re.findall('<plot>(.*?)</plot>', tv_file[8])
                        print(textwrap.fill(tv_plot[0], 100))
                        separator_2()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID QUERY, PLEASE RETRY')
        separator_3()


def saved_searches():
    print(pyfiglet.figlet_format('SAVED_SEARCHES', font='cybermedium'))

    saved_search_inputs_list = []
    saved_searches_list = []
    search_keywords_list = []

    separator_2()
    print('1) VIEW SAVED SEARCH TERMS (GENRE(S), KEYWORD(S))')
    separator_2()
    print('2) ADD A NEW SEARCH TERM')
    separator_2()
    print('0) MAIN MENU')
    separator_3()
    saved_search_type_input = int(input('ENTER #: '))
    saved_search_inputs_list.append(saved_search_type_input)
    separator_3()

    try:

        if saved_search_inputs_list[0] == 0:
            media_index_home()

        elif saved_search_inputs_list[0] == 1:

            saved_searches_file = os.path.expanduser((index_folder + '/SEARCH/{0}_SAVED_SEARCHES.csv').format(username))

            with open(saved_searches_file, 'r', encoding='UTF-8', newline='') as f:
                for search_rows in f:
                    saved_searches_list.append(search_rows)

            for enumeration_number, searches in enumerate(saved_searches_list):
                genres = searches.rsplit(',')[0]
                keywords = searches.rsplit(',')[1]
                print((str(enumeration_number) + ') '), '\n', '\n', 'GENRE: ', genres, '\n', 'KEYWORD(S): ', keywords)

        elif saved_search_inputs_list[0] == 2:
            saved_searches_file = os.path.expanduser((index_folder + '/SEARCH/{0}_SAVED_SEARCHES.csv').format(username))
            print('SELECT TITLE FOR GENRE, ADD KEYWORD(S) FOR SEARCH TERM(S))')
            separator_2()
            new_genre = str(input('ENTER TITLE FOR NEW GENRE: '))
            separator_2()
            new_search_term = str(input('ENTER KEYWORD(S): ')).lower()
            separator_3()
            saved_searches_list.append([new_genre, new_search_term])

            with open(saved_searches_file, 'a', encoding='UTF-8', newline='') as f:
                csv_writer = csv.writer(f)
                for user_data in saved_searches_list:
                    csv_writer.writerow(user_data)
            saved_searches()

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()

    separator_3()
    print('1) QUERY DATABASE WITH SAVED SEARCH TERM(S): ')
    separator_2()
    print('0) MAIN MENU')
    separator_3()
    saved_search_sub_query_type_input = int(input('ENTER #: '))
    saved_search_inputs_list.append(saved_search_sub_query_type_input)
    separator_3()

    try:

        if saved_search_inputs_list[1] == 0:
            media_index_home()

        elif saved_search_inputs_list[1] == 1:
            print('SELECT NUMBER (#) FOR GENRE, KEYWORD(S) TO SEARCH: ', '\n')
            separator_3()
            saved_search_sub_query_input = int(input('ENTER #: '))
            search_term = str(saved_searches_list[saved_search_sub_query_input].rsplit(',')[1]).lower()

            for words in search_term.split(' '):
                words = words.strip()
                search_keywords_list.append(words)

            for found_search_terms in search_keywords_list:
                separator_3()
                print('QUERYING INFORMATION FOR SELECTED KEYWORD(S): ', found_search_terms)
                separator_3()
                search_plots(plot_search_type=3, plot_search_keywords=found_search_terms)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'PLEASE RETRY YOUR SELECTION USING THE NUMBER KEYS')
        separator_3()


def scrape_media_folders_for_csv():
    movie_title_items = []
    tv_title_items = []

    try:

        if movie_dir_input is not str(''):
            movie_dir_list = os.listdir(movie_dir_input)
            for movie_found in sorted(movie_dir_list):
                movie_scrape_info = guessit.guessit(movie_found)
                title_item_check = ['MOVIE', movie_scrape_info.get('title'), str(movie_scrape_info.get('year'))]
                if "," in title_item_check[2]:
                    title_item_check.append(title_item_check[2][-5:-1])
                    title_item_check.remove(title_item_check[2])
                movie_title_items.append(title_item_check)

        elif movie_alt_dir_input is not str(''):
            movie_alt_dir_list = os.listdir(movie_alt_dir_input)
            for movie_found in sorted(movie_alt_dir_list):
                movie_scrape_info = guessit.guessit(movie_found)
                title_item_check = ['MOVIE', movie_scrape_info.get('title'), str(movie_scrape_info.get('year'))]
                if "," in title_item_check[2]:
                    title_item_check.append(title_item_check[2][-5:-1])
                    title_item_check.remove(title_item_check[2])
                movie_title_items.append(title_item_check)

        elif tv_dir_input is not str(''):
            tv_dir_list = os.listdir(tv_dir_input)
            for tv_found in sorted(tv_dir_list):
                tv_scrape_info = guessit.guessit(tv_found)
                title_item_check = ['TV', tv_scrape_info.get('title'), str(tv_scrape_info.get('year'))]
                if "," in title_item_check[2]:
                    title_item_check.append(title_item_check[2][-5:-1])
                    title_item_check.remove(title_item_check[2])
                tv_title_items.append(title_item_check)

        elif tv_alt_dir_input is not str(''):
            tv_alt_dir_list = os.listdir(tv_alt_dir_input)
            for tv_found in sorted(tv_alt_dir_list):
                tv_scrape_info = guessit.guessit(tv_found)
                title_item_check = ['TV', tv_scrape_info.get('title'), str(tv_scrape_info.get('year'))]
                if "," in title_item_check[2]:
                    title_item_check.append(title_item_check[2][-5:-1])
                    title_item_check.remove(title_item_check[2])
                tv_title_items.append(title_item_check)

        with open(os.path.expanduser((index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)), 'w',
                  encoding='UTF-8', newline='') as f:
            csv_writer = csv.writer(f)
            for file_row in movie_title_items:
                csv_writer.writerow(file_row)

            for file_row in tv_title_items:
                csv_writer.writerow(file_row)

    except (OSError, TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INCORRECT DIRECTORY INPUT(S), PLEASE RETRY')
        separator_3()


def search_plots(plot_search_type, plot_search_keywords):
    movie_files_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username)), encoding='UTF-8')))
    tv_files_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), encoding='UTF-8')))
    tv_plots_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_PLOTS_INDEX.csv').format(username)), encoding='UTF-8')))
    plots_list = []

    if int(plot_search_type) == 1:

        for plot in movie_files_results_list:
            plots_list.append('MOVIE' + ' - ' + plot[0] + ' - ' + plot[5])

        for items in plots_list:
            if plot_search_keywords.lower() in items.lower():
                print('\n', textwrap.fill(items, 100))
        separator_3()

    elif int(plot_search_type) == 2:

        for plot in tv_files_results_list:
            plots_list.append('TV SHOW' + ' - ' + plot[0] + ' - ' + plot[8])

        for items in plots_list:
            if plot_search_keywords.lower() in items.lower():
                print('\n', textwrap.fill(items, 100))
        separator_3()

    elif int(plot_search_type) == 3:

        for plot in movie_files_results_list:
            plots_list.append('MOVIE' + ' - ' + plot[0] + ' - ' + plot[5])

        for plot in tv_files_results_list:
            plots_list.append('TV SHOW' + ' - ' + plot[0] + ' - ' + plot[8])

        for items in plots_list:
            if plot_search_keywords.lower() in items.lower():
                print('\n', textwrap.fill(items, 100))
        separator_3()

    elif int(plot_search_type) == 4:

        for plot in tv_plots_list:
            plots_list.append('TV SHOW' + ' - ' + plot[0] + ' - ' + plot[1])

        for items in plots_list:
            if plot_search_keywords.lower() in items.lower():
                print('\n', textwrap.fill(items, 100))
        separator_3()


def search_titles(title_search_type, movie_title_query, tv_show_query):
    media_index_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)), encoding='UTF-8')))
    tv_files_results_list = csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), encoding='UTF-8'))
    episode_information_list = []
    episode_information_search_list = []
    episode_folder_titles_dictionary = {}
    episode_folder_titles_list = []

    if title_search_type == 1:

        try:

            print('SEARCH RESULTS: ')
            separator_1()
            print('MOVIES: ', '\n')

            for movie_search_result in media_index_list:
                if str('MOVIE') in movie_search_result[0]:
                    search_info = re.split(r'(.+) \((\d{4})\) \((.+)x(.+)\)\.(.+)', str(movie_search_result), flags=0)

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
                if str('TV') in tv_search_result[0]:
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
                tv_folder_key = tv_file[0]
                tv_title_key = tv_folder_key[:-7]
                tv_episode_name_key = tv_file[3]

                if tv_show_query.lower() in tv_title_key.lower():

                    if str(tv_episode_name_key) == str(''):
                        tv_episode_name_key = 'NO EPISODE TITLE IN MEDIA-INDEX FOR THIS FILE'
                    episode_information_list.append([tv_title_key, tv_episode_name_key])

                    if tv_folder_key not in episode_folder_titles_dictionary:
                        episode_folder_titles_dictionary[tv_folder_key] = {}
                        episode_folder_titles_dictionary[tv_folder_key]['EPISODES'] = []
                    episode_folder_titles_dictionary[tv_folder_key]['EPISODES'].append(tv_episode_name_key)

            for enumeration_number, found_episodes in enumerate(episode_information_list):
                found_tv_folder_key = found_episodes[0]
                found_tv_episode_name_key = found_episodes[1]
                episode_information_search_list.append([(str(enumeration_number) + ') '),
                                                        (str(found_tv_folder_key) + ' - '), found_tv_episode_name_key])
            print('TV SHOWS FOUND: ')
            separator_1()

            for found_tv_shows in episode_folder_titles_dictionary.keys():
                episode_folder_titles_list.append(found_tv_shows)

            for show_titles in episode_folder_titles_list:
                print('-', show_titles)

            separator_3()
            print('EPISODES FOUND: ')
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


def sort_function_base(sort_options_int):
    media_index = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/MEDIA_TITLE_INDEX.csv').format(username)), encoding='UTF-8')))

    sorted_title = sorted(media_index, key=lambda x: (x[0], x[1]))
    sorted_title_r = sorted(media_index, key=lambda x: (x[0], x[1]), reverse=True)
    sorted_year = sorted(media_index, key=lambda x: (x[0], x[2]))
    sorted_year_r = sorted(media_index, key=lambda x: (x[0], x[2]), reverse=True)

    if sort_options_int == 1:
        for title_item in sorted_title:
            print('\n', title_item)
        separator_3()

    elif sort_options_int == 2:
        for title_item in sorted_title_r:
            print('\n', title_item)
        separator_3()

    elif sort_options_int == 3:
        for title_item in sorted_year:
            print('\n', title_item)
        separator_3()

    elif sort_options_int == 4:
        for title_item in sorted_year_r:
            print('\n', title_item)
        separator_3()


def sort_options_sub_menu():
    print(pyfiglet.figlet_format('SORT_OPTIONS', font='cybermedium'))
    separator_3()

    print('SORT MOVIE & TV SHOWS BY:            TITLES:     1) ASCENDING    2) DESCENDING', '\n')
    print('                                     YEARS:      3) ASCENDING    4) DESCENDING')
    separator_2()
    print('SORT NUMBER (#) OF TV EPISODES BY:   TITLES:     5) ASCENDING    6) DESCENDING', '\n')
    print('                                     AMOUNT:     7) ASCENDING    8) DESCENDING')
    separator_2()
    print('0) MAIN MENU')
    separator_3()

    try:

        sort_input = input('ENTER #: ')
        separator_3()
        sort_options_int = int(sort_input)

        if sort_options_int == 0:
            media_index_home()

        elif 1 <= sort_options_int <= 4:

            sort_function_base(sort_options_int=sort_options_int)

        elif 5 <= sort_options_int <= 8:

            tv_episodes_sort_function(sort_options_int=sort_options_int)

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

            graph_options_base(username, picture_graph_options_int='',
                               terminal_graph_options_int=terminal_graph_options_int)

        elif 5 <= terminal_graph_options_int <= 6:

            graph_options_advanced(username, picture_graph_options_int='',
                                   terminal_graph_options_int=terminal_graph_options_int)

        elif 7 <= terminal_graph_options_int <= 8:

            query_file_type_totals(username, picture_graph_options_int='',
                                   terminal_graph_options_int=terminal_graph_options_int)

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


def total_tv_episodes_in_show_title():
    tv_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), encoding='UTF-8')))
    total_query_action_list = []
    tv_amounts = []
    tv_show_episodes_found = []
    tv_show_found = {}

    try:

        tv_total_query_action = input('ENTER TV SHOW TITLE: ')
        separator_3()
        total_query_action_list.append(tv_total_query_action.lower())

    except (OSError, TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n', '\n', 'INVALID INPUT, PLEASE RETRY')

    for tv_title in tv_results_list:
        tv_amounts.append(tv_title[0])

    for found_tv_title in tv_amounts:
        if total_query_action_list[0] in found_tv_title.lower():
            tv_show_episodes_found.append(found_tv_title)
            tv_show_found[found_tv_title] = tv_show_episodes_found.count(found_tv_title)

    for episode in tv_show_found.items():
        print('TITLE NAME: NUMBER (#) OF EPISODES: ', '\n', episode)
        separator_3()
    print('NUMBER (#) OF EPISODES TOTAL: ', sum(tv_show_found.values()))
    separator_3()


def tv_episodes_sort_function(sort_options_int):
    tv_results_list = list(csv.reader(open(os.path.expanduser(
        (index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), encoding='UTF-8')))
    tv_amounts = []
    tv_show_episodes_found = []
    tv_show_found = {}

    for tv_title in tv_results_list:
        tv_amounts.append(tv_title[0])

    for found_tv_title in tv_amounts:
        tv_show_episodes_found.append(found_tv_title)
        tv_show_found[found_tv_title] = tv_show_episodes_found.count(found_tv_title)

    sorted_by_key_d = sorted(tv_show_found.items(), key=lambda kv: kv[0])
    sorted_by_key_a = sorted(tv_show_found.items(), key=lambda kv: kv[0], reverse=True)
    sorted_by_value_d = sorted(tv_show_found.items(), key=lambda kv: kv[1])
    sorted_by_value_a = sorted(tv_show_found.items(), key=lambda kv: kv[1], reverse=True)

    if sort_options_int == 5:
        for item in sorted_by_key_d:
            print('\n', item)
        separator_3()

    elif sort_options_int == 6:
        for item in sorted_by_key_a:
            print('\n', item)
        separator_3()

    elif sort_options_int == 7:
        for item in sorted_by_value_d:
            print('\n', item)
        separator_3()

    elif sort_options_int == 8:
        for item in sorted_by_value_a:
            print('\n', item)
        separator_3()


def username_check_and_folder_creation():
    global movie_dir_input, tv_dir_input, movie_alt_dir_input, tv_alt_dir_input

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
        main()


def walk_directories_and_create_indices():
    movie_video_files_results = []

    if movie_dir_input is not str(''):
        for root, dirs, files in os.walk(movie_dir_input):
            for movie_file in sorted(files):
                if movie_file.lower().endswith(extensions):
                    movie_video_files_results.append([(pathlib.Path(root) / movie_file).as_posix()])

    elif movie_alt_dir_input is not str(''):
        for listed_alternate_movie_directories in movie_alt_dir_input:
            for root, dirs, files in os.walk(listed_alternate_movie_directories):
                for alt_file in sorted(files):
                    if alt_file.lower().endswith(extensions):
                        movie_video_files_results.append([(pathlib.Path(root) / alt_file).as_posix()])

    with open(os.path.expanduser((index_folder + '/MOVIE_VIDEO_FILES_PATHS.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as f:
        csv_writer = csv.writer(f)
        for movie_row in sorted(movie_video_files_results):
            csv_writer.writerow(movie_row)

    tv_show_video_files_results = []

    if tv_dir_input is not str(''):
        for root, dirs, files in os.walk(tv_dir_input):
            for tv_file in sorted(files):
                if tv_file.lower().endswith(extensions):
                    tv_show_video_files_results.append([(pathlib.Path(root) / tv_file).as_posix()])

    elif tv_alt_dir_input is not str(''):
        for listed_alternate_tv_directories in tv_alt_dir_input:
            for root, dirs, files in os.walk(listed_alternate_tv_directories):
                for alt_file in sorted(files):
                    if alt_file.lower().endswith(extensions):
                        tv_show_video_files_results.append([(pathlib.Path(root) / alt_file).as_posix()])

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)), 'w',
              encoding='UTF-8', newline='') as f:
        csv_writer = csv.writer(f)
        for tv_row in sorted(tv_show_video_files_results):
            csv_writer.writerow(tv_row)


if __name__ == '__main__':
    main()
