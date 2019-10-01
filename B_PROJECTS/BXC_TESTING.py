import random
import string
import textwrap
import time

from tkinter import filedialog, Tk


test_list = []
test_list_inverse = []


def get_bytes_from_files(filename):
    try:
        with open(filename, 'rb') as f:
            for byte in f.read():
                yield byte

    except (TypeError, ValueError, UnicodeDecodeError, ZeroDivisionError) as e:
        print(e)
        separator()
        print('INPUT ERROR, PLEASE RETRY SELECTION USING NUMBER KEYS: ')
        return


def inverse_bytes():
    test_file = tk_gui_file_selection_window()
    for bytes_found in get_bytes_from_files(test_file):
        bytes_found = int(bytes_found)
        bytes_remainder = int(256 - bytes_found)
        test_list.append(bytes_found)
        test_list_inverse.append(bytes_remainder)


def random_number_for_multiplier_bit():
    multiplier_digit = random.randint(1, 9)
    return int((multiplier_digit % 9) + 1)


def random_number_with_obscurer_digits(number_of_digits):
    number_range_start = 10 ** (number_of_digits - 1)
    number_range_end = (10 ** number_of_digits) - 1
    return random.randint(number_range_start, number_range_end)


def random_string_with_one_time_pad_characters(number_of_characters):
    one_time_pad_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(one_time_pad_characters) for _ in range(number_of_characters))


def rotate_list_as_rotor(character_set, rotations):
    return character_set[rotations:] + character_set[:rotations]


def separator():
    for item in '\n', '-' * 100, '\n':
        print(item)


def tk_gui_file_selection_window():
    root = Tk()
    root.withdraw()
    root.update()
    selected_file = filedialog.askopenfilename()
    root.destroy()
    return selected_file


separator()
start = time.time()
sequence = random_string_with_one_time_pad_characters(10000000)
print(textwrap.fill(sequence, 100))
separator()
end = time.time()
test_time = round(end - start, 2)
print("TIME ELAPSED:", test_time, 'Seconds')
separator()
