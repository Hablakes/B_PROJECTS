import os


def rename_files(folder_path, season, episode_start):
    for i, file_name in enumerate(os.listdir(folder_path)):
        # Get the file extension
        file_extension = os.path.splitext(file_name)[1]

        # Get the current file path
        current_file_path = os.path.join(folder_path, file_name)

        # Generate the new file name using the input scheme
        new_file_name = f"Star Trek Voyager - S{season:02d}E{i+episode_start:02d}{file_extension}"

        # Get the new file path
        new_file_path = os.path.join(folder_path, new_file_name)

        # Rename the file
        os.rename(current_file_path, new_file_path)


rename_files('C:/Users/botoole/Documents/BX STUFF/CODING TESTS/', 1, 1)
