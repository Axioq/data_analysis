import os
import json
import requests
from dotenv import load_dotenv

 # Load variables from .env file
load_dotenv()

# Define Steam API base URL, API Key and Steam_ID
STEAM_API_URL = "https://api.steampowered.com"
API_KEY = os.getenv("STEAM_API_KEY")
if not API_KEY:
    raise ValueError("Missing Steam API Key. Set it in a .env file or as an environment variable.")
STEAM_ID = os.getenv("STEAM_ID")
if not STEAM_ID:
    raise ValueError("Missing Steam ID. Set it in a .env file or as an environment variable.")

# Steam API endpoints
PLAYER_SUMMARY_ENDPOINT = f"{STEAM_API_URL}/ISteamUser/GetPlayerSummaries/v0002/"
OWNED_GAMES_ENDPOINT = f"{STEAM_API_URL}/IPlayerService/GetOwnedGames/v0001/"

def fetch_player_summary(api_key, steam_id):
    params = {
        "key": api_key,
        "steamids": steam_id
    }
    response = requests.get(PLAYER_SUMMARY_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json().get("response", {}).get("players", [])[0]
    else:
        print("Failed to fetch player summary:", response.status_code, response.text)
        return None

def fetch_owned_games(api_key, steam_id):
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    response = requests.get(OWNED_GAMES_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json().get("response", {}).get("games", [])
    else:
        print("Failed to fetch owned games:", response.status_code, response.text)
        return None

def main():
    # Step 1: Fetch Player Summary
    player_summary = fetch_player_summary(API_KEY, STEAM_ID)
    if player_summary:
        print("Player Summary:")
        print(json.dumps(player_summary, indent=2))

    # Step 2: Fetch Owned Games
    owned_games = fetch_owned_games(API_KEY, STEAM_ID)
    if owned_games:
        print("\nOwned Games:")
        for game in owned_games:
            print(f"{game['name']} - Playtime: {game['playtime_forever'] / 60:.2f} hours")

if __name__ == "__main__":
    main()

