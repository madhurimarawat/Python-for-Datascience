"""
Bulk_Zip_Cleaner_Sorter

A Python script to automatically extract, clean, and organize files
from multiple ZIP archives into a structured folder system.

-------------------------
🔧 What this script does:
-------------------------
1. Scans the current directory (or given folder) for all .zip files.
2. Extracts all ZIP files into a temporary folder.
3. Cleans filenames by removing unwanted parts like '_compressed'.
4. Identifies specific handwritten note patterns:
   - '_Handwritten_Index'
   - '_Handwritten_Notes'
5. Extracts meaningful prefixes from filenames.
6. Creates folders based on the first 1–2 words of each file.
7. Moves files into their respective folders.
8. Deletes the temporary extraction folder after processing.

-------------------------
🎯 Purpose:
-------------------------
To automate the tedious task of organizing large collections of
study materials, especially handwritten notes and resources.

-------------------------
📁 Output:
-------------------------
A clean 'organized/' folder with properly grouped files.

-------------------------
💡 Example:
-------------------------
Input:
    "Math Algebra _Handwritten_Notes_compressed.pdf"

Output:
    organized/
        └── Math Algebra/
              └── Math Algebra _Handwritten_Notes.pdf
"""

import os  # for file and directory operations
import zipfile  # for handling zip files
import shutil  # for moving and deleting files/folders

# === CONFIGURATION ===

outer_zip_folder = "."  # Folder containing ZIP files ('.' = current directory)
temp_extract = "temp_extracted"  # Temporary folder to extract ZIP contents
final_output = "organized"  # Final organized output folder

# Create required folders if they don't already exist
os.makedirs(temp_extract, exist_ok=True)
os.makedirs(final_output, exist_ok=True)

# === STEP 1: PROCESS EACH ZIP FILE ===

# Loop through all files in the given folder
for zip_name in os.listdir(outer_zip_folder):

    # Check if file is a ZIP archive
    if zip_name.endswith(".zip"):

        # Full path to the ZIP file
        zip_path = os.path.join(outer_zip_folder, zip_name)

        print(f"\n📦 Processing: {zip_name}")

        # Open and extract ZIP contents into temp folder
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_extract)

# === STEP 2: PROCESS EXTRACTED FILES ===

# Walk through all files inside the extracted folder (including subfolders)
for root, dirs, files in os.walk(temp_extract):

    for file in files:

        # Full path of the current file
        old_path = os.path.join(root, file)

        # Remove '_compressed' from filename (if present)
        new_name = file.replace("_compressed", "")

        # Identify if file matches required handwritten patterns
        if "_Handwritten_Index" in new_name:
            keyword = "_Handwritten_Index"
        elif "_Handwritten_Notes" in new_name:
            keyword = "_Handwritten_Notes"
        else:
            # Skip files that don't match required patterns
            continue

        # Extract part of filename before the keyword
        prefix = new_name.split(keyword)[0].strip()

        # Split prefix into words
        words = prefix.split()

        # Skip if filename has no valid words
        if not words:
            continue

        # Take first 1 or 2 words to form folder name
        folder_name = " ".join(words[:2])

        # Create folder inside final output directory
        folder_path = os.path.join(final_output, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Final path where file will be moved
        new_path = os.path.join(folder_path, new_name)

        # Move file to its respective folder
        shutil.move(old_path, new_path)

        print(f"📂 Moved: {new_name} → {folder_name}/")

# === STEP 3: CLEANUP ===

# Delete the temporary extraction folder to free space
shutil.rmtree(temp_extract)

print("\n✅ All ZIP files processed and organized successfully.")
