"""
Image Batch Converter to Lossless PNG Format
--------------------------------------------

This script recursively scans an input folder for supported image formats
(.jpg, .jpeg, .png, .bmp, .tiff), converts each image to a lossless PNG format,
and saves it in the specified output folder while preserving the directory structure.

Key Features:
- Maintains original image dimensions (no resizing).
- Converts all images to PNG using lossless compression.
- Calculates and prints detailed file size statistics for each image and total space saved.
- Handles common image formats and ensures RGBA compatibility for consistency.

Usage:
- Set INPUT_FOLDER and OUTPUT_FOLDER to the desired source and destination directories.
- Run the script directly using: `python script_name.py`

Dependencies:
- Pillow (Python Imaging Library fork) for image processing.
"""

# Author: Madhurima Rawat
# Date: June 5, 2025
# GitHub: https://github.com/madhurimarawat

# Importing Libraries
import os
from PIL import Image
from pathlib import Path

# 📁 Define input and output folders here
INPUT_FOLDER = "input_folder"  # 🔍 Folder with original images
OUTPUT_FOLDER = "output_folder"  # 💾 Folder to save processed images

# 🖼️ Supported image file extensions
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

# 🎯 Resize settings
# RESIZE_WIDTH = 500
# RESIZE_HEIGHT = 500

# 📊 Totals to accumulate sizes
total_original_size = 0
total_compressed_size = 0


def sizeof_mb(file_path):
    """Convert file size in bytes to megabytes (MB)."""
    return os.path.getsize(file_path) / (1024 * 1024)


def compress_and_convert_image(input_path, output_path):
    """🛠️ Resize image to 500x500, convert to lossless PNG, print size stats."""
    global total_original_size, total_compressed_size

    try:
        original_size = sizeof_mb(input_path)

        with Image.open(input_path) as img:
            img = img.convert("RGBA")  # 🖌️ Ensure compatible mode

            # 🔄 Resize forcibly to 500x500 ignoring aspect ratio
            # img = img.resize((RESIZE_WIDTH, RESIZE_HEIGHT), Image.LANCZOS)

            output_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Ensure output directory exists
            png_path = output_path.with_suffix(".png")

            # 💾 Save as PNG (lossless)
            img.save(png_path, "PNG", compress_level=3, optimize=True)

        compressed_size = sizeof_mb(png_path)

        total_original_size += original_size
        total_compressed_size += compressed_size

        saved = original_size - compressed_size
        saved_percent = (saved / original_size) * 100 if original_size > 0 else 0

        print(
            f"✅ {input_path.name}: "
            f"Original: {original_size:.2f} MB, "
            f"Compressed: {compressed_size:.2f} MB, "
            f"Saved: {saved:.2f} MB ({saved_percent:.1f}%)"
        )
    except Exception as e:
        print(f"❌ Failed to process {input_path}: {e}")


def process_folder(input_folder, output_folder):
    """🔄 Recursively process all images in the input folder."""
    for root, _, files in os.walk(input_folder):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in SUPPORTED_EXTENSIONS:
                rel_path = Path(root).relative_to(input_folder) / file
                input_path = Path(root) / file
                output_path = Path(output_folder) / rel_path
                compress_and_convert_image(input_path, output_path)


if __name__ == "__main__":
    print("🚀 Starting image resizing and PNG conversion (lossless)...")
    process_folder(INPUT_FOLDER, OUTPUT_FOLDER)

    total_saved = total_original_size - total_compressed_size
    saved_percent_total = (
        (total_saved / total_original_size) * 100 if total_original_size > 0 else 0
    )

    print("\n🎉 Processing complete!")
    print(f"📦 Total original size: {total_original_size:.2f} MB")
    print(f"📦 Total final size: {total_compressed_size:.2f} MB")
    print(f"💾 Total space saved: {total_saved:.2f} MB ({saved_percent_total:.1f}%)")
