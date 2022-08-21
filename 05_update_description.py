import json
from bungieapi import BungieApi
from config import API_KEY, CLIENT_ID, CLIENT_SECRET

api = BungieApi(API_KEY, CLIENT_ID, CLIENT_SECRET)

MOTTO = "Sanctuary for all, community for all."
ABOUT = """
Welcome to D2Sanctuary!

Are you deaf, mute, or have social anxiety? Please read the following.

You can get a lot done in the world of Destiny while playing solo, but what about all that sweet loot that you miss out on when you need a pre-made fireteam? You may want to hunt for the exotics in Zero Hour, The Whisper, or reach Legend in Crucible, etc. There are also Iron Banners, Dungeons, Nightfalls, and Raids. You may not think so, but we all have something in common. We know the disappointment when we see mics as a requirement.

Here at D2Sanctuary, we want to be a home for the voiceless guardians. Where we can tackle quests, complete dungeons, and raid together.

Mics are something that will never be a requirement for our members.

Join and help us build a community for the guardians who can't be heard.
discord.gg/d2sanctuary
"""


with open("users.json", "r") as f:
    userList = json.load(f)

for user in userList:
    membershipInfo = api.getMembershipDataForCurrentUser(userList[user]["access_token"])
    membershipType = membershipInfo["destinyMemberships"][0]["membershipType"]
    membershipId = membershipInfo["destinyMemberships"][0]["membershipId"]

    clanInfo = api.findClanForMembership(membershipType, membershipId)
    if clanInfo["totalResults"] != 1:
        print("ERROR WITH %d %d %s: No clans found. Ignoring" % (user, membershipType, membershipId))
        continue
    clan = clanInfo["results"][0]
    l = api.editClanInfo(
        clan["group"]["groupId"],
        userList[user]["access_token"],
        {
            "name": None,
            "theme": None,
            "avatarImageIndex": None,
            "tags": None,
            "isPublic": None,
            "membershipOption": None,
            "isPublicTopicAdminOnly": None,
            "allowChat": None,
            "chatSecurity": None,
            "callsign": None,
            "locale": None,
            "homepage": None,
            "enableInvitationMessagingForAdmins": None,
            "defaultPublicity": None,
            "about": ABOUT,
            "motto": MOTTO
        }
    )
    print(l)


