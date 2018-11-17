import sys
import json
from espnCrawler import return_leaders

js_input = sys.argv[1]
player = return_leaders(js_input)[0]["player"]

with open("./logs.json", "w+") as outfile:
    json.dump({"arg": js_input}, outfile)

print(player)
sys.stdout.flush()

