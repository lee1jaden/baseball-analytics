# Baseball Analytics

## Overview

- **Title: baseball-analytics**
- *Owner: Jaden Lee*
- Affiliation: University of Utah
- Email: <u1417827@utah.edu>
- Created Date: September 8, 2024
- Repository Link: [Click here!](https://github.com/lee1jaden/baseball-analytics)
- Description: This repository is for personal and team use experimenting with baseball data analytics. 
- Copyright: This code may be copied and edited for reuse, but please cite this source repository.

> How can you not be romantic about baseball? - Billy Beane in Moneyball

[![The backdrop at Smith's Ballpark is incredible!](/smiths-ballpark.webp "Smith's Ballpark: Home of Utah Baseball")](https://utahutes.com/sports/baseball)

## Installation

1. Install Python and a virtual environment such as venv on your machine. Make sure to activate it before installing dependencies from the 'requirements.txt' file.
1. To install dependencies, run the following commands:
    ```
    pip install pipreqs
    pip install -r requirements.txt
    ```
1. If trying to access data from the FTP server, add a file called "my_secrets.py" and create variables with the HOST, USERNAME, PASSWORD, and SERVER_DIRECTORY needed to connect.
1. Run python executables from the terminal or use the debug window.
1. To update dependencies, run the following command:
    > pipreqs . --ignore ./.venv --force
1. If a Python file does not run, provide executable permissions with:
    > chmod +x [filepath]

## References

1. Here is a link to an overview of the data typically contained in TrackMan CSV files: <https://support.trackmanbaseball.com/hc/en-us/articles/5089413493787-V3-FAQs-Radar-Measurement-Glossary-Of-Terms>

## Files

### Pitcher Development Reports

- Name: pitcher-development.py
- Author: Jaden Lee
- Created Date: September 8, 2024
- Description: This folder is specifically for analyzing TrackMan data for pitchers. The plan is to run these after games and scrimmages to provide feedback for pitchers. The emphasis should be on process more than results.

### Sandbox

- Name: example.py
- Author: Jaden Lee
- Created Date: September 8, 2024
- Description: This file is to experiment with the libraries we need. It can be a sandbox file to test out code.