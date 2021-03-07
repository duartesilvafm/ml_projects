import pandas as pd
import numpy as np


def read_data(id_one, id_two, data_tag, series, data):

    if series == False:

        for x in np.arange(id_one, id_two + 1):

            data = data.append(pd.read_json(str(x) + data_tag + ".json"), ignore_index=True)

    else:

        for x in np.arange(id_one, id_two + 1):

            xdict = pd.read_json(str(x) + data_tag + ".json", typ="series")

            xdata = pd.DataFrame({str(x): xdict})

            data[str(x)] = xdata[str(x)]

    return data


first_id = 2019283
second_id = 2019377
third_id = 2019613
fourth_id = 2019641
fifth_id = 2021587
sixth_id = 2021711
seventh_id = 2025053
eigth_id = 2025148

lineup_data = pd.read_json("2019282_Lineups.json")

lineup_data = read_data(first_id, second_id, "_Lineups", False, lineup_data)

lineup_data = read_data(third_id, fourth_id, "_Lineups", False, lineup_data)

lineup_data = read_data(fifth_id, sixth_id, "_Lineups", False, lineup_data)

lineup_data = read_data(seventh_id, eigth_id, "_Lineups", False, lineup_data)

matchID_list = np.unique(lineup_data["MatchID"].to_list())

hometeam_array = lineup_data["Teams"].apply(
    lambda d: d["TeamID"] if d["TeamPosition"] == "Home" else 0).to_numpy()
hometeam_list = np.delete(hometeam_array, np.where(hometeam_array == 0)).tolist()

awayteam_array = lineup_data["Teams"].apply(
    lambda d: d["TeamID"] if d["TeamPosition"] == "Away" else 0).to_numpy()
awayteam_list = np.delete(awayteam_array, np.where(awayteam_array == 0)).tolist()

playershome_array = lineup_data["Teams"].apply(
    lambda d: d["Players"] if d["TeamPosition"] == "Home" else 0).to_numpy()
playershome_list = np.delete(playershome_array, np.where(playershome_array == 0)).tolist()

playersaway_array = lineup_data["Teams"].apply(
    lambda d: d["Players"] if d["TeamPosition"] == "Away" else 0).to_numpy()
playersaway_list = np.delete(playersaway_array, np.where(playersaway_array == 0)).tolist()

lineup_dict = {"MatchID": matchID_list, "HomeTeam": hometeam_list, "AwayTeam": awayteam_list,
               "PlayersHome": playershome_list, "PlayersAway": playersaway_list}
lineup_data = pd.DataFrame(data=lineup_dict)

lineup_data

lineup_data.to_csv("lineup_data.csv")


matchdata_dict = pd.read_json("2019282_MatchData.json", typ="series")

match_data = pd.DataFrame({'2019282': matchdata_dict})

match_data = read_data(first_id, second_id, "_MatchData", True, match_data)

match_data = read_data(third_id, fourth_id, "_MatchData", True, match_data)

match_data = read_data(fifth_id, sixth_id, "_MatchData", True, match_data)

match_data = read_data(seventh_id, eigth_id, "_MatchData", True, match_data).transpose()

match_data


match_data.to_csv("match_data.csv")

matchinfo_dict = pd.read_json("2019282_MatchInfo.json", typ="series")

matchinfo_data = pd.DataFrame({'2019282': matchinfo_dict})

matchinfo_data = read_data(first_id, second_id, "_MatchInfo", True, matchinfo_data)

matchinfo_data = read_data(third_id, fourth_id, "_MatchInfo", True, matchinfo_data)

matchinfo_data = read_data(fifth_id, sixth_id, "_MatchInfo", True, matchinfo_data)

matchinfo_data = read_data(seventh_id, eigth_id, "_MatchInfo", True, matchinfo_data).transpose()

matchinfo_data

matchinfo_data.to_csv("matchinfo_data.csv")


phases_data = pd.read_json("2019282_Phases.json")

phases_data = read_data(first_id, second_id, "_Phases", False, phases_data)

phases_data = read_data(third_id, fourth_id, "_Phases", False, phases_data)

phases_data = read_data(fifth_id, sixth_id, "_Phases", False, phases_data)

phases_data = read_data(seventh_id, eigth_id, "_Phases", False, phases_data)

phases_data

phases_data.to_csv("phases_data.csv")
