import csv
import os
import pathlib

username_input = None
media_index_folder = '~/{0}_MEDIA_INDEX'

extensions = ('.3gp', '.asf', '.asx', '.avc', '.avi', '.bdmv', '.bin', '.bivx', '.dat', '.disc', '.divx', '.dv',
              '.dvr-ms', '.evo', '.fli', '.flv', '.h264', '.img', '.iso', '.m2ts', '.m2v', '.m4v', '.mkv', '.mov',
              '.mp4', '.mpeg', '.mpg', '.mt2s', '.mts', '.nfo', '.nrg', '.nsv', '.nuv', '.ogm', '.pva', '.qt', '.rm',
              '.rmvb', '.strm', '.svq3', '.ts', '.ty', '.viv', '.vob', '.vp3', '.wmv', '.xvid', '.webm')


def compare_results(results_user, results_other):
    output = []

    for line in results_user:
        if line not in results_other:
            output.append('HAVE: ' + line)

    for line in results_other:
        if line not in results_user:
            output.append('DO NOT HAVE: ' + line)

    return output


def compare_results_files_and_create_differences_file():
    movie_comparison_list = []
    tv_comparison_list = []

    print()
    comparison_username = input('ENTER USERNAME FOR THE RESULTS LISTS TO COMPARE: ')

    with open(os.path.expanduser((media_index_folder + '/MOVIE_INFORMATION_INDEX.csv').format(username_input)), 'r',
              encoding='UTF-8') as m_0, open(os.path.expanduser(r'~/{0}/'.format(username_input)) + comparison_username
                                             + '_MEDIA_INDEX/MOVIE_INFORMATION_INDEX.csv', 'r',
                                             encoding='UTF-8') as m_1:
        movie_results = m_0.readlines()
        comparison_movie_results = m_1.readlines()

        for lines in compare_results(movie_results, comparison_movie_results):
            movie_comparison_list.append(lines)

