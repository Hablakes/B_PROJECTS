import os

import pyfiglet

from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor

from tkinter import filedialog, Tk

video_extensions = ('.3gp', '.asf', '.asx', '.avc', '.avi', '.bdmv', '.bin', '.bivx', '.dat', '.disc', '.divx', '.dv',
                    '.dvr-ms', '.evo', '.fli', '.flv', '.h264', '.img', '.iso', '.m2ts', '.m2v', '.m4v', '.mkv', '.mov',
                    '.mp4', '.mpeg', '.mpg', '.mt2s', '.mts', '.nrg', '.nsv', '.nuv', '.ogm', '.pva', '.qt', '.rm',
                    '.rmvb', '.strm', '.svq3', '.ts', '.ty', '.viv', '.vob', '.vp3', '.wmv', '.xvid', '.webm')


def main():
    separator_3()
    while True:
        interface()


def get_directory_to_scan():
    root = Tk()
    root.withdraw()
    root.update()
    selected_directory = filedialog.askdirectory()
    root.destroy()
    print('DIRECTORY INPUT: ', selected_directory)
    separator_3()
    return selected_directory


def interface():
    print(pyfiglet.figlet_format('BX_FILE_AUDITOR', font='cybermedium'))
    separator_1()
    print('\n', 'OPTIONS: ', '\n', '\n', '1) COMPARE TWO DIRECTORIES                         2) AUDIT A DIRECTORY',
          '\n', '\n', '3) FIND SUB-DIRECTORIES IN A DIRECTORY             4) FIND EXTRAS / FEATURETTES FOLDERS',
          '\n', '\n', '0) EXIT')

    separator_3()
    user_input = input('ENTER OPTION #: ')
    separator_3()

    try:
        if int(user_input) == 1:
            scan_and_compare_directories()

        elif int(user_input) == 2:
            scan_directory_folders()

        elif int(user_input) == 3:
            scan_for_sub_directories()

        elif int(user_input) == 4:
            scan_for_extras_and_featurettes_sub_directories()

        elif int(user_input) == 0:
            exit()

    except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
        print(e, '\n', ('-' * 100), '\n', 'INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
        return


def scan_and_compare_directories():
    print(pyfiglet.figlet_format('COMPARE', font='cybermedium'))
    print(pyfiglet.figlet_format('DIRECTORIES', font='cybermedium'))
    separator_3()

    first_directory_found_items_list = []
    second_directory_found_items_list = []

    print('FIRST DIRECTORY: ', '\n')
    first_directory_selected_in_function = [get_directory_to_scan()]

    print('SECOND DIRECTORY: ', '\n')
    second_directory_selected_in_function = [get_directory_to_scan()]

    for items in os.listdir(first_directory_selected_in_function[0]):
        if items not in os.listdir(second_directory_selected_in_function[0]):
            first_directory_found_items_list.append(items)

    for items in os.listdir(second_directory_selected_in_function[0]):
        if items not in os.listdir(first_directory_selected_in_function[0]):
            second_directory_found_items_list.append(items)

    print('ITEMS IN FIRST DIRECTORY THAT ARE NOT IN SECOND: ', '\n', '\n')
    for items in first_directory_found_items_list:
        print(items)
    separator_3()

    print('ITEMS IN SECOND DIRECTORY THAT ARE NOT IN FIRST: ', '\n', '\n')
    for items in second_directory_found_items_list:
        print(items)
    separator_3()


def scan_directory_folders():
    print(pyfiglet.figlet_format('SPACE_AUDITOR', font='cybermedium'))
    separator_3()

    found_directories_average_file_size_list = []
    found_directories_average_video_size_list = []
    found_directories_total_folder_size_list = []
    found_counts_list = []

    graph = Pyasciigraph(separator_length=2)
    directory_selected_in_function = [get_directory_to_scan()]

    for found_dirs in os.listdir(directory_selected_in_function[0]):
        found_sub_directories_count = 0
        found_files_count = 0
        found_video_files_count = 0
        total_folder_size = 0
        directory_path = directory_selected_in_function[0] + '/' + found_dirs

        if os.path.isdir(directory_path):
            for found_items in os.listdir(directory_path):

                if os.path.isdir(directory_path + '/' + found_items):
                    found_sub_directories_count = found_sub_directories_count + 1

                elif os.path.isfile(directory_path + '/' + found_items) and found_items.endswith(video_extensions):
                    found_video_files_count = found_video_files_count + 1

                else:
                    found_files_count = found_files_count + 1
            found_counts_list.append([found_dirs, 'FILES', found_files_count, 'VIDEOS',
                                      found_video_files_count, 'SUB-DIRECTORIES', found_sub_directories_count])

        else:
            found_files_count = found_files_count + 1
            found_counts_list.append(
                [found_dirs, 'FILES', found_files_count, 'VIDEOS', found_video_files_count, 'SUB-DIRECTORIES',
                 found_sub_directories_count])

        try:

            for path, dirs, files in os.walk(directory_path):
                for f in files:
                    fp = os.path.join(path, f)
                    total_folder_size += os.path.getsize(fp)

        except (FileExistsError, FileNotFoundError, OSError, TypeError, ValueError) as e:
            print('\n', 'FILE ERROR: ', e)
            separator_3()

        if int(found_files_count) > 0:
            total_folder_size_in_mb = (int(total_folder_size) / 1048576)
            average_file_size = total_folder_size_in_mb / found_files_count
            average_file_size_in_mb = str(int(average_file_size))[:4]
            found_directories_total_folder_size_list.append([found_dirs, total_folder_size_in_mb])
            found_directories_average_file_size_list.append([found_dirs, int(average_file_size_in_mb)])

            if int(found_video_files_count) > 0:
                average_video_file_size = total_folder_size_in_mb / found_video_files_count
                average_video_file_size_in_mb = str(int(average_video_file_size))[:4]
                found_directories_average_video_size_list.append([found_dirs, int(average_video_file_size_in_mb)])
        else:
            total_folder_size_in_mb = (int(total_folder_size) / 1048576)
            average_file_size_in_mb = int(0)
            average_video_file_size_in_mb = int(0)
            found_directories_total_folder_size_list.append([found_dirs, total_folder_size_in_mb])
            found_directories_average_file_size_list.append([found_dirs, int(average_file_size_in_mb)])
            found_directories_average_video_size_list.append([found_dirs, int(average_video_file_size_in_mb)])

    sorted_found_directories_total_list = sorted(found_directories_total_folder_size_list, reverse=True,
                                                 key=lambda x: x[1])
    sorted_found_directories_average_list = sorted(found_directories_average_file_size_list, reverse=True,
                                                   key=lambda x: x[1])
    sorted_found_directories_vid_avg_list = sorted(found_directories_average_video_size_list, reverse=True,
                                                   key=lambda x: x[1])
    graph_color_pattern = [Gre, Blu, Pur, Red]
    color_coded_directory_totals = vcolor(sorted_found_directories_total_list, graph_color_pattern)
    color_coded_directory_averages = vcolor(sorted_found_directories_average_list, graph_color_pattern)
    color_coded_directory_vid_avg = vcolor(sorted_found_directories_vid_avg_list, graph_color_pattern)

    def sub_interface():
        while True:
            print('PLEASE SELECT AN OPTION: ', '\n', '\n', '1) SORT BY TOTAL SIZE'
                                                           '                             2) SORT BY AVERAGE FILE-SIZE',
                  '\n',
                  '\n', '3) SORT BY AVERAGE VIDEO FILE-SIZE'
                        '                4) SCAN A DIFFERENT DIRECTORY', '\n', '\n', '0) MAIN MENU')
            separator_3()
            bct_input = input('ENTER OPTION #: ')
            separator_3()

            try:

                if int(bct_input) == 1:
                    for line in graph.graph('DIRECTORY TOTALS - (TOTAL SIZE IN MB, DIRECTORY): ',
                                            data=color_coded_directory_totals):
                        print(line, '\n', ('-' * 100))
                    print()
                    separator_3()

                elif int(bct_input) == 2:
                    for line in graph.graph('DIRECTORY TOTALS - (AVERAGE FILE-SIZE IN MB, DIRECTORY): ',
                                            data=color_coded_directory_averages):
                        print(line, '\n', ('-' * 100))
                    print()
                    separator_3()

                elif int(bct_input) == 3:
                    for line in graph.graph('DIRECTORY TOTALS - (AVERAGE VIDEO FILE-SIZE IN MB, DIRECTORY): ',
                                            data=color_coded_directory_vid_avg):
                        print(line, '\n', ('-' * 100))
                    print()
                    separator_3()

                elif int(bct_input) == 4:
                    scan_directory_folders()

                elif int(bct_input) == 0:
                    return

            except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
                print(e, '\n', ('-' * 100), '\n', 'INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
                return

    sub_interface()


def scan_for_extras_and_featurettes_sub_directories():
    print(pyfiglet.figlet_format('SUB_DIRECTORY', font='cybermedium'))
    print(pyfiglet.figlet_format('FINDER', font='cybermedium'))
    separator_3()

    directory_selected_in_function_for_search = [get_directory_to_scan()]

    for found_directories in os.listdir(directory_selected_in_function_for_search[0]):
        directory_path = directory_selected_in_function_for_search[0] + '/' + found_directories

        for found_items in os.listdir(directory_path):
            if os.path.isdir(directory_path + '/' + found_items):
                if found_items.lower() == str('Extras').lower() or found_items.lower() == str(
                        'Featurettes').lower() or found_items.lower() == str('Specials').lower():
                    print('SUB-DIRECTORIES: ', (directory_path + '/' + found_items), '\n', '\n')
    separator_1()


def scan_for_sub_directories():
    print(pyfiglet.figlet_format('SUB_DIRECTORY', font='cybermedium'))
    print(pyfiglet.figlet_format('FINDER', font='cybermedium'))
    separator_3()

    directory_selected_in_function_for_search = [get_directory_to_scan()]

    for found_directories in os.listdir(directory_selected_in_function_for_search[0]):
        directory_path = directory_selected_in_function_for_search[0] + '/' + found_directories
        print('\n', 'DIRECTORY: ', found_directories, '\n', '\n')

        for found_items in os.listdir(directory_path):
            if os.path.isdir(directory_path + '/' + found_items):
                print('SUB-DIRECTORIES: ', found_items, '\n', '\n')
        separator_1()


def separator_1():
    print('-' * 100)


def separator_2():
    for items in '\n', '-' * 100:
        print(items)


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


if __name__ == '__main__':
    main()
