import requests
import json


class MatchHistory:

    # match history uses puuid to search in Riot API
    def __init__(self, puuid, region, api_key):
        self.puuid = puuid
        if region == "na1":
            self.region = "americas"
        elif region == "euw1":
            self.region = "europe"
        else:
            self.region = "asia"
        self.api_key = api_key

    # gets the # of unique matchIDs using the player's puuid
    # number of games defaulted at 20
    def get_match_id(self, games=str(20)):
        # create URL for json file for matchIDs
        url = "https://" + self.region + ".api.riotgames.com/tft/match/v1/matches/by-puuid/" \
              + self.puuid + "/ids?count=" + games + "&api_key=" + self.api_key
        # request URL and then get the json file
        response = requests.get(url)
        response = response.json()
        # returns the list of match ids of the previous # of games
        return response

    # gets the json file for the match results
    def get_match(self, match_id):
        # create url to get a json file for the match
        url = "https://americas.api.riotgames.com/tft/match/v1/matches/" + match_id + "?api_key=" + self.api_key
        # request URL and then get the json file
        response = requests.get(url)
        response = response.json()
        return response

    # gets the player's placement using the json results file
    def get_placement(self, file):
        # placement player got in the match -1 if player doesnt exist
        placement = -1

        # loop through each participant's data
        for participant in file['info']['participants']:
            # find the participant using puuid
            if participant['puuid'] == self.puuid:
                # returns the player's placement
                placement = participant['placement']
                return placement
            else:
                continue
        return placement

    # returns the queue id
    def get_queue_id(self, file):
        if file.get('info') is None:
            return 0
        else:
            return file.get('info').get('queue_id', 0)

    # gets the radiant item you used in your game
    def get_radiant(self, file):
        # if the item number is over 2000 it is a radiant item
        is_radiant = 2000
        # radiant item
        radiant = -1

        # loop through each participant
        for participant in file['info']['participants']:
            # find the participant using puuid
            if participant['puuid'] == self.puuid:
                # loop through all the units participant used
                for unit in participant['units']:
                    # loop through items in each unit
                    for item in unit['items']:
                        # look for radiant item
                        if item > is_radiant:
                            radiant = item

        # open the items folder
        items = open("C:/Users/PCM2020-2/PycharmProjects/TFT_Project/RIOT TFT/items.json", "r")
        # search radiant item used and get the name
        items = json.load(items)

        if radiant == -1:
            return -1

        for item in items:
            if item['id'] == radiant:
                radiant_item = [radiant, item['name']]

        # return the radiant item
        return radiant_item
