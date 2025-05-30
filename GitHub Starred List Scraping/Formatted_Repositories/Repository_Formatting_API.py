"""
GitHub Starred Repositories Markdown Formatter

This script reads a Markdown file containing a list of GitHub repositories
(in a format like `- [repo_name](repo_url)`), fetches additional metadata
(description and star count) for each repository via the GitHub API, and
generates a new formatted Markdown file.

The output Markdown includes:
- Repository name as a header with a link
- An embed shortcode (for supported static site generators)
- The repository description
- Star count
- A call-to-action shortcode to visit and star the repo

Features:
- Uses GitHub API v3 to fetch repo details
- Supports optional GitHub API token to increase rate limits
- Handles API failures gracefully by providing fallback messages
- Preserves non-repository lines from the input file unchanged

Usage:
- Place your starred repo list in `All_Starred_Repository_List.md`
- (Optional) Set your GitHub API token in `GITHUB_TOKEN` for higher rate limits
- Run the script; it writes output to `Formatted_Starred_Repository_List.md`

Requirements:
- Python 3.x
- requests library (`pip install requests`)

Author: Madhurima Rawat
Date: 2025-05-30
"""

import requests
import re

# Input and output filenames
input_file = "All_Starred_Repository_List.md"
output_file = "Formatted_Starred_Repository_List.md"

# GitHub API token for higher rate limit (optional)
GITHUB_TOKEN = None  # Replace with your token string if available

# Headers for GitHub API requests
headers = {
    "Accept": "application/vnd.github.v3+json",
}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

rate_limit_exceeded = (
    False  # Global flag to prevent further API calls once rate limit is reached
)


def fetch_repo_data(repo_url):
    """
    Fetch metadata for a given GitHub repository URL using the GitHub API.

    Args:
        repo_url (str): Full URL to the GitHub repository

    Returns:
        dict: Contains repository 'name', 'url', 'description', and 'stars'
    """
    global rate_limit_exceeded  # Use the global flag

    # If rate limit already exceeded, skip API call
    if rate_limit_exceeded:
        return {
            "name": repo_url.split("https://github.com/")[-1],
            "url": repo_url,
            "description": "Skipped due to previous rate limit.",
            "stars": "N/A",
        }

    # Extract owner and repository name from the URL
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    # Make the GET request to GitHub API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "name": f"{owner}/{repo}",
            "url": repo_url,
            "description": data.get("description") or "No description provided.",
            "stars": data.get("stargazers_count", 0),
        }

    elif response.status_code == 403:
        # Check if it's due to rate limiting
        rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
        if rate_limit_remaining == "0":
            print("⚠️ GitHub API rate limit reached. Further requests will be skipped.")
            rate_limit_exceeded = True  # Set the flag
            return {
                "name": f"{owner}/{repo}",
                "url": repo_url,
                "description": "GitHub API rate limit reached. Skipping further fetches.",
                "stars": "N/A",
            }

        print(f"⚠️ Access forbidden for {repo_url}.")
    else:
        print(
            f"⚠️ Failed to fetch data for {repo_url} - Status code: {response.status_code}"
        )

    return {
        "name": f"{owner}/{repo}",
        "url": repo_url,
        "description": "Failed to fetch description.",
        "stars": "N/A",
    }


def process_markdown(md_lines):
    """
    Process input Markdown lines, detect repo links, fetch their data,
    and return formatted Markdown lines with embedded repo info.

    Args:
        md_lines (list): List of strings, each representing a line from input Markdown

    Returns:
        list: List of formatted Markdown lines with embedded repo metadata
    """
    output_lines = []

    # Regex to match lines with GitHub repo links in markdown list format
    repo_line_pattern = re.compile(r"- \[(.*?)\]\((https://github.com/[^)]+)\)")

    for line in md_lines:
        # Strip line to avoid whitespace issues in matching
        match = repo_line_pattern.match(line.strip())

        if match:
            # Extract repo display name and URL from the matched line
            repo_name = match.group(1)
            repo_url = match.group(2)

            # Fetch repo data from GitHub API
            repo_data = fetch_repo_data(repo_url)

            # Append formatted markdown with headers, embed shortcode, description, stars, and CTA
            output_lines.append(f"### [{repo_data['name']}]({repo_data['url']})")
            output_lines.append(f"{{% embed {repo_data['url']} %}}")
            output_lines.append("")
            output_lines.append(f"**📝 Description:** {repo_data['description']}")
            output_lines.append(f"> **🌟 Stars:** {repo_data['stars']}")
            output_lines.append("")
            output_lines.append(
                f"{{% cta {repo_data['url']} %}} 👀 Visit & star this repo! 💫 {{% endcta %}}"
            )
            output_lines.append("")  # Blank line after each repo block

        else:
            # Non-repo lines are copied as is (stripping trailing whitespace)
            output_lines.append(line.rstrip())

    return output_lines


def main():
    """
    Main function to read input Markdown, process it, and write formatted output Markdown.
    """
    # Read all lines from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        md_lines = f.readlines()

    # Process lines to fetch repo info and format output
    processed_lines = process_markdown(md_lines)

    # Write processed lines to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(processed_lines))

    print(f"Formatted markdown saved to {output_file}")


if __name__ == "__main__":
    main()
