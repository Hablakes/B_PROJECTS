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

username_input = None
media_index_folder = '~/{0}_MEDIA_INDEX'

extensions = ('.3gp', '.asf', '.asx', '.avc', '.avi', '.bdmv', '.bin', '.bivx', '.dat', '.disc', '.divx', '.dv',
              '.dvr-ms', '.evo', '.fli', '.flv', '.h264', '.img', '.iso', '.m2ts', '.m2v', '.m4v', '.mkv', '.mov',
              '.mp4', '.mpeg', '.mpg', '.mt2s', '.mts', '.nfo', '.nrg', '.nsv', '.nuv', '.ogm', '.pva', '.qt', '.rm',
              '.rmvb', '.strm', '.svq3', '.ts', '.ty', '.viv', '.vob', '.vp3', '.wmv', '.xvid', '.webm')

nfo_extensions = ".nfo"
srt_extensions = ".srt"

years_range = range(1900, 2100, 1)
movie_string = str("MOVIE")
tv_string = str("TV")


def sep():
    for item in "\n", '-' * 100, "\n":
        print(item)


def run_picture_graphs():
    print(pyfiglet.figlet_format("PICTURE-GRAPHS", font="cybermedium"))
    sep()
    print("1) MOVIES (TITLES PER YEAR)         - 2) TV SHOWS (TITLES PER YEAR)")
    print()
    print("3) MOVIES (TITLES PER DECADE)       - 4) TV SHOWS (TITLES PER DECADE)")
    print()
    print("5) MOVIES (RESOLUTIONS PERCENTAGES) - 6) TV SHOWS (RESOLUTIONS PERCENTAGES)")
    print()
    print("7) MOVIES (FILE-TYPE AMOUNTS)       - 8) TV SHOWS (FILE-TYPE AMOUNTS)                - 9) EXIT")
    sep()
    picture_graph_options = input("ENTER #")
    sep()
    picture_graph_options_int = int(picture_graph_options)
    if picture_graph_options_int == 1:
        bar_graph_options_base(username_input, picture_graph_options_int=1)
    elif picture_graph_options_int == 2:
        bar_graph_options_base(username_input, picture_graph_options_int=2)
    elif picture_graph_options_int == 3:
        bar_graph_options_base(username_input, picture_graph_options_int=3)
    elif picture_graph_options_int == 4:
        bar_graph_options_base(username_input, picture_graph_options_int=4)
    elif picture_graph_options_int == 5:
        pie_chart_options_base(username_input, picture_graph_options_int=5)
    elif picture_graph_options_int == 6:
        pie_chart_options_base(username_input, picture_graph_options_int=6)
    elif picture_graph_options_int == 7:
        search_file_type_totals_movies(username_input, picture_graph_options_int=7,
                                       terminal_graph_options_int='', b_totals_query_input_int='')
    elif picture_graph_options_int == 8:
        search_file_type_totals_tv(username_input, picture_graph_options_int=8,
                                   terminal_graph_options_int='', b_totals_query_input_int='')
    elif picture_graph_options_int == 9:
        pass


def bar_graph_options_base(username_input, picture_graph_options_int):
    media_index_list = list(
        csv.reader(open(os.path.expanduser(r'~/{0}-MEDIA-INDEX/MEDIA-INDEX.csv'.format(username_input)),
                        encoding='UTF8')))
    movie_years_dict = {}
    movie_decades_dict = {}
    tv_decades_amount_dict = {}
    tv_years_dict = {}
    movie_year_totals_dict = {}
    movie_decades_totals_dict = {}
    tv_year_totals_dict = {}
    tv_decades_totals_dict = {}

    for title_item in media_index_list:
        title_item_year = re.split("(.+) \((\d{4})\)", title_item[2], flags=0)
        title_item_year_int = int(title_item_year[0])
        title_item_decade_int = int(title_item_year[0][:-1] + '0')
        if title_item_year_int in years_range:
            if movie_string in title_item:
                if title_item_year_int not in movie_years_dict:
                    movie_years_dict[title_item_year_int] = []
                movie_years_dict[title_item_year_int].append(title_item)
                if title_item_decade_int not in movie_decades_dict:
                    movie_decades_dict[title_item_decade_int] = []
                movie_decades_dict[title_item_decade_int].append(title_item)
            if tv_string in title_item:
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
        plt.savefig(os.path.expanduser(r'~/{0}-MEDIA-INDEX/FILES/MOVIE-YEAR-RESULTS.png'.format(username_input)))
        plt.show()

    if picture_graph_options_int == 2:

        for year_values, value in sorted(tv_years_dict.items()):
            tv_year_totals_dict[year_values] = len(value)
        x, y = zip(*sorted(tv_year_totals_dict.items()))
        plt.bar(x, y)
        plt.savefig(os.path.expanduser(r'~/{0}-MEDIA-INDEX/FILES/TV-YEAR-RESULTS.png'.format(username_input)))
        plt.show()

    if picture_graph_options_int == 3:

        for year_values, value in sorted(movie_decades_dict.items()):
            movie_decades_totals_dict[year_values] = len(value)
        x, y = zip(*movie_decades_totals_dict.items())
        plt.bar(x, y, width=5)
        plt.savefig(os.path.expanduser(r'~/{0}-MEDIA-INDEX/FILES/MOVIE-DECADE-RESULTS.png'.format(username_input)))
        plt.show()

    if picture_graph_options_int == 4:

        for year_values, value in sorted(tv_decades_amount_dict.items()):
            tv_decades_totals_dict[year_values] = len(value)
        x, y = zip(*tv_decades_totals_dict.items())
        plt.bar(x, y, width=5)
        plt.savefig(os.path.expanduser(r'~/{0}-MEDIA-INDEX/FILES/TV-DECADE-RESULTS.png'.format(username_input)))
        plt.show()


def pie_chart_options_base(username_input, picture_graph_options_int):
    movie_files_results_list = list(
        csv.reader(open(os.path.expanduser(r'~/{0}-MEDIA-INDEX/MOVIE-RESULTS.csv'.format(username_input)),
                   encoding='UTF8')))
    tv_files_results_list = list(
        csv.reader(open(os.path.expanduser(r'~/{0}-MEDIA-INDEX/TV-RESULTS.csv'.format(username_input)),
                   encoding='UTF8')))

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

        if re.findall("19\d{2}x", res[3]):
            m_ten_eighty_found_list.append(res)
        elif re.findall("1[0-8]\d{2}x", res[3]):
            m_seven_twenty_found_list.append(res)
        elif re.findall("\d{3}x", res[3]):
            m_standard_def_found_list.append(res)
        else:
            m_empty_response_list.append(+1)
        movies_total_list.append(+1)

    movie_data = [float(len(m_ten_eighty_found_list)), float(len(m_seven_twenty_found_list)),
                  float(len(m_standard_def_found_list))]

    for res in tv_files_results_list:

        if re.findall("19\d{2}x", res[6]):
            tv_ten_eighty_found_list.append(res)
        elif re.findall("1[0-8]\d{2}x", res[6]):
            tv_seven_twenty_found_list.append(res)
        elif re.findall("\d{3}x", res[6]):
            tv_standard_def_found_list.append(res)
        else:
            tv_empty_response_list.append(+1)
        tv_total_list.append(+1)

    tv_data = [float(len(tv_ten_eighty_found_list)), float(len(tv_seven_twenty_found_list)),
               float(len(tv_standard_def_found_list))]

    def format_data(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    labels = ['1080p', '720p', 'SD (Below 720p)']

    colors = ['#85c1e9', '#a569bd', '#808b96']

    if picture_graph_options_int == 5:
        fig, ax = plt.subplots(figsize=(20, 10), subplot_kw=dict(aspect="equal"))

        wedges, texts, autotexts = ax.pie(movie_data, autopct=lambda pct: format_data(pct, movie_data),
                                          shadow=True, colors=colors, textprops=dict(color="black"))

        ax.legend(wedges, labels,
                  title="RESOLUTIONS",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=9, weight='bold')
        ax.set_title("MOVIE-RESOLUTION-RESULTS")
        plt.savefig(
            os.path.expanduser(r'~/{0}-MEDIA-INDEX/FILES/MOVIE-RESOLUTION-RESULTS.png'.format(username_input)))
        plt.show()

    if picture_graph_options_int == 6:
        fig, ax = plt.subplots(figsize=(20, 10), subplot_kw=dict(aspect="equal"))

        wedges, texts, autotexts = ax.pie(tv_data, autopct=lambda pct: format_data(pct, tv_data),
                                          shadow=True, colors=colors, textprops=dict(color="black"))

        ax.legend(wedges, labels,
                  title="RESOLUTIONS",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=9, weight='bold')
        ax.set_title("TV-SHOW-RESOLUTION-RESULTS")
        plt.savefig(
            os.path.expanduser(r'~/{0}-MEDIA-INDEX/FILES/TV-RESOLUTION-RESULTS.png'.format(username_input)))
        plt.show()


def search_file_type_totals_movies(username_input, b_totals_query_input_int, picture_graph_options_int,
                                   terminal_graph_options_int):
    movie_file_index = list(
        csv.reader(open(os.path.expanduser(r'~/{0}-MEDIA-INDEX/MOVIE-RESULTS.csv'.format(username_input)),
                        encoding='UTF8')))
    extensions_dict = {}
    extensions_totals = {}

    for file_type in movie_file_index:
        if str(',') not in file_type[4]:
            if file_type[4] not in extensions_dict:
                extensions_dict[file_type[4]] = []
            extensions_dict[file_type[4]].append(file_type[4])
    movie_file_type_totals = {}

    if b_totals_query_input_int == 7:

        for movie_file_type_values, value in sorted(extensions_dict.items()):
            movie_file_type_totals[movie_file_type_values] = len(value)
        print()
        print("TOTAL AMOUNTS OF FILE-TYPES IN MOVIES:")
        print()
        for items in movie_file_type_totals.items():
            print()
            print(items)
        sep()

    if picture_graph_options_int == 7:

        for movie_file_type_values, value in sorted(extensions_dict.items()):
            movie_file_type_totals[movie_file_type_values] = len(value)

        x, y = zip(*sorted(movie_file_type_totals.items()))
        plt.bar(x, y)
        plt.savefig(
            os.path.expanduser(r'~/{0}-MEDIA-INDEX/FILES/MOVIE-FILE-TYPE-RESULTS.png'.format(username_input)))
        plt.show()

    if terminal_graph_options_int == 7:

        for file_type_values, value in sorted(extensions_dict.items()):
            extensions_totals[file_type_values] = len(value)

        file_type_totals_terminal_graph_list = []

        for key, value in extensions_totals.items():
            file_type_totals_terminal_graph_list.append((str(key), value))

        graph = Pyasciigraph()
        for line in graph.graph('MOVIES: FILE-TYPE AMOUNTS', file_type_totals_terminal_graph_list):
            print()
            print(line)
        sep()


def search_file_type_totals_tv(username_input, b_totals_query_input_int, picture_graph_options_int,
                               terminal_graph_options_int):
    tv_file_index = list(
        csv.reader(open(os.path.expanduser(r'~/{0}-MEDIA-INDEX/TV-RESULTS.csv'.format(username_input)),
                        encoding='UTF8')))
    extensions_dict = {}
    extensions_totals = {}

    for file_type in tv_file_index:
        if str(',') not in file_type[7]:
            if file_type[7] not in extensions_dict:
                extensions_dict[file_type[7]] = []
            extensions_dict[file_type[7]].append(file_type[7])
    tv_file_type_totals = {}

    if b_totals_query_input_int == 8:

        for tv_file_type_values, value in sorted(extensions_dict.items()):
            tv_file_type_totals[tv_file_type_values] = len(value)
        print()
        print("TOTAL AMOUNTS OF FILE-TYPES IN TV SHOWS:")
        print()
        for items in tv_file_type_totals.items():
            print()
            print(items)
        sep()

    if picture_graph_options_int == 8:

        for tv_file_type_values, value in sorted(extensions_dict.items()):
            tv_file_type_totals[tv_file_type_values] = len(value)

        x, y = zip(*sorted(tv_file_type_totals.items()))
        plt.bar(x, y)
        plt.savefig(os.path.expanduser(r'~/{0}-MEDIA-INDEX/FILES/TV-FILE-TYPE-RESULTS.png'.format(username_input)))
        plt.show()

    if terminal_graph_options_int == 8:

        for file_type_values, value in sorted(extensions_dict.items()):
            extensions_totals[file_type_values] = len(value)

        file_type_totals_terminal_graph_list = []

        for key, value in extensions_totals.items():
            file_type_totals_terminal_graph_list.append((str(key), value))

        graph = Pyasciigraph()
        for line in graph.graph('TV SHOWS: FILE-TYPE AMOUNTS', file_type_totals_terminal_graph_list):
            print()
            print(line)
        sep()

