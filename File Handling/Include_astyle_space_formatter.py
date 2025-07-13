"""
The function `add_space_after_includes` adds a space after `#include` statements in all C/C++ files
within a specified directory.

:param directory: The `directory` parameter in the `add_space_after_includes` function is a string
that represents the directory path containing C/C++ files. This function is designed to add a space
after `#include` statements in all C/C++ files within the specified directory.
"""

# For directory and file functions
import os

# For matching with regular expressions (finding #include)
import re

# Function to add space after #include
def add_space_after_includes(directory, extension):
    """
    Add a space after #include in all C/C++ files in the specified directory.

    Args:
    - directory (str): Directory path containing C/C++ files.
    - extension (str): File extension to work with (either ".c" or ".cpp").

    Returns:
    - str: Name of the main directory where the files were processed.
    """
    include_pattern = re.compile(r'#include\s*<')

    # Printing main directory name
    print(f"-----\nMain Directory  {os.path.basename(directory)}\n-----")

    # Walk through all files in the directory and its subdirectories
    for subdir, _, files in os.walk(directory):
        # Printing subdirectory name
        print(f"----\nSubdirectory  {os.path.basename(subdir)}\n----")

        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(subdir, file)

                # Read the file content
                with open(file_path, 'r') as f:
                    content = f.read()

                # Update the content by adding space after #include
                updated_content = include_pattern.sub('#include <', content)

                # Printing file path and name
                print(f"Formatted  {file_path}")

                # Write the updated content back to the file
                with open(file_path, 'w') as f:
                    f.write(updated_content)

    return os.path.basename(directory)


def main():
    # Prompt the user to choose the file extension type
    extension_type = input("Enter the file extension to work with (1 for C, 2 for C++): ")

    if extension_type == '1':
        extension = ".c"
    elif extension_type == '2':
        extension = ".cpp"
    else:
        print("Invalid option. Please choose 1 or 2.")
        return

    # Take input directory path
    directory_path = input("Enter the directory path containing C/C++ files: ")

    # Prompt user to choose save location
    save_option = input("Do you want to save modified files in the same directory (press 1) or a new directory (press 2)? ")

    if save_option == '1':
        saved_directory = add_space_after_includes(directory_path, extension)
    elif save_option == '2':
        new_directory = input("Enter the path to save the modified files: ")
        saved_directory = add_space_after_includes(directory_path, extension)
        # Move modified files to the new directory
        for subdir, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(extension):
                    old_path = os.path.join(subdir, file)
                    new_path = os.path.join(new_directory, file)
                    os.rename(old_path, new_path)
    else:
        print("Invalid option. Please choose 1 or 2.")
        return

    # Print the name of the directory where files are saved
    print(f"\nFiles saved in directory: {saved_directory}")


if __name__ == "__main__":
    main()