"""
Shields_Io_Badges_Addition.py

Author: Madhurima Rawat
Description:
This script processes a Markdown file containing GitHub repository listings with custom Liquid-style tags and headings.
It performs the following conversions:
- {% embed URL %} → Plain Markdown link
- {% cta URL %} ... {% endcta %} → Centered call-to-action badge (Shields IO Badge Conversion)
- Converts ## and ### headings to centered HTML-wrapped sections
- Generates a collapsible Table of Contents from all ## headings

The final Markdown is suitable for GitHub README or documentation pages.
"""

# Importing Regular Expression
import re


def slugify(text):
    """
    Convert a heading string to a URL-friendly slug used as an anchor ID.
    Example: "My Section Title" → "my-section-title"
    """
    return re.sub(r"[^\w\- ]+", "", text).strip().lower().replace(" ", "-")


def convert_embed_and_cta(md_text):
    """
    Convert custom Liquid-style tags in the Markdown content to GitHub-compatible Markdown:
    - {% embed URL %} → Markdown link
    - {% cta URL %} ... {% endcta %} → Centered badge
    - ## and ### headings → Center-aligned with optional section IDs
    - Builds a Table of Contents from ## headings
    """
    toc = []  # Stores lines for the Table of Contents

    # ───────────────────────────────────────────────
    # Convert {% embed https://github.com/... %} → Markdown link
    md_text = re.sub(
        r"{% embed (https://github\.com/[\w\-/]+) %}",
        r"[🔗 Visit Repository](\1)",
        md_text,
    )

    # ───────────────────────────────────────────────
    # Convert {% cta URL %} ... {% endcta %} → Centered, larger badge
    md_text = re.sub(
        r"{% cta (https://github\.com/[\w\-/]+) %}.*?{% endcta %}",
        r'<div align="center">\n\n<a href="\1">\n<img src="https://img.shields.io/badge/👀%20Visit%20&%20Star%20this%20repo-💫-6a5acd?style=flat&labelColor=ffd700" height="35">\n</a>\n\n</div>\n\n',
        md_text,
        flags=re.DOTALL,
    )

    # ───────────────────────────────────────────────
    # Process ## and ### headings
    def handle_heading(match):
        hashes = match.group(1)  # ## or ###
        text = match.group(2).strip()

        if hashes == "##":
            anchor = slugify(text)
            toc.append(f"- [{text}](#{anchor})")  # Add plain text ToC entry
            return f'<section id="{anchor}">\n<div align="center">\n\n{hashes} {text}\n\n</div>\n</section>\n'
        else:
            # For ### headings: just center-align, no section tag
            return f'<div align="center">\n\n{hashes} {text}\n\n</div>\n'

    # Apply heading transformation across the document
    md_text = re.sub(r"^(#{2,3}) (.+)$", handle_heading, md_text, flags=re.MULTILINE)

    # ───────────────────────────────────────────────
    # Insert Table of Contents at the top (if any headings found)
    if toc:
        toc_md = (
            "<details open>\n"
            "<summary><strong>📌 Table of Contents</strong></summary>\n\n"
            + "\n".join(toc)
            + "\n\n</details>\n\n"
        )
        md_text = toc_md + md_text

    return md_text


def main():
    """
    Main execution function:
    - Reads input markdown
    - Converts embed, CTA, headings, and builds ToC
    - Saves output markdown
    """
    input_file = r"Formatted_Repositories\Formatted_Starred_Repository_List.md"
    output_file = "Formatted_Starred_Repository_List.md"

    # Read the original Markdown content
    with open(input_file, "r", encoding="utf-8") as f:
        original_md = f.read()

    # Convert to final Markdown format
    converted_md = convert_embed_and_cta(original_md)

    # Write the updated Markdown content to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(converted_md)

    print(f"✅ Conversion complete! Output saved to: {output_file}")


if __name__ == "__main__":
    main()
