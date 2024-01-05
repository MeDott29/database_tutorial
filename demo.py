import streamlit as st
import sqlite3

# Assuming a streamlit app, we would have some setup code like this:

# Connecting to the database again (use the same connection code as above)
conn = sqlite3.connect('conversations.db', check_same_thread=False) # Streamlit workaround

# UI to select a conversation
st.title("Conversation Viewer")
conversations_list = conn.execute("SELECT id, title FROM conversations").fetchall()
conversation_titles = {title: id for id, title in conversations_list}
selected_convo = st.selectbox("Choose a conversation", options=conversation_titles.keys())

# Retrieve and display messages
if selected_convo:
    messages = conn.execute("SELECT author, content, timestamp FROM messages WHERE conversation_id = ?", (conversation_titles[selected_convo],)).fetchall()
    for author, content, timestamp in messages:
        st.write(f"{timestamp} - {author}: {content}")

# Close the database connection
conn.close()