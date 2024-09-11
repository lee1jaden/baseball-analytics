import csv

pitchers = {}
pitchFields = { "Name": "Pitcher",
                "ThrowingHand": "PitcherThrows",
                "Set": "PitcherSet",
                "PitchType": "AutoPitchType",
                "Speed": "RelSpeed",
                "VerticalBreak": "InducedVertBreak",
                "HorizontalBreak": "HorzBreak"
                }

# Read and write a TrackMan CSV file.
with open('./trackman/data/example-trackman.csv', newline='') as readFile:
    reader = csv.DictReader(readFile)
    for row in reader:
        if not row["PitcherId"] in pitchers:
            pitchers.update({row["PitcherId"]: {"Name": row[pitchFields["Name"]], 
                                                "ThrowingHand": row[pitchFields["ThrowingHand"]], 
                                                "Pitches": []
                                                }})
        pitchers[row["PitcherId"]]["Pitches"].append({"Set": row[pitchFields["Set"]], 
                                                "PitchType": row[pitchFields["PitchType"]], 
                                                "Speed": row[pitchFields["Speed"]], 
                                                "VerticalBreak": row[pitchFields["VerticalBreak"]], 
                                                "HorizontalBreak": row[pitchFields["HorizontalBreak"]], 
                                                })
            
for pitcher in pitchers.values():
    # Make matplotlib chart of pitch profiles
    template = "{} threw {} pitches."
    print(template.format(pitcher["Name"], len(pitcher["Pitches"])))