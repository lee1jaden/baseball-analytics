#!/usr/bin/env python3

import os
import io
from ftplib import FTP
from my_secrets import HOST, USERNAME, PASSWORD
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

# Create file storage locations for data and reports
data_dir = "./data"
report_dir = "./reports"
# The date must be in YYYY/MM/DD format
date = "2024/10/02"
date_dashed = date.replace('/', '-')
server_dir = f"v3/{date}/CSV/"

# Create macros for the fields of a TrackMan CSV file
ID = "PitcherId"
NAME = "Pitcher"
THROWING_HAND = "PitcherThrows"
SET = "PitcherSet"
PITCH_TYPE = "TaggedPitchType"
VELOCITY = "RelSpeed"
VERTICAL_BREAK = "InducedVertBreak"
HORIZONTAL_BREAK = "HorzBreak"
SPIN_RATE = "SpinRate"
SPIN_AXIS = "SpinAxis"
VERITCAL_APPROACH = "VertApprAngle"
HORIZONTAL_POSITION = "PlateLocSide"
VERTICAL_POSITION = "PlateLocHeight"
RELEASE_HEIGHT = "RelHeight"
RELEASE_SIDE = "RelSide"
EXTENSION = "Extension"

# Copy TrackMan data from the FTP server
ftp = FTP(HOST, USERNAME, PASSWORD)
ftp.cwd(server_dir)
trackman_file = ftp.nlst()[0]
os.makedirs(data_dir, exist_ok=True)
with open(f"{data_dir}/{trackman_file}", 'w') as file:
    ftp.retrlines("RETR " + trackman_file, lambda text : file.write(text + '\n'))
ftp.quit()

# Create canvas for the PDF report
pdf = canvas.Canvas(f"{report_dir}/{date_dashed}-pitching.pdf", pageSize=letter)
pdf_width, pdf_height = letter

def plotToPDF(figure, x, y, width, height):
    plotImg = io.BytesIO()
    figure.savefig(plotImg, format='png')
    plotImg.seek(0)
    image = ImageReader(plotImg)
    pdf.drawImage(image, x, y, width, height)

# Begin processing the TrackMan CSV file
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
    os.makedirs(report_dir, exist_ok=True)

    # Set up pitch arsenal chart
    fig1, arsenal = plt.subplots()
    fig1.suptitle(f'{first_name} {last_name} ({throwing_hand[0]}) - {len(pitcher_df)} Pitches')
    arsenal.set_title('Pitch Arsenal')
    arsenal.set_xlabel('Induced Horizontal Break (in)')
    arsenal.set_ylabel('Induced Vertical Break (in)')
    arsenal.set_xlim(-25, 25)
    arsenal.set_ylim(-25, 25)
    arsenal.grid(True)

    # Set up pitch location chart
    fig2, locations = plt.subplots()
    fig2.suptitle(f'{first_name} {last_name} ({throwing_hand[0]}) - {len(pitcher_df)} Pitches')
    locations.set_title('Pitch Locations')
    locations.set_xlabel('Horizontal Location (ft)')
    locations.set_ylabel('Vertical Location (ft)')
    locations.set_xlim(-4, 4)
    locations.set_ylim(-1, 7)
    locations.grid(True)
    rect = patches.Rectangle((-8.5/12.0, 1.5), 17.0/12.0, 2.5, linewidth=2, edgecolor='none', facecolor='0.75')
    locations.add_patch(rect)

    # Set up pitch release point chart
    fig3, release = plt.subplots()
    fig2.suptitle(f'{first_name} {last_name} ({throwing_hand[0]}) - {len(pitcher_df)} Pitches')
    release.set_title('Pitch Release Points')
    release.set_xlabel('Release Side (ft)')
    release.set_ylabel('Release Height (ft)')
    release.set_xlim(-3, 3)
    release.set_ylim(2, 8)
    release.grid(True)

    colors = ["b", "g", "r", "c", "m", "y"]
    colorIndex = 0
    for pt in pitch_types:
        pitch_type_df = pitcher_df.loc[pitcher_df[PITCH_TYPE] == pt]
        velo_avg = pitch_type_df[VELOCITY].mean().round(1)
        velo_std = pitch_type_df[VELOCITY].std().round(2)
        spinrate_avg = pitch_type_df[SPIN_RATE].mean().round()
        spinrate_std = pitch_type_df[SPIN_RATE].std().round(1)
        spinaxis_avg = pitch_type_df[SPIN_AXIS].mean().round()
        spinaxis_std = pitch_type_df[SPIN_AXIS].std().round(1)
        approach_avg = pitch_type_df[VERITCAL_APPROACH].mean().round(1)
        approach_std = pitch_type_df[VERITCAL_APPROACH].std().round(2)
        extension_avg = pitch_type_df[EXTENSION].mean().round(2)
        extension_std = pitch_type_df[EXTENSION].std().round(3)
        arsenal.plot(pitch_type_df[HORIZONTAL_BREAK], pitch_type_df[VERTICAL_BREAK], f"{colors[colorIndex]}o", label=f'{pt} ({spinrate_avg} rpm)')
        # Try to classify by strikes and balls and improve strike zone position. Switch to scatter. Add text labels for pitchNo
        locations.plot(pitch_type_df[HORIZONTAL_POSITION], pitch_type_df[VERTICAL_POSITION], f"{colors[colorIndex]}o", label=f'{pt} ({velo_avg} mph)')
        release.plot(pitch_type_df[RELEASE_SIDE], pitch_type_df[RELEASE_HEIGHT], f"{colors[colorIndex]}o", label=f'{pt} ({extension_avg} ft ext)')
        colorIndex += 1
    
    arsenal.legend()
    locations.legend()
    release.legend()

    for index, fig in [(n, plt.figure(n)) for n in plt.get_fignums()]:  
        plotToPDF(fig, 1*inch, 1 + 3*index*inch, 2*inch, 2*inch)
        plt.close(fig)
    pdf.showPage()

pdf.save()
os.remove(f"{data_dir}/{trackman_file}")
os.rmdir(data_dir)

