"""
Script Name: File_Collector.py

Author: Madhurima Rawat

Purpose:
    This script traverses through Week 1 to Week 12 folders inside a given source directory.
    It looks for an "Assignment" subfolder in each week and copies all files from it into
    a single destination folder.

    To avoid filename conflicts, each copied file is prefixed with the week number
    (e.g., Week1_filename.ext).

Usage:
    - Set `source_base_path` to the directory containing "Week 1" to "Week 12" folders.
    - Set `destination_folder` to where you want to collect all assignment files.
    - Run the script in any Python environment with appropriate access permissions.
"""

import os
import shutil

# ✏️ Configure paths below
source_base_path = r"Source Path"  # Path to course directory
destination_folder = r"Destination Path"  # Path to save all assignments

# Create the destination folder if it doesn't already exist
os.makedirs(destination_folder, exist_ok=True)

# 🔁 Loop through Week 1 to Week 12
for week_num in range(1, 13):
    # Construct full path to the Assignment folder inside each week
    assignment_path = os.path.join(source_base_path, f"Week {week_num}", "Assignment")

    # ✅ Check if Assignment folder exists
    if os.path.exists(assignment_path):
        # Loop through all files inside Assignment folder
        for file_name in os.listdir(assignment_path):
            file_path = os.path.join(assignment_path, file_name)

            # ✅ Copy only files (skip directories)
            if os.path.isfile(file_path):
                # Prefix filename with week number to avoid overwriting
                dest_file_name = f"Week{week_num}_{file_name}"
                dest_path = os.path.join(destination_folder, dest_file_name)

                # Copy file preserving metadata
                shutil.copy2(file_path, dest_path)

        print(f"✅ Copied files from Week {week_num}")
    else:
        print(f"⚠️ Assignment folder not found in Week {week_num}")
