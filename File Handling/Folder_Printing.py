"""
Program Name: Outer Folder Lister
Author: Madhurima Rawat
Description:
    This program lists and prints the names of all immediate
    subdirectories (outer folders) present inside a given directory.
    It is useful for organizing and reviewing folder structures,
    such as subject-wise or category-wise study materials.
"""

import os


def print_outer_folders(path):
    """
    Prints the names of all immediate subfolders (outer folders)
    present inside the given directory path.
    """

    # Iterate through all items in the specified directory
    for item in os.listdir(path):

        # Create the complete path of the item
        full_path = os.path.join(path, item)

        # Check whether the item is a directory (not a file)
        if os.path.isdir(full_path):

            # Print only the folder name
            print(item)


# ---------------------- Example Usage ----------------------

# Path containing subject-wise or category-wise folders
outer_folder = r"folder_path"

# Call the function to display outer folder names
print_outer_folders(outer_folder)
