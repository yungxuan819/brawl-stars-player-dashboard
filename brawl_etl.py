# %%
# import necessary libraries
import requests 
import pandas as pd
import sqlite3 
from config import API_TOKEN, PLAYER_TAG
import time 

# %%
BASE_URL = "https://api.brawlstars.com/v1"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Extract players, brawlers, and battle log data from the Brawl Stars API
def extract(player_tags):
    all_data = []

    # Get brawlers once
    brawlers_res = requests.get(BASE_URL + "/brawlers", headers=HEADERS)
    brawlers_data = brawlers_res.json() if brawlers_res.status_code == 200 else None

    for tag in player_tags:
        print(f"\nExtracting data for: {tag}")
        player_tag_encoded = tag.replace("#", "%23")
        endpoints = {
            "player": f"/players/{player_tag_encoded}",
            "battlelog": f"/players/{player_tag_encoded}/battlelog"
        }

        data = {}
        for key, endpoint in endpoints.items():
            url = BASE_URL + endpoint
            res = requests.get(url, headers=HEADERS)
            print(f"  - {key} status: {res.status_code}")
            if res.status_code == 200:
                data[key] = res.json()
            else:
                print(f"Failed to fetch {key} data for tag {tag}. Status code: {res.status_code}")
                data[key] = None

        data["player_tag"] = tag  # Keep track of whose data this is
        all_data.append(data)

        time.sleep(0.2)  # Wait 200ms between requests to avoid rate limit
        
        print(f"\n✅ Total players processed: {len(all_data)}")

    return all_data, brawlers_data



# Transform the extracted data into a structured format
def transform(all_data, brawlers_data):
    player_df_list = []
    battlelog_df_list = []

    for data in all_data:
        tag = data.get("player_tag", "")

        if data['player']:
            temp_player_df = pd.json_normalize(data['player'])
            temp_player_df['player_tag'] = tag
            player_df_list.append(temp_player_df)

        if data['battlelog']:
            battle_logs = data['battlelog']['items']
            temp_battlelog_df = pd.json_normalize(
                battle_logs,
                sep='_',
                meta=['battleTime'],
                record_prefix='battlelog_'
            )
            temp_battlelog_df['player_tag'] = tag
            battlelog_df_list.append(temp_battlelog_df)

    player_df = pd.concat(player_df_list, ignore_index=True) if player_df_list else pd.DataFrame()
    battlelog_df = pd.concat(battlelog_df_list, ignore_index=True) if battlelog_df_list else pd.DataFrame()
    brawlers_df = pd.json_normalize(brawlers_data['items']) if brawlers_data else pd.DataFrame()

    return player_df, brawlers_df, battlelog_df




# Load the transformed data into a SQLite database
def load(player_df, brawlers_df, battlelog_df, db_name="brawl_data_2.db"):
    conn = sqlite3.connect(db_name)
    
    # Convert unsupported data types to strings
    player_df = player_df.applymap(lambda x: str(x) if isinstance(x, (dict, list)) else x)
    brawlers_df = brawlers_df.applymap(lambda x: str(x) if isinstance(x, (dict, list)) else x)
    battlelog_df = battlelog_df.applymap(lambda x: str(x) if isinstance(x, (dict, list)) else x)
    
    # Create tables and load data into SQLite database
    player_df.to_sql("player", conn, if_exists="replace", index=False)
    brawlers_df.to_sql("brawlers", conn, if_exists="replace", index=False)
    battlelog_df.to_sql("battlelog", conn, if_exists="replace", index=False)
    conn.close()
    print("Data successfully loaded into brawl_data_2.db")
    

# %%
# Main function to run the ETL pipeline
# Run the ETL for multiple players
data, brawlers_data = extract(PLAYER_TAG)
player_df, brawlers_df, battlelog_df = transform(data, brawlers_data)
load(player_df, brawlers_df, battlelog_df)

# %%
