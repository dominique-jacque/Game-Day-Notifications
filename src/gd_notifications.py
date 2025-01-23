import os
import json
import urllib.request
import boto3
from datetime import datetime, timedelta, timezone

# Format game data into a readable message
def format_game_data(game):
    # Extract relevant game details
    home_team = game.get("HomeTeamName", "Unknown")
    away_team = game.get("AwayTeamName", "Unknown")
    status = game.get("Status", "Unknown")
    start_time = game.get("DateTime", "Unknown")
    final_score = f"{game.get('HomeTeamScore', 'N/A')} - {game.get('AwayTeamScore', 'N/A')}"

    # Format the message based on the game status
    if status == "Final":
        return (
            f"Game Status: {status}\n"
            f"{home_team} {final_score} {away_team}\n"
            f"Kickoff: {start_time}\n"
        )
    elif status == "Scheduled":
        return (
            f"Game Status: {status}\n"
            f"{home_team} vs {away_team}\n"
            f"Kickoff: {start_time}\n"
        )
    elif status == "InProgress":
        return (
            f"Game Status: {status}\n"
            f"{home_team} {final_score} {away_team}\n"
            f"Kickoff: {start_time}\n"
        )
    else:
        return (
            f"Game Status: {status}\n"
            f"{home_team} vs {away_team}\n"
            f"Details are unavailable.\n"
        )

# Lambda handler function
def lambda_handler(event, context):
    # Get environment variables
    api_key = os.getenv("SOCCER_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")
    
    # Adjust for Central Time (UTC-6)
    utc_now = datetime.now(timezone.utc)
    central_time = utc_now - timedelta(hours=6)
    today_date = central_time.strftime("%Y-%m-%d")
    
    # Define competition and API URL
    competition = "MLS"  # Replace with your desired league
    api_url = f"https://api.sportsdata.io/v4/soccer/scores/json/GamesByDate/{competition}/{today_date}?key={api_key}"
    
    print(f"Fetching games for date: {today_date}")
    print(f"API URL: {api_url}")

    try:
        # Fetch data from the API
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            print(f"API Response: {json.dumps(data, indent=4)}")  # Log raw API data
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return {"statusCode": 500, "body": "Error fetching data from the API"}
    
    # Check if there are games for the given date
    if not data:
        # No games found, set a default message
        final_message = "No games are scheduled for today."
    else:
        # Format the data for all available games
        messages = [format_game_data(game) for game in data]
        final_message = "\n---\n".join(messages)
    
    # Publish the final message to SNS
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="Soccer Game Updates"
        )
        print("Message published to SNS successfully.")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}
    
    return {"statusCode": 200, "body": "Data processed and sent to SNS"}
