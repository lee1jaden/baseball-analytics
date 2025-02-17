#!/usr/bin/env python3
"""
This file retrieves a list of games for the given 
"""

from ftplib import FTP
from my_secrets import HOST, USERNAME, PASSWORD

# Create file storage locations for data
DATA_DIR = "./data"
NAME = "FLA_GAT"
YEAR = "2024"
MONTH = "07"
DAY = "12"


def main(): 
    matching_files = []

    ftp = FTP(HOST, USERNAME, PASSWORD)
    ftp.cwd(f"v3/{YEAR}")
    for month in ftp.nlst():
        if MONTH is None or month == MONTH:
            ftp.cwd(month)
            for day in ftp.nlst():
                if DAY is None or day == DAY: 
                    ftp.cwd(f"{day}/CSV")
                    print(f"{YEAR}-{month}-{day}...")
                    for csv_file in ftp.nlst():
                        if "playerpositioning" not in csv_file:
                            if file_matches(ftp, csv_file):
                                matching_files.append(f"/v3/{YEAR}/{month}/{day}/{csv_file}")
                    ftp.cwd("../..")
            ftp.cwd("..")
    ftp.quit()
    save_matching_files(matching_files)


def file_matches(ftp: FTP, filepath: str):
    def handle_line(line):
        if NAME in line:
            nonlocal found
            found = True

    found = False
    ftp.retrlines(f"RETR {filepath}", handle_line)
    return found


def save_matching_files(matching_files: list[str]):
    games_filepath = f"{DATA_DIR}/{NAME}.txt"
    with open(games_filepath, "w") as games_file:
        for match_file in matching_files:
            games_file.write(match_file + '\n')


if __name__=="__main__":
    main()