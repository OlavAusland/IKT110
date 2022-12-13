import requests
import os 
import json
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# API key from steam:
try:
    api_key =  os.getenv("API_KEY")
except KeyError:
    print("Unable to find the steam api key in the environment variable API_KEY")
    exit(0)

print(api_key)

# =========================
print("cwd: ", os.getcwd())

img_sizes = ["sb.png"] # "sb.png" "lg.png", "full.png", "vert.jpg"
heroes_r = requests.get("http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1?key={}".format(api_key))
heroes = heroes_r.json()["result"]["heroes"]

for hero in heroes:
    hero["api_name"] = str(hero["name"]).replace("npc_dota_hero_", "") 
    hero["name"] = str(hero["name"]).replace("npc_dota_hero_", "").replace("_", " ").title()
    # hero["name"] = str(hero["name"].replace("_", " ").title())

# Save heroes json
with open("../doracle/data/heroes.json", "w") as fp:
    json.dump(heroes, fp)

print("[OK] Save heroes.json")


# Download images
for img_size in img_sizes:
    f_ext = img_size.split(".")[1]
    f_size = img_size.split(".")[0]
    save_folder = "../doracle/static/img/avatar-{}".format(f_size)

    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)

    for hero in tqdm(heroes, desc="{}".format(img_size)):

        img = requests.get("http://cdn.dota2.com/apps/dota2/images/heroes/{}_{}".format(hero["api_name"], img_size))

        with open("{}/{}.{}".format(save_folder, hero["id"], f_ext), "wb") as fp:
            fp.write(img.content)

print('[OK] Save avatars')

print("Done")
