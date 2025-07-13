"""
📁 Folder Scanner Script

Author: Madhurima Rawat
Date: August 13, 2025

This script scans a specified directory and prints:
- Folder names
- File names with size and type
- Emoji-enhanced formatting for better readability

Useful for documenting folder contents or generating resource summaries.
"""

import os


def format_size(size_bytes):
    """
    Converts a file size in bytes to a human-readable string
    in B, KB, MB, or GB format, rounded to 2 decimal places.
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def scan_directory(root_dir):
    """
    Walks through the specified root directory and prints:
    - Folder names with 📁 emoji
    - File names with 📄 emoji
    - File sizes with 🧮 emoji
    - File extensions with 📦 emoji
    """
    for root, dirs, files in os.walk(root_dir):
        folder_name = os.path.basename(root)
        print(f"\n📁 Folder: {folder_name} ({root})")

        if not files:
            print("  🚫 No files in this folder.")

        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Fetch file size and extension
                size = os.path.getsize(file_path)
                file_size = format_size(size)
                file_ext = os.path.splitext(file)[1] or "No Extension"

                # Print file details with emojis
                print(f"  📄 {file}  |  🧮 {file_size}  |  📦 {file_ext}")
            except Exception as e:
                # Handle errors (e.g., permission denied, broken links)
                print(f"  ⚠️ Error reading file '{file}': {e}")


# Entry point: set folder path and begin scanning
if __name__ == "__main__":
    folder_to_scan = r"Study Materials"  # Specify the folder to scan here
    if os.path.exists(folder_to_scan):
        scan_directory(folder_to_scan)
    else:
        print("❌ Path does not exist. Please enter a valid directory.")
