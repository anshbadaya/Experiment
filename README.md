# Google Sheets API Service

This Flask API service reads data from a publicly accessible Google Sheets document and returns it in a frontend-compatible format.

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the service:**
   ```bash
   python service.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoint

### Get All Matches (`/matches`)

Retrieves all match data from the Google Sheets in frontend-compatible format.

**Response Format:**

```typescript
interface FixturesResponse {
  count: number;
  data: FixtureOdds[];
  date: string;
  status: "success" | "error";
}

interface FixtureOdds {
  match_code: number;
  match_date: string;
  match_number: string;
  match_time: string;
  season: string;
  sport: string;
  teams: {
    pre_match_win_odds: number;
    team_name: string;
  }[];
  top_defenders: {
    player_code: string;
    player_name: string;
    pre_match_top_defender_odds: number;
    role: string;
    team_name: string;
  }[];
  top_raiders: {
    player_code: string;
    player_name: string;
    pre_match_top_raider_odds: number;
    role: string;
    team_name: string;
  }[];
  tournament_name: string;
  venue: {
    city: string;
    stadium: string;
  };
}
```

**Example Response:**

```json
{
  "status": "success",
  "data": [
    {
      "match_code": 6464,
      "match_date": "2025-01-15",
      "match_number": "Match 6464",
      "match_time": "20:00",
      "season": "2025",
      "sport": "Kabaddi",
      "teams": [
        {
          "team_name": "Telugu Titans",
          "pre_match_win_odds": 1.9
        },
        {
          "team_name": "Tamil Thalaivas",
          "pre_match_win_odds": 2.5
        }
      ],
      "top_defenders": [],
      "top_raiders": [],
      "tournament_name": "Pro Kabaddi League",
      "venue": {
        "city": "Mumbai",
        "stadium": "Dome @ NSCI SVP Stadium"
      }
    }
  ],
  "count": 1,
  "date": "2025-08-29"
}
```

## Data Source

The API reads from the Google Sheets document at:
https://docs.google.com/spreadsheets/d/1nqZq5SltAVtZj7suTed2QHxHnvKdS3cpD6JnMdldNik/edit?usp=sharing

The sheet contains columns:

- `match_code`: Unique identifier for each match
- `team_name`: Name of the team
- `updated_odds`: Current odds for the team

## Notes

- The service automatically cleans empty rows from the data
- All odds are converted to float values for consistency
- The API uses pandas to read the public Google Sheets directly
- No authentication is required since the sheet is publicly accessible
- Default values are used for fields not present in the sheet (dates, times, venue, etc.)
