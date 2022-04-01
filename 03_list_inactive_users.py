import json
from datetime import datetime
from bungieapi import BungieApi
from config import API_KEY, CLIENT_ID, CLIENT_SECRET

MAX_OFFLINE_DAYS = 60

api = BungieApi(API_KEY, CLIENT_ID, CLIENT_SECRET)

with open("users.json", "r") as f:
    userList = json.load(f)

todoGroups = []

for user in userList:
    membershipInfo = api.getMembershipDataForCurrentUser(userList[user]["access_token"])
    membershipType = membershipInfo["destinyMemberships"][0]["membershipType"]
    membershipId = membershipInfo["destinyMemberships"][0]["membershipId"]

    clanInfo = api.findClanForMembership(membershipType, membershipId)
    if clanInfo["totalResults"] != 1:
        print("ERROR WITH %d %d %s: No clans found. Ignoring" % (user, membershipType, membershipId))
        continue
    clan = clanInfo["results"][0]

    todoGroups.append((membershipType, membershipId, clan["group"]["groupId"], clan["group"]["name"]))

formatStr = "{:<9}\t{:<30}\t{:<20}\t{:<5}"
for todo in todoGroups:
    groupId = todo[2]
    users = api.getGroupMembers(groupId)["results"]
    print("Handling Clan:\t'%s'" % todo[3])
    print(formatStr.format("GroupId", "UserName", "Last Seen", "Gone Days"))

    now = datetime.now()
    users = sorted(users, key=lambda user: datetime.fromtimestamp(int(user["lastOnlineStatusChange"])))

    for user in users:
        dt = datetime.fromtimestamp(int(user["lastOnlineStatusChange"]))
        goneDays = (now - dt).days
        if goneDays > MAX_OFFLINE_DAYS:
            userName = user["destinyUserInfo"]["LastSeenDisplayName"]
            print(formatStr.format(groupId, userName, str(dt), goneDays))