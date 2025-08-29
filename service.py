from flask import Flask, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Your Google Sheets URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1nqZq5SltAVtZj7suTed2QHxHnvKdS3cpD6JnMdldNik/edit?usp=sharing"

def get_sheet_data():
    """Read data from Google Sheets"""
    try:
        # For public sheets, we can use pandas directly
        # Extract sheet ID from URL
        sheet_id = "1nqZq5SltAVtZj7suTed2QHxHnvKdS3cpD6JnMdldNik"
        
        # Read the sheet using pandas
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
    """Get all matches data in frontend-compatible format"""
    try:
        data = get_sheet_data()
        
        # Group data by match_code
        matches_dict = {}
        for row in data:
            match_code = str(row['match_code'])
            if match_code not in matches_dict:
                matches_dict[match_code] = {
                    'teams': [],
                    'top_defenders': [],
                    'top_raiders': []
                }
            
            # Add team data
            team_data = {
                'team_name': row['team_name'],
                'pre_match_win_odds': float(row['updated_odds']) if row['updated_odds'] else 0.0
            }
            matches_dict[match_code]['teams'].append(team_data)
        
        # Match metadata with player information
        match_metadata = {
            '6464': {
                'match_date': '2025-08-29',
                'match_number': 'Match 1',
                'match_time': '08:00 PM',
                'season': '2025',
                'sport': 'Kabaddi',
                'tournament_name': 'Pro Kabbadi league',
                'venue': {
                    'city': 'Vizag',
                    'stadium': 'Rajiv Gandhi Indoor Stadium, Vizag'
                },
                'teams': [
                    {
                        'team_name': 'Tamil Thalaivas',
                        'pre_match_win_odds': 1.9
                    },
                    {
                        'team_name': 'Telugu Titans',
                        'pre_match_win_odds': 1.9
                    }
                ],
                'top_defenders': [
                    {
                        'player_code': '4938',
                        'player_name': 'Mohit Khaler',
                        'pre_match_top_defender_odds': 2.33,
                        'role': 'Defender',
                        'team_name': 'Tamil Thalaivas'
                    },
                    {
                        'player_code': '5150',
                        'player_name': 'Nitesh Kumar',
                        'pre_match_top_defender_odds': 1.4,
                        'role': 'Defender',
                        'team_name': 'Tamil Thalaivas'
                    },
                    {
                        'player_code': '2659',
                        'player_name': 'Sagar Rathee',
                        'pre_match_top_defender_odds': 1.23,
                        'role': 'Defender',
                        'team_name': 'Tamil Thalaivas'
                    },
                    {
                        'player_code': '2501',
                        'player_name': 'Aman Mukesh',
                        'pre_match_top_defender_odds': 1.61,
                        'role': 'Defender',
                        'team_name': 'Telugu Titans'
                    },
                    {
                        'player_code': '10890',
                        'player_name': 'Ankit',
                        'pre_match_top_defender_odds': 2.99,
                        'role': 'Defender',
                        'team_name': 'Telugu Titans'
                    },
                    {
                        'player_code': '2479',
                        'player_name': 'Shubham Shashikant Shinde',
                        'pre_match_top_defender_odds': 1.9,
                        'role': 'Defender',
                        'team_name': 'Telugu Titans'
                    }
                ],
                'top_raiders': [
                    {
                        'player_code': '2024',
                        'player_name': 'Arjun Deshwal',
                        'pre_match_top_raider_odds': 2.33,
                        'role': 'Raider',
                        'team_name': 'Tamil Thalaivas'
                    },
                    {
                        'player_code': '6667',
                        'player_name': 'Moein Shafaghi',
                        'pre_match_top_raider_odds': 1.61,
                        'role': 'All Rounder',
                        'team_name': 'Tamil Thalaivas'
                    },
                    {
                        'player_code': '318',
                        'player_name': 'Pawan Kumar Sehrawat',
                        'pre_match_top_raider_odds': 1.23,
                        'role': 'All Rounder',
                        'team_name': 'Tamil Thalaivas'
                    },
                    {
                        'player_code': '3551',
                        'player_name': 'Vishal Rothas Chahal',
                        'pre_match_top_raider_odds': 2.99,
                        'role': 'Raider',
                        'team_name': 'Tamil Thalaivas'
                    },
                    {
                        'player_code': '4390',
                        'player_name': 'Ashish Kaptan Narwal',
                        'pre_match_top_raider_odds': 1.9,
                        'role': 'Raider',
                        'team_name': 'Telugu Titans'
                    },
                    {
                        'player_code': '745',
                        'player_name': 'Vijay Malik',
                        'pre_match_top_raider_odds': 1.4,
                        'role': 'All Rounder',
                        'team_name': 'Telugu Titans'
                    }
                ]
            }
        }
        
        # Convert to frontend format
        fixtures_data = []
        for match_code, match_data in matches_dict.items():
            metadata = match_metadata.get(match_code)
            
            if metadata:
                # Use exact data provided, but update team odds from Google Sheets
                teams_with_updated_odds = []
                for team in metadata['teams']:
                    # Find matching team in Google Sheets data
                    sheet_team = next((row for row in data if str(row['match_code']) == match_code and row['team_name'] == team['team_name']), None)
                    if sheet_team:
                        team['pre_match_win_odds'] = float(sheet_team['updated_odds']) if sheet_team['updated_odds'] else team['pre_match_win_odds']
                    teams_with_updated_odds.append(team)
                
                fixture = {
                    'match_code': int(match_code),
                    'match_date': metadata['match_date'],
                    'match_number': metadata['match_number'],
                    'match_time': metadata['match_time'],
                    'season': metadata['season'],
                    'sport': metadata['sport'],
                    'teams': teams_with_updated_odds,
                    'top_defenders': metadata['top_defenders'],
                    'top_raiders': metadata['top_raiders'],
                    'tournament_name': metadata['tournament_name'],
                    'venue': metadata['venue']
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
