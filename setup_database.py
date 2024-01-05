import sqlite3

# Connect to SQLite database (or create it if it does not exist)
conn = sqlite3.connect('conversations.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create tables 'conversations' and 'messages'
cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER,
    author TEXT,
    content TEXT,
    timestamp DATETIME,
    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
)
''')

# Insert sample data into the 'conversations' table
cursor.execute("INSERT INTO conversations (title) VALUES ('Project Discussion')")
cursor.execute("INSERT INTO conversations (title) VALUES ('Team Standup')")

# Committing the changes
conn.commit()

# Insert sample data into the 'messages' table
conversation_id = cursor.lastrowid
messages = [
    (conversation_id, 'User 1', 'Hello, how is the project going?', '2023-04-10 09:00:00'),
    (conversation_id, 'User 2', 'Hi! Making good progress, how about you?', '2023-04-10 09:01:00'),
    # Add as many messages as needed...
]

cursor.executemany("INSERT INTO messages (conversation_id, author, content, timestamp) VALUES (?, ?, ?, ?)", messages)

# Committing the changes
conn.commit()

# Querying the database to retrieve messages from a specific conversation
cursor.execute("""
SELECT m.content, m.author, m.timestamp 
FROM messages m 
JOIN conversations c ON m.conversation_id = c.id 
WHERE c.title = 'Project Discussion'
""")
rows = cursor.fetchall()
for row in rows:
    print(f"{row[1]} at {row[2]} said: {row[0]}")

# Close the connection
conn.close()
