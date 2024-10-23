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

# ---------------------------------------------------------------------------

"""
import sys

# Read command line arguments.
arguments = sys.argv
print(arguments)
"""

# ---------------------------------------------------------------------------

"""
import pandas as pd

df = pd.read_csv('./data/example-trackman.csv')

print(df.loc[:, ["Pitcher", "Batter"]]) 
"""

# ---------------------------------------------------------------------------

"""
from ftplib import FTP
from my_secrets import HOST, USERNAME, PASSWORD
import os

ftp = FTP(HOST, USERNAME, PASSWORD)

local_dir = "data/"
server_dir = "v3/2024/10/02/CSV"
ftp.cwd(server_dir)
csv_file = ftp.nlst()[0]

with open(local_dir + csv_file, 'w') as file:
    ftp.retrlines("RETR " + csv_file, lambda text : file.write(text + '\n'))

ftp.quit()
os.remove(local_dir + csv_file)
"""
    
# ---------------------------------------------------------------------------

"""
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import matplotlib.pyplot as plt

width, height = letter  #keep for later
def hello(c):
    c.drawString(100,100,"Hello World")
    c.line(100,100,200,100)
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], "ro", label="Fastball")
    b = io.BytesIO()
    plt.savefig(b, format='png')
    b.seek(0)
    image = ImageReader(b)
    c.drawImage(image, 200, 200, width=2*inch, height=2*inch, mask=None)

c = canvas.Canvas("hello.pdf", pageSize=letter)
for i in range(5):
    hello(c)
    c.showPage()
c.save()
"""