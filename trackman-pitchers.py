#!/usr/bin/env python3

# Title: trackman.py
# Author: Jaden Lee
# Created Date: September 8, 2024
# Description: This folder is specifically for analyzing TrackMan data for pitchers. 

import os
from ftplib import FTP
from my_secrets import HOST, USERNAME, PASSWORD
import csv
import matplotlib.pyplot as plt
import numpy as np


class Pitcher:
    def __init__(self, id, name, throwingHand):
        self.id = id
        self.name = name
        self.throwingHand = throwingHand
        self.pitches = []
    
    def __str__(self):
        return f'{self.name.split(", ")[1].upper()} {self.name.split(", ")[0].upper()} ({self.throwingHand[0]})'


class Pitch:
    def __init__(self, set, pitchType, speed, verticalBreak, horizontalBreak):
        self.set = set
        self.pitchType = pitchType
        self.speed = speed
        self.verticalBreak = verticalBreak
        self.horizontalBreak = horizontalBreak
    
    def __str__(self):
        return f"{self.pitchType}"


ID = "PitcherId"
NAME = "Pitcher"
THROWING_HAND = "PitcherThrows"
SET = "PitcherSet"
PITCH_TYPE = "TaggedPitchType"
VELO = "RelSpeed"
VERTICAL_BREAK = "InducedVertBreak"
HORIZONTAL_BREAK = "HorzBreak"

ftp = FTP(HOST, USERNAME, PASSWORD)

local_dir = "data/"
server_dir = "v3/2024/10/02/CSV"
ftp.cwd(server_dir)
csv_file = ftp.nlst()[0]

with open(local_dir + csv_file, 'w') as file:
    ftp.retrlines("RETR " + csv_file, lambda text : file.write(text + '\n'))

ftp.quit()

# Read and write a TrackMan CSV file.
pitchers = set()
with open(local_dir + csv_file, newline='') as readFile:
    reader = csv.DictReader(readFile)
    for row in reader:
        try:
            pitcher = [p for p in pitchers if p.id == row[ID]][0]
        except:
            pitchers.add(Pitcher(row[ID], 
                                    row[NAME], 
                                    row[THROWING_HAND]))
            pitcher = [p for p in pitchers if p.id == row[ID]][0]
        finally:
            pitcher.pitches.append(Pitch(row[SET], 
                                    row[PITCH_TYPE], 
                                    float(row[VELO]), 
                                    float(row[VERTICAL_BREAK]), 
                                    float(row[HORIZONTAL_BREAK])))
            
# Make matplotlib chart of pitch profiles

for pitcher in pitchers:
    pitchTypes = set(map(lambda p: p.pitchType, pitcher.pitches))

    fig, ax = plt.subplots()
    fig.suptitle("Pitch Arsenal Chart (Pitcher's Viewpoint)")
    ax.set_title(f'{pitcher} - {len(pitcher.pitches)} Pitches')
    ax.set_xlabel('Horizontal Break (in)')
    ax.set_ylabel('Induced Vertical Break (in)')
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.grid(True)

    colors = ["bo", "go", "ro", "co", "mo", "yo"]
    colorIndex = 0
    for pt in pitchTypes:
        horizBreaks = [p.horizontalBreak for p in pitcher.pitches if p.pitchType == pt]
        vertBreaks = [p.verticalBreak for p in pitcher.pitches if p.pitchType == pt]
        avgSpeed = np.mean([p.speed for p in pitcher.pitches if p.pitchType == pt]).round(1)
        ax.plot(horizBreaks, vertBreaks, colors[colorIndex], label=f'{pt} ({avgSpeed} mph)')
        colorIndex += 1
    
    ax.legend()
    filepath = './profiles/{}_{}_{}'.format(f'{pitcher}'.split()[0], f'{pitcher}'.split()[1], pitcher.id)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    fig.savefig(f'{filepath}/pitch-arsenal.png')