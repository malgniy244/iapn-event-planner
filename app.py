import streamlit as st
import psycopg
from datetime import datetime
import os

# Database connection
def get_db_connection():
    return psycopg.connect(os.environ['DATABASE_URL'])

# Initialize database ONLY if truly empty
def init_database():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # CHECK if data already exists - CRITICAL FIX
    cur.execute('SELECT COUNT(*) FROM events')
    count = cur.fetchone()[0]
    
    # Only add default data if table is COMPLETELY EMPTY
    if count == 0:
        default_events = [
            ("IAPN General Meeting", "2024-11-15", "18:00", "Community Center", "Monthly general meeting"),
            ("IAPN Cultural Night", "2024-12-01", "19:00", "Main Hall", "Annual cultural celebration"),
            ("IAPN Workshop", "2024-11-20", "14:00", "Room 101", "Educational workshop")
        ]
        
        cur.executemany(
            'INSERT INTO events (title, date, time, location, description) VALUES (%s, %s, %s, %s, %s)',
            default_events
        )
        conn.commit()
        st.success("Database initialized with default IAPN events!")
    
    cur.close()
    conn.close()

# Get all events
def get_events():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, date, time, location, description FROM events ORDER BY date, time')
    events = cur.fetchall()
    cur.close()
    conn.close()
    return events

# Add new event
def add_event(title, date, time, location, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO events (title, date, time, location, description) VALUES (%s, %s, %s, %s, %s)',
        (title, date, time, location, description)
    )
    conn.commit()
    cur.close()
    conn.close()

# Update event
def update_event(event_id, title, date, time, location, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE events SET title=%s, date=%s, time=%s, location=%s, description=%s WHERE id=%s',
        (title, date, time, location, description, event_id)
    )
    conn.commit()
    cur.close()
    conn.close()

# Delete event
def delete_event(event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM events WHERE id=%s', (event_id,))
    conn.commit()
    cur.close()
    conn.close()

# Streamlit App
def main():
    st.set_page_config(page_title="IAPN Event Planner", page_icon="📅", layout="wide")
    
    # Initialize database (only adds data if empty)
    init_database()
    
    st.title("📅 IAPN Event Planner")
    st.markdown("---")
    
    # Sidebar for adding events
    with st.sidebar:
        st.header("➕ Add New Event")
        
        with st.form("add_event_form"):
            title = st.text_input("Event Title")
            date = st.date_input("Date")
            time = st.time_input("Time")
            location = st.text_input("Location")
            description = st.text_area("Description")
            
            submitted = st.form_submit_button("Add Event")
            
            if submitted:
                if title and location:
                    add_event(
                        title,
                        date.strftime("%Y-%m-%d"),
                        time.strftime("%H:%M"),
                        location,
                        description
                    )
                    st.success(f"✅ Event '{title}' added!")
                    st.rerun()
                else:
                    st.error("Please fill in at least Title and Location")
    
    # Main area - Display events
    st.header("📋 Upcoming Events")
    
    events = get_events()
    
    if not events:
        st.info("No events scheduled. Add your first event using the sidebar!")
    else:
        for event in events:
            event_id, title, date, time, location, description = event
            
            with st.expander(f"📌 {title} - {date} at {time}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**📍 Location:** {location}")
                    st.write(f"**📅 Date:** {date}")
                    st.write(f"**🕐 Time:** {time}")
                    if description:
                        st.write(f"**📝 Description:** {description}")
                
                with col2:
                    # Edit button
                    if st.button("✏️ Edit", key=f"edit_{event_id}"):
                        st.session_state[f'editing_{event_id}'] = True
                        st.rerun()
                    
                    # Delete button
                    if st.button("🗑️ Delete", key=f"delete_{event_id}"):
                        delete_event(event_id)
                        st.success(f"Deleted '{title}'")
                        st.rerun()
                
                # Edit form (shown when Edit button clicked)
                if st.session_state.get(f'editing_{event_id}', False):
                    st.markdown("---")
                    with st.form(f"edit_form_{event_id}"):
                        new_title = st.text_input("Title", value=title)
                        new_date = st.date_input("Date", value=datetime.strptime(date, "%Y-%m-%d"))
                        new_time = st.time_input("Time", value=datetime.strptime(time, "%H:%M").time())
                        new_location = st.text_input("Location", value=location)
                        new_description = st.text_area("Description", value=description or "")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            save = st.form_submit_button("💾 Save Changes")
                        with col2:
                            cancel = st.form_submit_button("❌ Cancel")
                        
                        if save:
                            update_event(
                                event_id,
                                new_title,
                                new_date.strftime("%Y-%m-%d"),
                                new_time.strftime("%H:%M"),
                                new_location,
                                new_description
                            )
                            st.session_state[f'editing_{event_id}'] = False
                            st.success("Changes saved!")
                            st.rerun()
                        
                        if cancel:
                            st.session_state[f'editing_{event_id}'] = False
                            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("**IAPN Event Planner** | Built with Streamlit & PostgreSQL")

if __name__ == "__main__":
    main()
