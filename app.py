import os
import sqlite3
import datetime
from flask import Flask, g, render_template

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='development key'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, pic_date, centroid_lat, centroid_lon, url from images')
    results = cur.fetchall()
    entries = []
    for result in results:
        entry = {}
        entry["title"] = result["title"]
        pic_date = datetime.datetime.strptime(result["pic_date"], '%Y-%m-%d %H:%M:%S')
        entry["year"] = pic_date.strftime("%Y")
        entry["month"] = pic_date.strftime("%m")
        entry["day"] = pic_date.strftime("%d")
        entry["centroid_lat"] = result["centroid_lat"]
        entry["centroid_lon"] = result["centroid_lon"]
        entry["url"] = result["url"]
        entries.append(entry)
    return render_template('epic.html', images=entries)

if __name__ == "__main__":
  app.run()
