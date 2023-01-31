import json
import os

import pandas as pd

import tkinter as tk
from tkinter import filedialog

nx_directory = 'nx_directory.json'


def select_directory():
    try:
        directory = filedialog.askdirectory()
        with open(nx_directory, 'w+') as f:
            json.dump(directory, f)
        return directory
    except (IndexError, TypeError, ValueError):
        print("Error, No Excel Files in Directory")


def read_excel(file_path):
    data = pd.read_excel(file_path)
    return data


def display_data(data):
    text.config(state='normal')
    text.delete('1.0', tk.END)
    text.insert('1.0', data.to_string())
    text.config(state='disabled')


def submit():
    file_path = file_dict[dropdown_var.get()]
    data = read_excel(file_path)
    display_data(data)


root = tk.Tk()
root.title("NetXPerts Customer Information Directory")

try:
    if os.path.isfile(nx_directory):
        with open(nx_directory, "r") as f:
            directory = json.load(f)
    else:
        directory = select_directory()
except (IndexError, TypeError, ValueError):
    print("Error: ")

# Create a button to select directory
select_dir_button = tk.Button(root, text="Select Directory", command=select_directory)
select_dir_button.pack()

# Create a dropdown list to select Excel file
file_dict = {}
for file_name in os.listdir(directory):
    if file_name.endswith('.xls') or file_name.endswith(".xlsx"):
        file_path = os.path.join(directory, file_name)
        df = pd.read_excel(file_path)
        key = df.columns[0]
        file_dict[key] = file_path

try:
    dropdown_var = tk.StringVar(root)
    dropdown_var.set(list(file_dict.keys())[0])
    dropdown = tk.OptionMenu(root, dropdown_var, *file_dict.keys())
    dropdown.pack()
except (IndexError, TypeError, ValueError):
    print("Error: ")

# Create a submit button
submit_button = tk.Button(root, text="ENTER", command=submit)
submit_button.pack()

# Create the text box
text = tk.Text(root, state='disabled')
text.pack()

root.geometry('600x400')
root.mainloop()

