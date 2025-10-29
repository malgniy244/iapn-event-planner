from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

# IAPN event library
EVENT_LIBRARY = [
    {"id": 1, "name": "Welcome Reception in Murray", "description": "", "duration": "3 hours", "perPersonCost": 1180, "minimumCost": 140000, "category": "food"},
    {"id": 5, "name": "Welcome Reception in Hyatt Regency", "description": "", "duration": "3 hours", "perPersonCost": 818, "minimumCost": 68800, "category": "food"},
    {"id": 6, "name": "Gala Dinner in The Verandah", "description": "", "duration": "Dinner", "perPersonCost": 1628, "minimumCost": 360000, "category": "food"},
    {"id": 9, "name": "Gala Dinner in Crown Wine Cellar", "description": "", "duration": "Dinner", "perPersonCost": 1688, "minimumCost": 110000, "category": "food"},
    {"id": 10, "name": "Gala Dinner in WaterMark", "description": "", "duration": "Dinner", "perPersonCost": 0, "minimumCost": 168000, "category": "food"},
    {"id": 11, "name": "Sai Kung Seafood Dinner", "description": "", "duration": "Dinner", "perPersonCost": 1000, "minimumCost": 0, "category": "food"},
    {"id": 12, "name": "Star Ferry", "description": "110 passengers. 3 hours 45,000", "duration": "Cocktail", "perPersonCost": 0, "minimumCost": 45000, "category": "food"},
    {"id": 15, "name": "Star Ferry Canapes/ Lunch", "description": "Canapes Room.", "duration": "Cocktail", "perPersonCost": 500, "minimumCost": 0, "category": "food"},
    {"id": 2, "name": "Conference Hall Rental in Murray", "description": "Main venue for keynote sessions", "duration": "Half Day", "perPersonCost": 0, "minimumCost": 75000, "category": "venue"},
    {"id": 7, "name": "Conference Hall Rental in Hyatt Regency", "description": "Main venue for keynote sessions", "duration": "Half Day", "perPersonCost": 0, "minimumCost": 40800, "category": "venue"},
    {"id": 8, "name": "Conference Hall Rental in W Hotel", "description": "Main venue for keynote sessions", "duration": "Half Day", "perPersonCost": 0, "minimumCost": 118000, "category": "venue"},
    {"id": 3, "name": "Workshop Session", "description": "Interactive training with materials", "duration": "4 hours", "perPersonCost": 1200, "minimumCost": 0, "category": "venue"},
    {"id": 13, "name": "Tour Bus for Macau", "description": "2 buses, 1 bus 4500 full day estimate", "duration": "", "perPersonCost": 0, "minimumCost": 9000, "category": "other"},
    {"id": 14, "name": "Macau Lunch - Portugese Food", "description": "Budget 500 per person", "duration": "", "perPersonCost": 500, "minimumCost": 0, "category": "other"},
    {"id": 16, "name": "Sai Kung Alcohol Cost", "description": "Buy Bottles and bring there.", "duration": "", "perPersonCost": 299.98, "minimumCost": 0, "category": "other"},
    {"id": 17, "name": "Dragon Dance Performance", "description": "", "duration": "", "perPersonCost": 0, "minimumCost": 10000, "category": "other"},
    {"id": 18, "name": "Dim Sum Lunch", "description": "", "duration": "Lunch", "perPersonCost": 350, "minimumCost": 0, "category": "other"},
    {"id": 19, "name": "Korean BBQ Dinner", "description": "", "duration": "Dinner", "perPersonCost": 800, "minimumCost": 0, "category": "other"},
    {"id": 20, "name": "Star Ferry Alcohol Cost", "description": "", "duration": "Lunch", "perPersonCost": 300, "minimumCost": 0, "category": "other"},
    {"id": 21, "name": "Murray Lunch", "description": "", "duration": "", "perPersonCost": 600, "minimumCost": 0, "category": "other"},
    {"id": 22, "name": "Jocky Club Lunch- Saturday/ Sunday", "description": "Wouldnt know until the race schedule out in 2026.", "duration": "", "perPersonCost": 830, "minimumCost": 0, "category": "other"}
]

def get_event_by_id(event_id):
    """Get full event object by ID"""
    for event in EVENT_LIBRARY:
        if event['id'] == event_id:
            return event.copy()
    return None

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_database():
    """Create table if it doesn't exist and initialize with default data"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS plan_data (
                id INTEGER PRIMARY KEY DEFAULT 1,
                data JSONB NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if data exists
        cur.execute("SELECT COUNT(*) as count FROM plan_data WHERE id = 1")
        result = cur.fetchone()
        
        if result['count'] == 0:
            # Insert default IAPN data
            default_data = {
                "eventTitle": "IAPN 2027 May 21-24",
                "eventDescription": "",
                "attendees": 100,
                "currency": "HKD",
                "events": EVENT_LIBRARY,
                "days": [
                    {"id": "day1", "label": "Day 1", "notes": ""},
                    {"id": "day2", "label": "Day 2", "notes": "Murray Conference->Star Ferry Lunch->Sai Kung Seafood Dinner"},
                    {"id": "day3", "label": "Day 3", "notes": "Macau Day Trip->Lunch in Macau-> Come BackBBQ"},
                    {"id": "day4", "label": "Day 4", "notes": "Conference->Dim Sum->Gala"}
                ],
                "schedule": {
                    "day1": [get_event_by_id(1)],
                    "day2": [get_event_by_id(2), get_event_by_id(11), get_event_by_id(16), get_event_by_id(17), get_event_by_id(12), get_event_by_id(15), get_event_by_id(20)],
                    "day3": [get_event_by_id(13), get_event_by_id(14), get_event_by_id(19)],
                    "day4": [get_event_by_id(2), get_event_by_id(18), get_event_by_id(6)]
                },
                "nextEventId": 23,
                "nextDayId": 5
            }
            
            cur.execute(
                "INSERT INTO plan_data (id, data) VALUES (1, %s)",
                (json.dumps(default_data),)
            )
        
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

def load_data():
    """Load data from database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT data FROM plan_data WHERE id = 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            return result['data']
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def save_data(data):
    """Save data to database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE plan_data SET data = %s, updated_at = CURRENT_TIMESTAMP WHERE id = 1",
            (json.dumps(data),)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# Initialize database on startup
if DATABASE_URL:
    init_database()
else:
    print("WARNING: No DATABASE_URL found. Data will not persist!")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all plan data"""
    data = load_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "No data found"}), 404

@app.route('/api/data', methods=['POST'])
def update_data():
    """Save all plan data"""
    try:
        data = request.json
        if save_data(data):
            return jsonify({"success": True, "message": "Data saved successfully"})
        else:
            return jsonify({"success": False, "error": "Failed to save data"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected" if DATABASE_URL else "not configured"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
