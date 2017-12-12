import os
import sqlite3
import requests

conn = sqlite3.connect('app.db')

c = conn.cursor()

# Create table
with open('schema.sql') as file:
    c.executescript(file.read())

# Insert a row of data
r = requests.get('https://epic.gsfc.nasa.gov/api/natural')
for image in r.json():
    c.execute("INSERT INTO images(title, pic_date, centroid_lat, centroid_lon, url) VALUES (?, ?, ?, ?, ?)",
              (image["caption"], image["date"], image["centroid_coordinates"]["lat"],
               image["centroid_coordinates"]["lon"], image["image"] + ".jpg"))

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()