#!/usr/bin/env python3

import os
from ftplib import FTP
from my_secrets import HOST, USERNAME, PASSWORD
import matplotlib.pyplot as plt
import pandas as pd

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
local_dir = "data/"
server_dir = "v3/2024/10/02/CSV"
ftp.cwd(server_dir)
csv_file = ftp.nlst()[0]
with open(local_dir + csv_file, 'w') as file:
    ftp.retrlines("RETR " + csv_file, lambda text : file.write(text + '\n'))
ftp.quit()

# Process the TrackMan CSV file and create reports.
df = pd.read_csv(local_dir + csv_file)
pitcher_ids = df[ID].unique()
            
for pid in pitcher_ids:

    # Record information for a given pitcher.
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
    filepath = f'./reports/{first_name}_{last_name}_{pid}'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    fig.savefig(f'{filepath}/pitch-arsenal-2.png')
