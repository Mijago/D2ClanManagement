import time
from typing import Dict
import requests

API_ROOT_PATH = "https://www.bungie.net/Platform"


class BungieApi:
    __HEADERS: Dict[str, str]

    def __init__(self, api_key: str, clientId: str, clientSecret: str):
        self.__HEADERS = {"X-API-Key": api_key}
        self.clientId = str(clientId)
        self.clientSecret = str(clientSecret)
        pass

    def getProfile(self, membershipType, destinyMembershipId, components=[200]):
        params = {}
        if components is not None: params["components"] = components

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}', headers=self.__HEADERS, params=params)

        return (api_call.json())['Response']

    def getClanMembers(self, groupId):
        api_call1 = requests.get(f'{API_ROOT_PATH}/GroupV2/{groupId}/Members/', headers=self.__HEADERS, params={"page": 0})
        return api_call1.json()['Response']["results"]

    def getAccountStats(self, membershipType, destinyMembershipId):
        params = {}

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats', headers=self.__HEADERS, params=params)

        return (api_call.json())['Response']

    def getActivities(self, membershipType, destinyMembershipId, characterId, page=0, count=250, mode=None):
        params = {}
        if page is not None: params["page"] = page
        if count is not None: params["count"] = count
        if mode is not None: params["mode"] = mode

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/', headers=self.__HEADERS, params=params)
        json_ = (api_call.json())
        if ("Response" not in json_):
            print(json_)
        return json_['Response']

    def getPGCR(self, activityId):
        params = {}

        try:
            api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/Stats/PostGameCarnageReport/{activityId}/', headers=self.__HEADERS, params=params, timeout=(10, 10))
        except:
            return None
        return (api_call.json())['Response']

    def getItem(self, itemReferenceId):
        pass

    def findClanForMembership(self, membershipType, membershipId):
        api_call = requests.get(f'{API_ROOT_PATH}/GroupV2/User/{membershipType}/{membershipId}/0/1/',
                                headers=self.__HEADERS
                                )
        return api_call.json()['Response']

    def getMembershipDataForCurrentUser(self, token):
        header = {
            "X-API-Key": self.__HEADERS["X-API-Key"],
            "authorization": "bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        api_call = requests.get(f'{API_ROOT_PATH}/User/GetMembershipsForCurrentUser/',
                                headers=header
                                )
        return api_call.json()['Response']

    def generateKeysFromAuthCode(self, code, grant_type="authorization_code"):
        body = "grant_type=%s&%s=%s&client_id=%s&client_secret=%s" % (
            grant_type,
            "code" if grant_type == "authorization_code" else "refresh_token",
            str(code),
            self.clientId,
            self.clientSecret
        )

        header = {
            "X-API-Key": self.__HEADERS["X-API-Key"],
            "Content-Type": "application/x-www-form-urlencoded"
        }

        r = requests.post("https://www.bungie.net/Platform/App/OAuth/Token/", headers=header, data=body).json()
        if "access_token" not in r:
            print(r)
            return None

        r["refresh_expires_at"] = time.time() + r["refresh_expires_in"]

        return r  # access_token refresh_expires_in membership_id

    def getGroupMembers(self, groupId):

        api_call = requests.get(f'{API_ROOT_PATH}/GroupV2/{groupId}/Members/',
                                headers=self.__HEADERS
                                )
        return api_call.json()['Response']
        pass
