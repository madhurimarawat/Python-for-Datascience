"""
📁 DIRECTORY TREE GENERATOR (Folders Only)

✨ Description:
This Python script prints a clean, visual tree structure of all folders
inside a given root directory — recursively (infinite depth).

It mimics the look of the Linux `tree` command, using:
├── for intermediate folders
└── for last folders
│   for vertical connections

🎯 Features:
- 📂 Displays only folder names (no files)
- 🔁 Recursive traversal (goes to deepest level)
- 🧼 Clean and readable tree structure
- ⚠️ Handles permission errors safely

💡 Use Case:
- Visualizing project structure
- Organizing files/folders
- Generating directory previews for documentation

👩‍💻 Author: Madhurima Rawat
"""

import os


def print_tree(root_path, prefix=""):
    """
    🌳 Recursively prints folder structure in tree format

    🔹 Parameters:
    - root_path (str): Path of the current directory
    - prefix (str): Used for formatting tree branches
    """

    try:
        # 📜 Get all items in the directory (sorted for consistency)
        items = sorted(os.listdir(root_path))
    except PermissionError:
        # 🚫 Skip folders without permission
        return

    # 📂 Filter only directories (ignore files)
    dirs = [item for item in items if os.path.isdir(os.path.join(root_path, item))]

    for i, directory in enumerate(dirs):
        # 📍 Full path of current folder
        path = os.path.join(root_path, directory)

        # 🔚 Check if this is the last folder in the list
        is_last = i == len(dirs) - 1

        # 🌿 Print tree branch
        if is_last:
            print(prefix + "└── " + directory)
            new_prefix = prefix + "    "  # ⬇️ No vertical line for last item
        else:
            print(prefix + "├── " + directory)
            new_prefix = prefix + "│   "  # 🔗 Continue vertical connection

        # 🔁 Recursive call for subdirectories
        print_tree(path, new_prefix)


# === 🚀 INPUT SECTION ===

# 🧾 Ask user for root folder path
root_folder = input("📁 Enter folder path: ")

# 🖨️ Print root folder name
print("\n" + root_folder)

# 🌳 Generate directory tree
print_tree(root_folder)
