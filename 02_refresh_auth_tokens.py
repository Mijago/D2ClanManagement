import json

from bungieapi import BungieApi
from config import API_KEY, CLIENT_ID, CLIENT_SECRET

api = BungieApi(API_KEY, CLIENT_ID, CLIENT_SECRET)

with open("users.json", "r") as f:
    lst = json.load(f)

with open("users.old.json", "w") as f:
    json.dump(lst, f, indent=2)

for l in lst:
    r = api.generateKeysFromAuthCode(lst[l]["refresh_token"], grant_type="refresh_token")
    if r is not None:
        lst[l] = r
    else:
        print("COULD NOT UPDATE ID=%d" % l)
        print(l)

with open("users.json", "w") as f:
    json.dump(lst, f, indent=2)
