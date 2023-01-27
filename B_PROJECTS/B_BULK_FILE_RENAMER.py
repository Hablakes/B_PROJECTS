import os
from tkinter import *
from tkinter import filedialog


def rename_files():
    folder_path = filedialog.askdirectory()
    season = entry_season.get()
    episode_start = entry_episode.get()
    numbering_scheme = var.get()

    for i, file_name in enumerate(os.listdir(folder_path)):
        # Get the file extension
        file_extension = os.path.splitext(file_name)[1]

        # Get the current file path
        current_file_path = os.path.join(folder_path, file_name)

        if numbering_scheme == "season_episode":
            # Generate the new file name using the input scheme
            new_file_name = f"S{season:02d}E{i + int(episode_start):02d}{file_extension}"
        else:
            # Generate the new file name using the input scheme
            new_file_name = f"{i + int(episode_start):02d}{file_extension}"

        # Get the new file path
        new_file_path = os.path.join(folder_path, new_file_name)

        # Rename the file
        os.rename(current_file_path, new_file_path)


root = Tk()
root.title("Bulk File Renamer")

# Season entry
label_season = Label(root, text="Season:")
label_season.grid(row=0, column=0)
entry_season = Entry(root)
entry_season.grid(row=0, column=1)

# Episode entry
label_episode = Label(root, text="Starting Episode:")
label_episode.grid(row=1, column=0)
entry_episode = Entry(root)
entry_episode.grid(row=1, column=1)

# Numbering scheme
var = StringVar(value="season_episode")
Radiobutton(root, text="Season and Episode", variable=var, value="season_episode").grid(row=2, column=0)
Radiobutton(root, text="Only Episode", variable=var, value="episode_only").grid(row=2, column=1)

# Rename button
rename_button = Button(root, text="Rename", command=rename_files)
rename_button.grid(row=3, column=0)

root.mainloop()
