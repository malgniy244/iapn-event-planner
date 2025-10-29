from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Data file
DATA_FILE = 'plan_data.json'

# Initialize with IAPN data if file doesn't exist
def init_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "eventTitle": "IAPN 2027 May 21-24",
            "eventDescription": "",
            "attendees": 100,
            "currency": "HKD",
            "events": [
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
            ],
            "days": [
                {"id": "day1", "label": "Day 1", "notes": ""},
                {"id": "day2", "label": "Day 2", "notes": "Murray Conference->Star Ferry Lunch->Sai Kung Seafood Dinner"},
                {"id": "day3", "label": "Day 3", "notes": "Macau Day Trip->Lunch in Macau-> Come BackBBQ"},
                {"id": "day4", "label": "Day 4", "notes": "Conference->Dim Sum->Gala"}
            ],
            "schedule": {
                "day1": [1],
                "day2": [2, 11, 16, 17, 12, 15, 20],
                "day3": [13, 14, 19],
                "day4": [2, 18, 6]
            },
            "nextEventId": 23,
            "nextDayId": 5
        }
        save_data(default_data)
        return default_data
    return load_data()

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return init_data()

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize data on startup
init_data()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all plan data"""
    data = load_data()
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def update_data():
    """Save all plan data"""
    try:
        data = request.json
        save_data(data)
        return jsonify({"success": True, "message": "Data saved successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
