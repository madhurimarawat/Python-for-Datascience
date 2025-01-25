"""
File Renaming Script
====================
Author: Madhurima Rawat
Date: 2025-01-25
Description:
This script reads all files from a specified directory and renames them sequentially
in the format "Lecture-01", "Lecture-02", and so on. It handles files with numeric names
inconsistent formats (e.g., "Lec01", "lec10", "Lec23") and ensures proper sorting
based on numeric values.

Features:
- Extracts numeric parts of file names for sorting.
- Renames files while preserving their original extensions.
- Logs the renaming process for user clarity.

Usage:
1. Set the `directory_path` variable to the folder containing your files.
2. Run the script.
3. Files will be renamed sequentially in the "Lecture-XX" format.

Note:
- Ensure the script has permission to read and write in the specified directory.
- Backup files before running the script if needed.
"""

import os
import re


def extract_numeric_part(file_name):
    """
    Extract the numeric part from the file name for sorting.

    Args:
        file_name (str): The name of the file.

    Returns:
        int: The numeric part of the file name. If no number is found, return infinity.
    """
    match = re.search(
        r"\d+", file_name
    )  # Search for the first numeric value in the file name
    return (
        int(match.group()) if match else float("inf")
    )  # Return the number or infinity if none exists


def rename_files_in_directory(directory_path):
    """
    Rename all files in the specified directory sequentially in the "Lecture-XX" format.

    Args:
        directory_path (str): The path to the directory containing files.

    Returns:
        None
    """
    try:
        # Step 1: List all files in the directory
        files = [
            f
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]

        # Step 2: Sort files based on the numeric part of their names
        files.sort(key=extract_numeric_part)

        # Step 3: Rename each file sequentially
        for i, file_name in enumerate(files, start=1):
            # Extract file extension (e.g., ".pdf", ".txt")
            file_extension = os.path.splitext(file_name)[1]

            # Create the new file name in the "Lecture-XX" format
            new_name = f"Lecture-{i:02d}{file_extension}"

            # Get full paths for the current and new file names
            old_path = os.path.join(directory_path, file_name)
            new_path = os.path.join(directory_path, new_name)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {file_name} -> {new_name}")

    except Exception as e:
        # Log any errors encountered during the process
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    # Set the directory containing the files to rename
    directory_path = r"path\to\directory"  # Replace with source directory path

    # Call the function to rename files
    rename_files_in_directory(directory_path)
