# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import sys
import json
import features


def main():
    print("\nType in one of the following regions to start: na1, euw1, kr\n")

    # request region, name, and APIKey so I can initilize SummonerData
    region = str(input('Enter your region: '))
    summoner_name = str(input('Enter your Summoner Name. DO NOT INCLUDE SPACES: '))
    api_key = str(input('Enter Riot APIKey: '))

    stats = features.get_player_stats(region, summoner_name, api_key)

    print("Hi " + stats['name'])
    print("Your Level is: " + str(stats['level']))
    print("Your current Rank is: " + stats['rank'])


"""
    #new instance of SummonerData
    player = SummonerData(region, summonerName, APIKey)

    #JSON file of playerData
    playerData = player.requestData()

    #get the puuid from playerData
    puuid = player.getPUUID(playerData)



    #initilize match history
    history = MatchHistory(puuid, region, APIKey)
    #get the list of matchID of the last # of games played by the player
    matchID = history.getMatchID("1")

    #print list of matchids
    print("The matchID of the last " + str(len(matchID)) + " game(s) you played is: " + str(matchID)[1:-1])

    #Using the matchID list get the match details from a player
    #make a file pointer
    fp = open("matchResult.json", "w")
    #file to dump match details
    matchResult = history.getMatch(str(matchID[0]))
    #dump the file for reading purposes
    json.dump(matchResult, fp, indent=4)

    #gets the player placement
    placement = history.getPlacement(matchResult)
    placement = "Your placement is " + str(placement)
    print(placement)



    #gets the radiant item used
    radiantItem = history.getRadiant(matchResult)
    radiantItem = "The Radiant Item you used is " + radiantItem[1]
    print(radiantItem)




    

    #open file
    file = open("./RadiantData.json", "r")
    tftGraph = RadiantGraph()
    tftGraph.makeRadiantGraph(file)
"""

"""
    THIS GETS MY RADIANT DATA 
    challengers = player.getChallengers()
    tftGraph = RadiantGraph()
    radiantData = tftGraph.makeRadiantData(challengers, region, APIKey)
    fp = open("RadiantData.json", "w")
    json.dump(radiantData, fp, indent=4)
"""

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
