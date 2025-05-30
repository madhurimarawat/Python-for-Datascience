"""
GitHub Starred Lists Scraper
Author: Madhurima Rawat

This script fetches all starred repository lists for the given GitHub user,
then fetches all repositories inside each list and generates a Markdown summary.
"""

import requests
from bs4 import BeautifulSoup

USERNAME = "madhurimarawat"
BASE_URL = (
    f"https://github.com/{USERNAME}?tab=stars"  # URL for the user's starred lists page
)
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Headers to mimic a browser request


def fetch_star_lists(url):
    """
    Fetch all custom starred lists from the GitHub stars page.

    Args:
        url (str): The URL of the GitHub stars tab page.

    Returns:
        list of dict: Each dict contains title, description, count, url, and slug of a starred list.
    """
    response = requests.get(url, headers=HEADERS)  # Send GET request to the URL
    if response.status_code != 200:
        print(
            f"❌ Failed to fetch star list page (Status code: {response.status_code})"
        )
        return []

    # Parse HTML content of the response
    soup = BeautifulSoup(response.text, "html.parser")

    # Select all the starred lists; each list is represented as a card (an anchor tag with specific classes)
    list_cards = soup.select("a.d-block.Box-row")

    star_lists = []
    for card in list_cards:
        href = card.get("href")  # URL path for the starred list
        title = card.select_one("h3").text.strip()  # Title of the starred list
        desc = card.select_one(
            "span.Truncate-text"
        ).text.strip()  # Description of the list
        repo_count = card.select_one(
            "div.color-fg-muted"
        ).text.strip()  # Number of repos in list
        full_url = f"https://github.com{href}"  # Full URL of the starred list page
        slug = href.split("/")[-1]  # Extract the list slug from URL path

        # Append the list info as a dictionary to star_lists
        star_lists.append(
            {
                "title": title,
                "description": desc,
                "count": repo_count,
                "url": full_url,
                "slug": slug,
            }
        )

    return star_lists


def get_repositories_from_list(url):
    """
    Fetch all repositories in a given starred list page.

    Args:
        url (str): URL of the starred list.

    Returns:
        list of tuples: Each tuple contains (repository name, repository URL).
    """
    response = requests.get(url, headers=HEADERS)  # Request the starred list page
    if response.status_code != 200:
        print(
            f"❌ Failed to fetch list page: {url} (Status code: {response.status_code})"
        )
        return []

    # Parse HTML content of the list page
    soup = BeautifulSoup(response.text, "html.parser")

    # Select all repository links inside the starred list (repo names are inside h3 > a)
    repo_elements = soup.select("div#user-list-repositories h3 a")

    repos = []
    for repo in repo_elements:
        # Clean repo name text and remove whitespace/newlines
        name = repo.get_text(strip=True).replace("\n", "").replace(" ", "")
        href = repo["href"]  # Relative link to the repo
        # Append tuple of (name, full repo URL)
        repos.append((name, f"https://github.com{href}"))

    return repos


def generate_markdown(all_lists, filename="All_Starred_Repository_List.md"):
    """
    Generate a markdown file summarizing all starred lists and their repositories.

    Args:
        all_lists (list): List of starred list metadata.
        filename (str): Output markdown filename.
    """
    with open(filename, "w", encoding="utf-8") as f:
        # Write main heading with username
        f.write(f"# 🌟 GitHub Starred Repository Lists for @{USERNAME}\n\n")

        for lst in all_lists:
            # Write each starred list's title, description, repo count, and link
            f.write(f"## {lst['title']}\n")
            f.write(f"**{lst['description']}**  \n")
            f.write(f"*{lst['count']}*  \n")
            f.write(f"[View on GitHub]({lst['url']})\n\n")

            # Get repos inside the starred list
            repos = get_repositories_from_list(lst["url"])
            if not repos:
                f.write("_No repositories found._\n\n")
                continue

            # Write each repository as a markdown list item
            for name, link in repos:
                f.write(f"- [{name}]({link})\n")
            f.write("\n---\n\n")  # Separator between lists
    print(f"✅ Markdown file created: {filename}")


if __name__ == "__main__":
    print(f"🔍 Fetching lists from {BASE_URL}")
    star_lists = fetch_star_lists(BASE_URL)  # Fetch all starred lists

    if not star_lists:
        print("⚠️ No star lists found.")
    else:
        print(f"✅ Found {len(star_lists)} lists.")
        generate_markdown(star_lists)  # Generate markdown summary file
