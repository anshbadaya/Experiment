from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app, origins="*", allow_headers="*", methods="*", supports_credentials=True)

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Your Google Sheets URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1nqZq5SltAVtZj7suTed2QHxHnvKdS3cpD6JnMdldNik/edit?usp=sharing"

def get_sheet_data():
    """Read data from Google Sheets - always fetches latest data"""
    try:
        # For public sheets, we can use pandas directly
        # Extract sheet ID from URL
        sheet_id = "1nqZq5SltAVtZj7suTed2QHxHnvKdS3cpD6JnMdldNik"
        
        # Read the sheet using pandas - this always gets the latest data
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
        df = pd.read_csv(url)
        
        # Clean the data - remove empty rows
        df = df.dropna(subset=['match_code', 'team_name', 'updated_odds'])
        
        return df.to_dict('records')
    except Exception as e:
        print(f"Error reading sheet: {e}")
        return []

@app.route('/matches')
def get_matches():
    """Get only real data from Google Sheets - no dummy data"""
    try:
        # Always fetch fresh data from Google Sheets
        data = get_sheet_data()
        
        # Debug: Print the raw data from Google Sheets
        print("=== Raw Google Sheets Data ===")
        for i, row in enumerate(data, start=1):
            print(f"Row {i}: Match Code: {row['match_code']}, Team: {row['team_name']}, Odds: {row['updated_odds']}")
        print("==============================")
        
        # Group data by match_code
        matches_dict = {}
        for row in data:
            match_code = str(row['match_code'])
            if match_code not in matches_dict:
                matches_dict[match_code] = {
                    'teams': []
                }
            
            # Add team data with real odds from Google Sheets
            team_data = {
                'team_name': row['team_name'],
                'pre_match_win_odds': float(row['updated_odds']) if row['updated_odds'] else 0.0
            }
            matches_dict[match_code]['teams'].append(team_data)
        
        # Convert to frontend format with only real data
        fixtures_data = []
        for match_code, match_data in matches_dict.items():
            fixture = {
                'match_code': int(match_code),
                'match_date': datetime.now().strftime("%Y-%m-%d"),
                'match_number': f"Match {match_code}",
                'match_time': 'TBD',
                'season': '2025',
                'sport': 'Kabaddi',
                'teams': match_data['teams'],
                'top_defenders': [],
                'top_raiders': [],
                'tournament_name': 'Pro Kabaddi League',
                'venue': {
                    'city': 'TBD',
                    'stadium': 'TBD'
                }
            }
            fixtures_data.append(fixture)
        
        return jsonify({
            "status": "success",
            "data": fixtures_data,
            "count": len(fixtures_data),
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/debug/sheet-data')
def debug_sheet_data():
    """Debug endpoint to show raw Google Sheets data"""
    try:
        data = get_sheet_data()
        return jsonify({
            "status": "success",
            "raw_data": data,
            "count": len(data),
            "message": "Raw data from Google Sheets"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
