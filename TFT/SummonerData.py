import requests


class SummonerData:

    def __init__(self, region, summoner_name, api_key):
        self.region = region
        self.summoner_name = summoner_name
        self.api_key = api_key

    # takes basic account ID from riot for tft and returns a json file that has an overview of the summoner data
    def request_data(self):
        # Create the URL to get JSON file with data
        url = "https://" + self.region + ".api.riotgames.com/tft/summoner/v1/summoners/by-name/" + self.summoner_name\
              + "?api_key=" + self.api_key

        response = requests.get(url)
        return response.json()

    # takes the JSON file from requestData and returns the Player Level
    def get_player_level(self, file):
        # gets the summoner level
        level = file['summonerLevel']
        return level

    # takes the JSON file from requestData and return the PUUID
    def get_puuid(self, file):
        # gets the unique puuid
        puuid = file['puuid']
        return puuid

    # gets a list of all the challengers (ID, NAME, LP)
    def get_challengers(self):
        challengers = []
        keys = ['summonerId', 'summonerName', 'leaguePoints']
        # url for challenger data
        url = "https://" + self.region + ".api.riotgames.com/tft/league/v1/challenger?api_key=" + self.api_key

        response = requests.get(url)
        data = response.json()

        # populate challengers list with summonerID and summonerName
        [challengers.append(list(map(challenger.get, keys))) for challenger in data['entries']]

        return challengers

    def get_summoner_id(self, file):
        summoner_id = file['id']
        return summoner_id

    def get_name(self, file):
        name = file['name']
        return name
