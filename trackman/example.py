"""
import csv

# Read a TrackMan CSV file.
with open('./trackman/data/example-trackman.csv', newline='') as readFile:
    reader = csv.DictReader(readFile)

    for row in reader:
        print(row['PitchNo'])

# Write a TrackMan CSV file.
with open('./trackman/data/fake-data.csv', 'w', newline='') as writeFile:
    fieldnames = ["Pitcher", "Batter"]
    writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
    writer.writeheader()

    entry = {}
    for field in fieldnames:
        entry.update({field: "Lee, Jaden"})
    writer.writerow(entry)
"""
# ---------------------------------------------------------------------------

import matplotlib.pyplot as plt

# Tutorial: https://matplotlib.org/stable/tutorials/pyplot.html
# Plot some data with pitches per plate appearance grouped by inning
plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()