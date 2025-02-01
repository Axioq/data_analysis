import os
import json
import requests
import pandas as pd
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

OWNED_GAMES_ENDPOINT = f"{STEAM_API_URL}/IPlayerService/GetOwnedGames/v0001/"
RECENT_GAMES_ENDPOINT = f"{STEAM_API_URL}/IPlayerService/GetRecentlyPlayedGames/v0001/"
PLAYER_ACHIEVEMENTS_ENDPOINT = f"{STEAM_API_URL}/ISteamUserStats/GetPlayerAchievements/v0001/"

def fetch_owned_games(api_key, steam_id):
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    response = requests.get(OWNED_GAMES_ENDPOINT, params=params)
    if response.status_code == 200:
        games = response.json().get("response", {}).get("games", [])
        return games
    else:
        print("Failed to fetch owned games:", response.status_code, response.text)
        return []

def fetch_recent_games(api_key, steam_id):
    params = {"key": api_key, "steamid": steam_id, "format": "json"}
    response = requests.get(RECENT_GAMES_ENDPOINT, params=params)
    if response.status_code == 200:
        games = response.json().get("response", {}).get("games", [])
        return games
    else:
        print("Failed to fetch recent games:", response.status_code, response.text)
        return []

def fetch_achievements(api_key, steam_id, appid):
    params = {"key": api_key, "steamid": steam_id, "appid": appid, "format": "json"}
    response = requests.get(PLAYER_ACHIEVEMENTS_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json().get("playerstats", {}).get("achievements", [])
    else:
        print(f"Failed to fetch achievements for {appid}: {response.status_code}")
        return []

def main():
    # Fetch Owned Games
    owned_games = fetch_owned_games(API_KEY, STEAM_ID)
    df_owned = pd.DataFrame(owned_games)
    if not df_owned.empty:
        df_owned["playtime_hours"] = df_owned["playtime_forever"] / 60
        df_owned.to_csv("data/owned_games.csv", index=False)
        print("Owned games data saved.")
    
    # Fetch Recent Games
    recent_games = fetch_recent_games(API_KEY, STEAM_ID)
    df_recent = pd.DataFrame(recent_games)
    if not df_recent.empty:
        df_recent["playtime_hours"] = df_recent["playtime_2weeks"] / 60
        df_recent.to_csv("data/recent_games.csv", index=False)
        print("Recent games data saved.")
    
    # Fetch Achievements for All Owned Games
    achievement_list = []
    for _, game in df_owned.iterrows():
        game_achievements = fetch_achievements(API_KEY, STEAM_ID, game["appid"])
        for ach in game_achievements:
            ach["game_name"] = game["name"]
            achievement_list.append(ach)
    
    df_achievements = pd.DataFrame(achievement_list)
    if not df_achievements.empty:
        df_achievements.to_csv("data/achievements.csv", index=False)
        print("Achievements data saved.")

if __name__ == "__main__":
    main()
