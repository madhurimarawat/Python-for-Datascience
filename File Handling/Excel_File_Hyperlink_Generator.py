"""
Module: hyperlink_extractor

This module provides functionality to extract embedded hyperlinks from
Excel files (.xlsx), categorize them based on keywords, and save the categorized
links into Markdown files.

Main Function:
--------------
extract_hyperlinks_by_category(file_path)

Usage:
------
Provide the path to an Excel (.xlsx) file. The function will:
    1. Parse the internal XML structure of the Excel file.
    2. Extract hyperlinks from worksheet files and their relationships.
    3. Categorize hyperlinks based on keywords.
    4. Write categorized links to Markdown files.

Requirements:
-------------
- lxml
- zipfile
- os
"""

import zipfile
from lxml import etree
import os


def extract_hyperlinks_by_category(file_path):
    """
    Extracts embedded hyperlinks from an Excel file (.xlsx), categorizes them
    by predefined keywords, and saves them into Markdown files.

    Args:
        file_path (str): The path to the Excel (.xlsx) file.
    """

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with zipfile.ZipFile(file_path, "r") as zip_archive:
        all_hyperlinks = []

        # Iterate through worksheet files inside the archive
        for sheet_filename in zip_archive.namelist():
            if sheet_filename.startswith(
                "xl/worksheets/sheet"
            ) and sheet_filename.endswith(".xml"):
                print(f"\n📄 Processing worksheet XML: {sheet_filename}")

                with zip_archive.open(sheet_filename) as sheet_file:
                    sheet_xml_content = sheet_file.read()
                    sheet_tree = etree.fromstring(sheet_xml_content)

                    # Find hyperlinks inside the worksheet XML
                    hyperlink_elements = sheet_tree.findall(
                        ".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}hyperlink"
                    )

                    if not hyperlink_elements:
                        continue

                    # Relationship file for the sheet (contains actual URLs)
                    rels_filename = (
                        sheet_filename.replace("worksheets/", "worksheets/_rels/")
                        + ".rels"
                    )
                    rels_mapping = {}

                    if rels_filename in zip_archive.namelist():
                        with zip_archive.open(rels_filename) as rels_file:
                            rels_xml_content = rels_file.read()
                            rels_tree = etree.fromstring(rels_xml_content)

                            # Build mapping of Relationship IDs to URLs
                            for rel in rels_tree.findall(
                                ".//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"
                            ):
                                r_id = rel.get("Id")
                                target_url = rel.get("Target")
                                rels_mapping[r_id] = target_url

                    # Collect hyperlink info from this sheet
                    for hyperlink in hyperlink_elements:
                        cell_ref = hyperlink.get("ref")
                        r_id = hyperlink.get(
                            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
                        )
                        target_url = rels_mapping.get(r_id, "Unknown")

                        all_hyperlinks.append(
                            {
                                "sheet": sheet_filename,
                                "cell": cell_ref,
                                "url": target_url,
                            }
                        )

        if not all_hyperlinks:
            print("⚠️ No embedded hyperlinks found.")
            return

        # Categorize links by keywords
        category_data_warehouse = []
        category_cloud_computing = []

        for link_info in all_hyperlinks:
            url_lower = link_info["url"].lower()

            # Keywords to categorize links (customize as needed)
            data_warehouse_keywords = [
                "data-warehouse",
                "etl",
                "olap",
                "snowflake",
                "star-schema",
                "fact-constellation",
                "granularity",
                "data-transformation",
                "data-loading",
            ]
            cloud_computing_keywords = [
                "cloud",
                "virtualization",
                "hypervisor",
                "migration",
                "cdn",
                "sdn",
                "cloud-security",
                "cloud-storage",
                "identity",
                "compliance",
            ]

            if any(keyword in url_lower for keyword in data_warehouse_keywords):
                category_data_warehouse.append(link_info)
            elif any(keyword in url_lower for keyword in cloud_computing_keywords):
                category_cloud_computing.append(link_info)
            else:
                # Default category if no keyword matches
                category_data_warehouse.append(link_info)

        # Save categorized links to markdown files
        output_links_to_markdown(
            filename="data_warehouse_links.md",
            title="Data Warehouse Links",
            links=category_data_warehouse,
        )

        output_links_to_markdown(
            filename="cloud_computing_links.md",
            title="Cloud Computing Links",
            links=category_cloud_computing,
        )


def output_links_to_markdown(filename, title, links):
    """
    Writes a list of hyperlinks to a Markdown file.

    Args:
        filename (str): The name of the output Markdown file.
        title (str): The heading/title to write at the top of the file.
        links (list): A list of dictionaries with hyperlink data.
    """
    if not links:
        print(f"⚠️ No links to write for {title}. Skipping file creation.")
        return

    with open(filename, "w", encoding="utf-8") as md_file:
        md_file.write(f"# {title}\n\n")
        for link in links:
            md_file.write(f"- [{link['url']}]({link['url']})\n")

    print(f"✅ Saved: {filename}")


# Example usage
if __name__ == "__main__":
    excel_file_path = "Excel_File.xlsx"  # Replace with your Excel file path
    extract_hyperlinks_by_category(excel_file_path)
