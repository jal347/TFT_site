import sys
import json

from TFT.SummonerData import SummonerData
from TFT.MatchHistory import MatchHistory
from TFT.RadiantGraph import RadiantGraph
from TFT.RankedData import RankedData
from utils import set_key


# gets player name, region, level, rank
def get_player_stats(region, name, api_key):
    # dictionary to return
    stats = {}
    set_key(stats, "region", region)

    # new instance of SummonerData
    player = SummonerData(region, name, api_key)

    # JSON file of player_data
    player_data = player.request_data()
    # get the name
    player_name = player.get_name(player_data)
    set_key(stats, "name", player_name)
    # get the level
    level = player.get_player_level(player_data)
    set_key(stats, "level", level)

    summoner_id = player.get_summoner_id(player_data)

    # new instance of ranked data
    league = RankedData(region, summoner_id, api_key)
    # get the rank of the player
    league_data = league.request_league()
    rank = league.get_rank(league_data)
    set_key(stats, "rank", rank)

    return stats


