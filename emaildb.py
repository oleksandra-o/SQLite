import sqlite3

# Connect to the database
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

# Drop the Counts table if it exists and create a new one with 'org' column
cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

# Prompt for a file name
fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)

# Process each line in the file
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    # Extract the domain (organization) from the email address
    org = email.split('@')[1]
    
    # Check if this org already exists in the database
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    
    # If org is not found, insert it with count 1
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    # If org is found, update the count
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    
    conn.commit()

# Select the top 10 organizations by count and display them
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()