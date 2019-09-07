from tkinter import filedialog, Tk

username = 'TEST'


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


def directory_selection():

    try:
        separator_3()
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

        if alternate_directory_prompt == str('y'):

            movie_alt_directories_list = list()
            print('ENTER ALTERNATE MOVIE DIRECTORIES: ')
            separator_3()

            movie_directory_input_line = tk_gui_file_browser_window()

            while movie_directory_input_line != '':
                movie_alt_directories_list.append(movie_directory_input_line)
                movie_directory_input_line = tk_gui_file_browser_window()

            movie_alt_dir_input = list(movie_alt_directories_list)
            print('DIRECTORIES ENTERED: ', '\n', '\n', movie_alt_dir_input)

            tv_alt_directories_list = list()
            separator_3()
            print('ENTER ALTERNATE TV DIRECTORIES: ')
            separator_3()

            tv_directory_input_line = tk_gui_file_browser_window()

            while tv_directory_input_line != '':
                tv_alt_directories_list.append(tv_directory_input_line)
                tv_directory_input_line = tk_gui_file_browser_window()

            tv_alt_dir_input = list(tv_alt_directories_list)
            print('DIRECTORIES ENTERED: ', '\n', '\n', tv_alt_dir_input)

            user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input, 'tv_dir:': tv_dir_input,
                              'movie_alt_dir:': movie_alt_dir_input, 'tv_alt_dir:': tv_alt_dir_input}

            separator_3()
            print('RESULTS: ', user_info_dict)

        elif alternate_directory_prompt != str('y'):

            print('NO ALTERNATE DIRECTORIES')
            separator_3()

            user_info_dict = {'user:': username, 'movie_dir:': movie_dir_input, 'tv_dir:': tv_dir_input,
                              'movie_alt_dir:': '', 'tv_alt_dir:': ''}

            print('RESULTS: ', user_info_dict)

    except (TypeError, ValueError) as e:
        print('\n', 'INPUT ERROR: ', e, '\n')


directory_selection()
