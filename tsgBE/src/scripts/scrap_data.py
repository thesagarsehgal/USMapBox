import json 
from pathlib import Path
import os
import requests 

state_boundaries_file_path = os.path.join(Path(__file__).parent.parent,"scripts","boundaries_data","gz_2010_us_040_00_20m.json")
county_boundaries_file_path = os.path.join(Path(__file__).parent.parent,"scripts","boundaries_data","gz_2010_us_050_00_20m.json")

def fetch_metadata(search_term, target_geoid):
    url = f"https://www.census.gov/quickfacts/search/json/?type=geo&search={search_term}"
    headers = {
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "priority": "u=1, i",
        "referer": "https://www.census.gov/quickfacts/fact/table/albanycitynewyork,US/PST045224",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != 200:
            print("Unexpected status code in response.")
            return None

        for item in data.get("data", []):
            if item.get("geoid") == target_geoid:
                return item

        print(f"No entry found with geoid: {target_geoid}")
        return None

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def download_csv(code, geoid, folder_path):
    url = f"https://www.census.gov/quickfacts/fact/csv/{code}"

    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"'
    }

    response = requests.get(url, headers=headers)
    
    with open(os.path.join(folder_path,f"{geoid}.csv"), "wb") as f:
        f.write(response.content)

# # read state data 
# with open(state_boundaries_file_path,"r") as file:
#     data = json.load(file)
#     for feat in data["features"]:
#         print(feat["properties"]["NAME"])
#         response  = fetch_metadata(feat["properties"]["NAME"], feat["properties"]["GEO_ID"].split("US")[1])
#         print(response)
#         download_csv(response["id"], response["geoid"] ,os.path.join(Path(__file__).parent,"csv_files","state"))
#         print("download done")

# parse csv and upload in the database [separate  script bcz of docker]

# download county bounty data        
with open(county_boundaries_file_path,"r") as file:
    data = json.load(file)
    for feat in data["features"]:
        print(feat["properties"]["NAME"])
        response  = fetch_metadata(feat["properties"]["NAME"], feat["properties"]["GEO_ID"].split("US")[1])
        print(response)
        if(response==None):
            continue 
        download_csv(response["id"], response["geoid"] ,os.path.join(Path(__file__).parent,"csv_files","county"))
        print("download done")



