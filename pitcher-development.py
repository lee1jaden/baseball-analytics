#!/usr/bin/env python3

import os
from ftplib import FTP
from my_secrets import HOST, USERNAME, PASSWORD, SERVER_DIRECTORY
import matplotlib.pyplot as plt
import pandas as pd

# Create file storage locations for data and reports
data_dir = "./data"
report_dir = "./reports"

# Create macros for the fields of a TrackMan CSV file
ID = "PitcherId"
NAME = "Pitcher"
THROWING_HAND = "PitcherThrows"
SET = "PitcherSet"
PITCH_TYPE = "TaggedPitchType"
VELOCITY = "RelSpeed"
VERTICAL_BREAK = "InducedVertBreak"
HORIZONTAL_BREAK = "HorzBreak"

# Copy TrackMan data from the FTP server
ftp = FTP(HOST, USERNAME, PASSWORD)
ftp.cwd(SERVER_DIRECTORY)
trackman_file = ftp.nlst()[0]
os.makedirs(data_dir, exist_ok=True)
with open(f"{data_dir}/{trackman_file}", 'w') as file:
    ftp.retrlines("RETR " + trackman_file, lambda text : file.write(text + '\n'))
ftp.quit()

# Process the TrackMan CSV file and create reports
df = pd.read_csv(f"{data_dir}/{trackman_file}")
pitcher_ids = df[ID].unique()
            
for pid in pitcher_ids:

    # Record information for a given pitcher
    pitcher_df = df.loc[df[ID] == pid]
    name = pitcher_df[NAME].unique()[0]
    last_name = name.split(", ")[0]
    first_name = name.split(", ")[1]
    throwing_hand = pitcher_df[THROWING_HAND].unique()[0]
    pitch_types = pitcher_df[PITCH_TYPE].unique()

    # Make matplotlib chart of pitch profiles.
    fig, ax = plt.subplots()
    fig.suptitle("Pitch Arsenal Chart (Pitcher's Viewpoint)")
    ax.set_title(f'{first_name} {last_name} ({throwing_hand[0]}) - {len(pitcher_df)} Pitches')
    ax.set_xlabel('Induced Horizontal Break (in)')
    ax.set_ylabel('Induced Vertical Break (in)')
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.grid(True)

    colors = ["bo", "go", "ro", "co", "mo", "yo"]
    colorIndex = 0
    for pt in pitch_types:
        pitch_type_df = pitcher_df.loc[pitcher_df[PITCH_TYPE] == pt]
        avg_velo = pitch_type_df[VELOCITY].mean().round(1)
        ax.plot(pitch_type_df[HORIZONTAL_BREAK], pitch_type_df[VERTICAL_BREAK], colors[colorIndex], label=f'{pt} ({avg_velo} mph)')
        colorIndex += 1
    
    ax.legend()
    filepath = f'{report_dir}/{first_name}_{last_name}'
    os.makedirs(filepath, exist_ok=True)
    fig.savefig(f'{filepath}/pitch-arsenal.png')

os.remove(f"{data_dir}/{trackman_file}")
os.rmdir(data_dir)