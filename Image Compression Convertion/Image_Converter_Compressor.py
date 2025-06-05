"""
Batch Image Resizer and WebP Converter (Lossless)
--------------------------------------------------

This script recursively scans an input folder for supported image formats
(.jpg, .jpeg, .png, .bmp, .tiff), resizes them to fixed dimensions (500x500),
and converts each image to a **lossless WebP** format. The output images are
saved in a separate directory, preserving the folder structure.

Key Features:
- Forcefully resizes all images to 500x500 using high-quality LANCZOS filtering.
- Converts images to WebP format with **lossless compression**.
- Calculates and displays individual and total size statistics for comparison.
- Automatically creates necessary output subdirectories.

Usage:
- Set `INPUT_FOLDER` and `OUTPUT_FOLDER` paths to your desired source and destination.
- Run the script using: `python Image_Converter_Compressor.py`

Dependencies:
- Pillow (Python Imaging Library fork) for image processing.

Note:
- WebP format is widely supported in browsers but may not render in some contexts
  like older email clients or certain metadata applications.

"""

# Author: Madhurima Rawat
# Date: June 5, 2025
# GitHub: https://github.com/madhurimarawat

# Importing Libraries
import os
from PIL import Image
from pathlib import Path

# 📁 Define your input and output folders here
INPUT_FOLDER = "assets"  # 🔍 Folder with original images
OUTPUT_FOLDER = "output_folder_assets"  # 💾 Folder to save processed images

# 🖼️ Supported image file extensions
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

# 🎯 Resize settings
RESIZE_WIDTH = 500
RESIZE_HEIGHT = 500

# 📊 Totals to accumulate sizes
total_original_size = 0
total_compressed_size = 0


def sizeof_mb(file_path):
    """Convert file size in bytes to megabytes (MB)."""
    return os.path.getsize(file_path) / (1024 * 1024)


def compress_and_convert_image(input_path, output_path):
    """🛠️ Resize image to 100x100, convert to lossless WebP, print size stats."""
    global total_original_size, total_compressed_size

    try:
        original_size = sizeof_mb(input_path)

        with Image.open(input_path) as img:
            img = img.convert("RGBA")  # 🖌️ Ensure compatible mode

            # 🔄 Resize forcibly to 100x100 ignoring aspect ratio
            img = img.resize((RESIZE_WIDTH, RESIZE_HEIGHT), Image.LANCZOS)

            output_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Ensure output directory exists
            webp_path = output_path.with_suffix(".webp")

            # 💎 Save as lossless WebP
            img.save(webp_path, "webp", lossless=True)

        compressed_size = sizeof_mb(webp_path)

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
    print("🚀 Starting image resizing and conversion (lossless)...")
    process_folder(INPUT_FOLDER, OUTPUT_FOLDER)

    total_saved = total_original_size - total_compressed_size
    saved_percent_total = (
        (total_saved / total_original_size) * 100 if total_original_size > 0 else 0
    )

    print("\n🎉 Processing complete!")
    print(f"📦 Total original size: {total_original_size:.2f} MB")
    print(f"📦 Total final size: {total_compressed_size:.2f} MB")
    print(f"💾 Total space saved: {total_saved:.2f} MB ({saved_percent_total:.1f}%)")
