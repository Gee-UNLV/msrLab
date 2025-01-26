import json
import requests
import csv
import os

# Languages for source files
LANGUAGE_EXTENSIONS = {
    "Python": [".py"],
    "JavaScript": [".js", ".jsx"],
    "Java": [".java"],
    "C++": [".cpp", ".hpp", ".cc", ".h"],
    "C": [".c", ".h"],
    "Ruby": [".rb"],
    "Go": [".go"],
    "PHP": [".php"],
    "Swift": [".swift"],
    "Kotlin": [".kt", ".kts"],
}
# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

# Function to check if a file is a source file
def is_source_file(filename):
    for extensions in LANGUAGE_EXTENSIONS.values():
        if any(filename.endswith(ext) for ext in extensions):
            return True
    return False

# Function to collect authors and dates for each source file
def collect_authors_dates(lsttokens, repo):
    authors_dates = {}  # Dictionary to store file info: {filename: [(author, date), ...]}
    ipage = 1  # URL page counter
    ct = 0  # Token counter

    try:
        # Loop through all commit pages
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # Break if no commits on this page
            if not jsonCommits:
                break

            # Process each commit
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # Get commit details
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                # Extract commit metadata
                commit_author = shaDetails.get("commit", {}).get("author", {}).get("name", "Unknown")
                commit_date = shaDetails.get("commit", {}).get("author", {}).get("date", "Unknown")
                filesjson = shaDetails.get('files', [])

                # Process only source files
                for fileObj in filesjson:
                    filename = fileObj['filename']
                    if is_source_file(filename):
                        # Add author and date info for this file
                        if filename not in authors_dates:
                            authors_dates[filename] = []
                        authors_dates[filename].append((commit_author, commit_date))

            ipage += 1
    except Exception as e:
        print("Error receiving data:", e)

    return authors_dates

# GitHub repository
repo = 'scottyab/rootbeer'

# Authentication tokens
lstTokens = ["123"]

# Collect authors and dates
authors_dates = collect_authors_dates(lstTokens, repo)

# Output to a CSV file
if not os.path.exists("data"):
    os.makedirs("data")
output_file = f"data/{repo.split('/')[1]}_authors_dates.csv"

with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Author", "Date"])

    # Write authors and dates to the CSV
    for filename, records in authors_dates.items():
        for author, date in records:
            writer.writerow([filename, author, date])

print(f"Authors and dates collected successfully. Output saved to {output_file}.")
