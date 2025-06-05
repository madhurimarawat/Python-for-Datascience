"""
Screenshot Batch Converter to High-Quality WebP
------------------------------------------------

This script recursively scans the specified folder for supported image formats
(.jpg, .jpeg, .png, .bmp, .tiff), and converts each to **WebP format** using
lossless compression or optionally very light lossy compression. It maintains
the original resolution and folder structure.

Key Features:
- Converts screenshots or other images to `.webp` while preserving dimensions.
- Uses **true lossless WebP** by default for maximum quality retention.
- Optional alternative: light lossy compression (`quality=90`) for better compatibility.
- Prints detailed size stats per file and overall space savings.
- Automatically creates subdirectories in the output folder as needed.

Usage:
- Set `INPUT_FOLDER` and `OUTPUT_FOLDER` at the top.
- Run with `python Image_Converter.py` to start conversion.

Dependencies:
- Python Imaging Library (Pillow fork) for image handling.

Note:
- WebP offers better compression ratios with high visual fidelity.
- Lossless WebP is supported by modern browsers, but ensure compatibility
  if targeting older environments.

"""

# Author: Madhurima Rawat
# Date: June 5, 2025
# GitHub: https://github.com/madhurimarawat


# Importing Libraries
import os
from PIL import Image
from pathlib import Path

# 📁 Input and output folders
INPUT_FOLDER = "assets"
OUTPUT_FOLDER = "output_folder_assets_ss_png"

# 🖼️ Supported image extensions
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

# 📊 Size counters
total_original_size = 0
total_converted_size = 0


def sizeof_mb(file_path):
    """Return file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)


def convert_image_lossless(input_path, output_path):
    """Convert to WebP (lossless or light lossy), preserving dimensions."""
    global total_original_size, total_converted_size

    try:
        original_size = sizeof_mb(input_path)

        with Image.open(input_path) as img:
            img = img.convert("RGBA")  # Ensure compatibility

            output_path.parent.mkdir(parents=True, exist_ok=True)
            webp_path = output_path.with_suffix(".webp")

            # 💎 Convert to WebP with minimal compression
            # Choose one:
            # ▶️ Option A: True lossless
            img.save(webp_path, "webp", lossless=True)

            # ▶️ Option B: Very light compression (better compatibility)
            # img.save(webp_path, "webp", quality=90, method=6)  # 90 = very high quality

        converted_size = sizeof_mb(webp_path)

        total_original_size += original_size
        total_converted_size += converted_size

        saved = original_size - converted_size
        saved_percent = (saved / original_size) * 100 if original_size > 0 else 0

        print(
            f"✅ {input_path.name}: "
            f"Original: {original_size:.2f} MB, "
            f"Converted: {converted_size:.2f} MB, "
            f"Saved: {saved:.2f} MB ({saved_percent:.1f}%)"
        )
    except Exception as e:
        print(f"❌ Failed to process {input_path}: {e}")


def process_folder(input_folder, output_folder):
    """Walk through and process all images."""
    for root, _, files in os.walk(input_folder):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in SUPPORTED_EXTENSIONS:
                rel_path = Path(root).relative_to(input_folder) / file
                input_path = Path(root) / file
                output_path = Path(output_folder) / rel_path
                convert_image_lossless(input_path, output_path)


if __name__ == "__main__":
    print("🚀 Starting conversion (high quality WebP, no resize)...")
    process_folder(INPUT_FOLDER, OUTPUT_FOLDER)

    total_saved = total_original_size - total_converted_size
    saved_percent_total = (
        (total_saved / total_original_size) * 100 if total_original_size > 0 else 0
    )

    print("\n🎉 Conversion complete!")
    print(f"📦 Total original size: {total_original_size:.2f} MB")
    print(f"📦 Total converted size: {total_converted_size:.2f} MB")
    print(f"💾 Total space saved: {total_saved:.2f} MB ({saved_percent_total:.1f}%)")
