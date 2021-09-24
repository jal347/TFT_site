import requests


class RankedData:
    def __init__(self, region, summoner_id, api_key):
        self.region = region
        self.summoner_id = summoner_id
        self.api_key = api_key

    # takes basic account ID from riot for tft and returns a json file that has an overview of the summoner league
    def request_league(self):
        # Create the URL to get JSON file with data
        url = "https://" + self.region + ".api.riotgames.com/tft/league/v1/entries/by-summoner/" + self.summoner_id + "?api_key=" \
              + self.api_key

        response = requests.get(url)
        return response.json()

    # get the rank of the summoner from the data
    def get_rank(self, file):
        rank = "unranked"
        if len(file) == 0:
            return rank
        # checks if the list has 2 values
        elif len(file) == 1:
            return rank
        else:
            if file[1].get('tier') is None:
                return rank
            rank = file[1].get('tier')
            return rank
