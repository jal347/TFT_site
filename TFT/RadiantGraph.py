import sys
import json
import time
from statistics import mean
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from .SummonerData import SummonerData
from .MatchHistory import MatchHistory
from utils import set_key


class RadiantGraph:

    def get_image(self, path):
        return OffsetImage(plt.imread(path), zoom=.2)

    """
    Takes a list of challenger data and takes the last 2 games they platey. Graph the average placement/winrate
    challenger[id, name, lp]
    
    """

    def make_radiant_data(self, challengers, region, api_key):
        ranked = 1100
        radiant_data = {}
        for challenger in challengers:
            # gets the challenger name w/o spaces
            summoner_name = challenger[1].replace(" ", "")

            # gets the puuid
            player = SummonerData(region, summoner_name, api_key)
            player_data = player.request_data()
            puuid = player.get_puuid(player_data)

            # get the last 50 matches
            matches = MatchHistory(puuid, region, api_key)
            match_ids = matches.get_match_id(str(2))

            # loop through the 50 matches to find placement and radiant item and put it into a dictionary
            for matchID in match_ids:

                time.sleep(1.8)
                match_data = matches.get_match(matchID)

                if matches.get_queue_id(match_data) == 0:
                    if match_data['status']['status_code'] == 503:
                        time.sleep(1)
                        matches.get_match(matchID)
                    else:
                        """ USED FOR DEBUGGING
                        print("this is matchID:" + matchID)
                        fp = open("debug.json", "a")
                        # file to dump match details
                        # dump the file for reading purposes
                        json.dump(match_data, fp, indent=4)
                        """
                        continue
                else:
                    # check queue id
                    if matches.get_queue_id(match_data) == ranked:
                        radiant = matches.get_radiant(match_data)
                        if radiant != -1:
                            placement = matches.get_placement(match_data)
                            radiant_data = set_key(radiant_data, radiant[0], placement)
                    else:
                        continue
        return radiant_data

    def make_radiant_graph(self, file):
        dict_data = json.load(file)
        # radiant item
        itemName = []
        x = []
        y = []
        paths = []

        for item in dict_data:
            y.append(len(dict_data[item]))
            # finds average placement for radiant item
            placements = [float(i) for i in dict_data[item]]
            x.append(mean(placements))

            # open the items folder
            fp = open("C:/Users/PCM2020-2/PycharmProjects/TFT_Project/RIOT TFT/items.json", "r")
            # search radiant item used and get the name
            fp = json.load(fp)

            for data in fp:
                if data['id'] == int(item):
                    itemName.append(data['name'])
                    paths.append("C:/Users/PCM2020-2/PycharmProjects/TFT_Project/RIOT TFT/items/" + item + ".png")

        print(x)
        print(y)
        print(itemName)

        fig, ax = plt.subplots(figsize=(16, 9))
        ax.scatter(x, y)

        for x0, y0, path in zip(x, y, paths):
            ab = AnnotationBbox(self.get_image(path), (x0, y0), frameon=False)
            ax.add_artist(ab)

        plt.show()
