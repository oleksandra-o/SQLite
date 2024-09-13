import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Artist (
    id  INTEGER PRIMARY KEY,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER  PRIMARY KEY,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER PRIMARY KEY,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER PRIMARY KEY,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

handle = open('tracks.csv')

# Another One Bites The Dust,Queen,Greatest Hits,Rock,55,100,217103
#   0                          1      2           3    4  5   6

for line in handle:
    line = line.strip()
    pieces = line.split(',')
    if len(pieces) < 7: continue  # Updated to expect 7 columns

    name = pieces[0]
    artist = pieces[1]
    album = pieces[2]
    genre = pieces[3]  # Added genre
    count = pieces[4]
    rating = pieces[5]
    length = pieces[6]

    print(name, artist, album, genre, count, rating, length)

    # Insert artist
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', (artist,))
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
    artist_id = cur.fetchone()[0]

    # Insert album
    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album,))
    album_id = cur.fetchone()[0]

    # Insert genre
    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', (genre,))
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre,))
    genre_id = cur.fetchone()[0]

    # Insert track with genre_id
    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''', 
        (name, album_id, genre_id, length, rating, count))

    conn.commit()