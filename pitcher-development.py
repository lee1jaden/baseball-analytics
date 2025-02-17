#!/usr/bin/env python3

import os
import io
from my_secrets import ADDRESS
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from tags import *

DATA_FILEPATH = "./data/UTA_UTE_scrimmages.txt"
REPORT_DIR = "./reports/development"
pdf_width, pdf_height = letter
colors = ["b", "g", "r", "c", "m", "y"]


def main():
    """
    Generate reports for each of the games in the file at the path given by the macro.
    """
    with open(DATA_FILEPATH, "r") as games_file:
        for file in games_file:
            filepath = file.strip()
            if filepath != "":
                print(filepath)
                generate_report(filepath)


def generate_report_name(filepath: str):
    directories = filepath.split("/")
    date_dashed = f"{directories[1]}-{directories[2]}-{directories[3]}"
    filepath = f"{REPORT_DIR}/{date_dashed}-pitching.pdf"
    index = 1
    while os.path.exists(filepath):
        filepath = f"{REPORT_DIR}/{date_dashed}-pitching({index}).pdf"
        index += 1
    return filepath


def generate_report(filepath: str):
    """
    Generate a report for the game with the given FTP file path.
    """
    pdf = Canvas(generate_report_name(filepath), pageSize=letter)
    df = pd.read_csv(f"{ADDRESS}/{filepath}")
    df.dropna(subset=[SPIN_RATE, HORIZONTAL_BREAK, VERTICAL_BREAK], inplace=True)
    for pid in df[ID].unique():
        generate_pitcher_report(pdf, df, pid)
    pdf.save()


def generate_pitcher_report(pdf: Canvas, df: pd.DataFrame, pid: str):
    """
    Provide a page-long report for a pitcher's outing.
    """
    pitcher_df = df.loc[df[ID] == pid]
    name = pitcher_df[NAME].unique()[0]
    last_name = name.split(", ")[0]
    first_name = name.split(", ")[1]
    throwing_hand = pitcher_df[THROWING_HAND].unique()[0]
    pdf.drawString(
        100,
        100,
        f"{first_name} {last_name} ({throwing_hand[0] if type(throwing_hand) == str else "n/a"}) - {len(pitcher_df)} Tracked Pitches",
    )
    generate_arsenal_chart(pitcher_df)
    generate_location_chart(pitcher_df)
    generate_release_chart(pitcher_df)
    for index, fig in [(n, plt.figure(n)) for n in plt.get_fignums()]:
        plotToPDF(pdf, fig, 1 * inch, 1 + 3 * index * inch, 2 * inch, 2 * inch)
        plt.close(fig)
    pdf.showPage()


def generate_arsenal_chart(df: pd.DataFrame):
    fig1, arsenal = plt.subplots()
    arsenal.set_title("Pitch Arsenal")
    arsenal.set_xlabel("Induced Horizontal Break (in)")
    arsenal.set_ylabel("Induced Vertical Break (in)")
    arsenal.set_xlim(-25, 25)
    arsenal.set_ylim(-25, 25)
    arsenal.grid(True)

    color_index = 0
    for pt in df[PITCH_TYPE].unique():
        pitch_type_df = df.loc[df[PITCH_TYPE] == pt]
        spinrate_avg = pitch_type_df[SPIN_RATE].mean().round()
        spinrate_std = pitch_type_df[SPIN_RATE].std().round(1)
        arsenal.plot(
            pitch_type_df[HORIZONTAL_BREAK],
            pitch_type_df[VERTICAL_BREAK],
            f"{colors[color_index]}o",
            label=f"{pt} ({spinrate_avg} rpm)",
        )
        color_index = (color_index + 1) % len(colors)
    arsenal.legend()
    return fig1


def generate_location_chart(df: pd.DataFrame):
    fig2, locations = plt.subplots()
    locations.set_title("Pitch Locations")
    locations.set_xlabel("Horizontal Location (ft)")
    locations.set_ylabel("Vertical Location (ft)")
    locations.set_xlim(-4, 4)
    locations.set_ylim(-1, 7)
    locations.grid(True)
    rect = patches.Rectangle(
        (-8.5 / 12.0, 1.5),
        17.0 / 12.0,
        2.5,
        linewidth=2,
        edgecolor="none",
        facecolor="0.75",
    )
    locations.add_patch(rect)

    color_index = 0
    for pt in df[PITCH_TYPE].unique():
        pitch_type_df = df.loc[df[PITCH_TYPE] == pt]
        velo_avg = pitch_type_df[VELOCITY].mean().round(1)
        velo_std = pitch_type_df[VELOCITY].std().round(2)
        # Try to classify by strikes and balls and improve strike zone position. Switch to scatter. Add text labels for pitchNo
        locations.plot(
            pitch_type_df[HORIZONTAL_POSITION],
            pitch_type_df[VERTICAL_POSITION],
            f"{colors[color_index]}o",
            label=f"{pt} ({velo_avg} mph)",
        )
        color_index = (color_index + 1) % len(colors)
    locations.legend()
    return fig2


def generate_release_chart(df: pd.DataFrame):
    fig3, release = plt.subplots()
    release.set_title("Pitch Release Points")
    release.set_xlabel("Release Side (ft)")
    release.set_ylabel("Release Height (ft)")
    release.set_xlim(-3, 3)
    release.set_ylim(2, 8)
    release.grid(True)

    color_index = 0
    for pt in df[PITCH_TYPE].unique():
        pitch_type_df = df.loc[df[PITCH_TYPE] == pt]
        extension_avg = pitch_type_df[EXTENSION].mean().round(2)
        extension_std = pitch_type_df[EXTENSION].std().round(3)
        release.plot(
            pitch_type_df[RELEASE_SIDE],
            pitch_type_df[RELEASE_HEIGHT],
            f"{colors[color_index]}o",
            label=f"{pt} ({extension_avg} ft ext)",
        )
        color_index = (color_index + 1) % len(colors)
    release.legend()
    return fig3


def generate_analysis_table(df: pd.DataFrame):
    for pt in df[PITCH_TYPE].unique():
        pitch_type_df = df.loc[df[PITCH_TYPE] == pt]
        spinaxis_avg = pitch_type_df[SPIN_AXIS].mean().round()
        spinaxis_std = pitch_type_df[SPIN_AXIS].std().round(1)
        approach_avg = pitch_type_df[VERITCAL_APPROACH].mean().round(1)
        approach_std = pitch_type_df[VERITCAL_APPROACH].std().round(2)


def plotToPDF(pdf: Canvas, figure, x: float, y: float, width: float, height: float):
    plotImg = io.BytesIO()
    figure.savefig(plotImg, format="png")
    plotImg.seek(0)
    image = ImageReader(plotImg)
    pdf.drawImage(image, x, y, width, height)


if __name__ == "__main__":
    main()
