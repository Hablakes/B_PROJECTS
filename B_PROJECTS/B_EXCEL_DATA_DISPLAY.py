import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import json


def select_directory():
    directory = filedialog.askdirectory()
    with open('directory.json', 'w') as f:
        json.dump(directory, f)
    return directory


def read_excel(file_path):
    data = pd.read_excel(file_path)
    return data


def display_data(data):
    display_space.config(text=data.to_string(index=False))


def submit():
    file_path = file_dict[dropdown_var.get()]
    data = read_excel(file_path)
    display_data(data)


root = tk.Tk()
root.title("Excel Data Display")

try:
    with open("directory.json", "r") as f:
        directory = json.load(f)

except Exception:
    directory = select_directory()

# Create a button to select directory
select_dir_button = tk.Button(root, text="Select Directory", command=select_directory)
select_dir_button.pack()

# Create a dropdown list to select Excel file
file_dict = {}
for file_name in os.listdir(directory):
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(directory, file_name)
        df = pd.read_excel(file_path)
        key = df.columns[0]
        file_dict[key] = file_path

dropdown_var = tk.StringVar(root)
dropdown_var.set(list(file_dict.keys())[0])
dropdown = tk.OptionMenu(root, dropdown_var, *file_dict.keys())
dropdown.pack()

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Create a space to display data
display_space = tk.Label(root)
display_space.pack()

root.geometry('600x400')
root.mainloop()
