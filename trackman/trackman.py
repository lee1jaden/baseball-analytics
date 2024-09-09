import csv

# Read and write a TrackMan CSV file.
with open('./trackman/data/example-trackman.csv', newline='') as readFile:
    reader = csv.DictReader(readFile)
    with open('./trackman/data/filtered-data.csv', 'w', newline='') as writeFile:
        fieldnames = ["Pitcher", "Batter"]
        writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            entry = {}
            for field in fieldnames:
                entry.update({field: row[field]})
            writer.writerow(entry)