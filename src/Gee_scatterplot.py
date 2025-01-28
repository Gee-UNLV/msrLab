import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from datetime import datetime
from collections import defaultdict

# define the csv file
csv_file = "data/rootbeer_authors_dates.csv"

# create nested dictionary to store data
file_data = defaultdict(lambda: defaultdict(list))

#initialize project start date
project_start_date = datetime(2015, 6, 19)

# parse the file and populate the file_data dictionary
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)  # read the csv file
    for row in reader:
        filename = row['Filename']
        author = row['Author']
        date = row['Date']

        # convert the date to a datetime object
        try:
            # parse date
            commit_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
            week_number = (commit_date - project_start_date).days // 7 # weeks since start of project
            file_data[filename][author].append(week_number)
        except Exception as e:
            print(f"Error processing")

# create variables for scatter plot
x_weeks = []
y_fileIndices = []
colors = []
authors = set()

# assign colors using color map
author_color_map = {}
dot_colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "gray", "olive", "cyan", "magenta", "yellow"]

# populate scatter plot
for file_index, (filename, author_data) in enumerate(file_data.items()):
    # loop over files
    for author, weeks in author_data.items():
        if author not in author_color_map:
            author_color_map[author] = dot_colors[len(author_color_map) % len(dot_colors)]

        # add data for scatter plot
        for week in weeks:
            x_weeks.append(week)                        # add the week to x-axis
            y_fileIndices.append(file_index)            # add the file index to y-axis
            colors.append(author_color_map[author])     # add the author's assigned color
        authors.add(author)                             # add the author to the set


# plot the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x_weeks, y_fileIndices, c=colors)
plt.xlabel("Week Since Project Start")
plt.ylabel("File Index")
plt.title("Scatter Plot of Commits")
plt.show()