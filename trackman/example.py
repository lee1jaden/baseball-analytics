#!/usr/bin/env python3

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

"""
import matplotlib.pyplot as plt

# Plot some data and make it look nice.
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], "ro", label="Fastball")
plt.plot([1, 2, 3, 4], [0, 0, 0, 0], "bo", label="Slider")
plt.axis((-20, 20, -20, 20))
plt.legend()
plt.title('example plot')
plt.xlabel('assigned by matplotlib')
plt.ylabel('some numbers')
plt.grid(True)
plt.savefig('plot.png')
"""