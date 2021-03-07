import pandas as pd
import numpy as np
from datetime import datetime
from functools import reduce

match_data = pd.read_csv("match_data.csv")
phases_data = pd.read_csv("phases_data.csv")
matchinfo_data = pd.read_csv("matchinfo_data.csv")
data = pd.read_csv("final_data.csv")

first_id = 2019282
second_id = 2019377
third_id = 2019613
fourth_id = 2019641
fifth_id = 2021587
sixth_id = 2021711
seventh_id = 2025053
eigth_id = 2025148

season_ids = {}

for id in np.arange(first_id, second_id + 1):
    season_ids[id] = "Season_1"

for id in np.arange(third_id, fourth_id + 1):
    season_ids[id] = "Season_1"

for id in np.arange(fifth_id, sixth_id + 1):
    season_ids[id] = "Season_2"

for id in np.arange(seventh_id, eigth_id + 1):
    season_ids[id] = "Season_3"


def get_last_matches(team_id, match_id, data, season_id=season_ids, n=3):
    """
    Return last three match ids for a team

    Parameter specification:
    team_id: int specifying the team_id
    match_id: int specifying the match_id
    data: pandas dataframe to retrive the last three matches
    """

    # Filter data by team id
    team_data = data[data["Team_ID"] == team_id].reset_index()

    # Filter the data by the last three ids
    up_to_match = team_data[:team_data[(team_data["Match_ID"] == match_id)].index[0]]
    up_to_match = up_to_match[up_to_match["Team_ID"] == team_id]
    last_three = list(up_to_match[-4:][:3]["Match_ID"].values)

    # Only return if there were three last matches in that season
    if len(last_three) == 3:
        if season_id[last_three[0]] == season_id[last_three[1]] == season_id[last_three[2]]:
            return last_three
    else:
        return None


def get_shot_stats(team_id, match_id, data=data):
    """
    Return list with shot stats

    Parameter specification:
    team_id: int indicating the team_id
    match_id: int indicating the match_id
    data: pandas dataframe with the shot data
    """

    # Dictionary for shot stats
    shot_stats = {"Match_ID": match_id, "Team_ID": team_id}

    # Get the three last match_ids
    last_three = get_last_matches(team_id, match_id, data)

    # Check whether there are three matches
    if last_three != None:

        # Filter dataset by match_ids and team_id
        data_last_three = data[(data["Match_ID"].isin(last_three)) & (data["Team_ID"] == team_id)]

        # Get shots on target
        ontarget = sum(data_last_three["Shots_OnTarget"]) / sum(data_last_three["Shots"])
        shot_stats["OnTarget_%"] = ontarget

        # Get short shots
        short = sum(data_last_three["Shots_St"]) / sum(data_last_three["Shots"])
        shot_stats["Short_%"] = short

    return shot_stats


def get_tackle_stats(team_id, match_id, data=data):
    """
    Return list with tackle stats

    Parameter specification:
    team_id: int indicating the team_id
    match_id: int indicating the match_id
    data: pandas dataframe with tackle data
    """

    # Dictionary for shot stats
    tackle_stats = {"Match_ID": match_id, "Team_ID": team_id}

    # Get the three last match_ids
    last_three = get_last_matches(team_id, match_id, data)

    # Check whether there are three matches
    if last_three != None:

        # Filter dataset by match_ids and team_id
        data_last_three = data[(data["Match_ID"].isin(last_three)) & (data["Team_ID"] == team_id)]

        # Successful tackle to attempted tackles
        tackles_suc = sum(data_last_three["Tack_Succ"]) / sum(data_last_three["Tack_Att"])
        tackle_stats["Tackles_Successful%"] = tackles_suc

        # Dummy more than 11 tackles
        aggressiveness = list(data_last_three["Tack_Att"].apply(lambda d: 1 if d >= 11 else 0))
        if sum(aggressiveness) >= 2:
            tackle_stats["Aggressiveness"] = 1
        else:
            tackle_stats["Aggressiveness"] = 0

    return tackle_stats


def get_foul_stats(team_id, match_id, data=data):
    """
    Return list with foul stats

    Parameter specification:
    team_id: int indicating the team_id
    match_id: int indicating the match_id
    data: pandas dataframe with foul data
    """

    # Dictionary for foul stats
    foul_stats = {"Match_ID": match_id, "Team_ID": team_id}

    # Get the three last match_ids
    last_three = get_last_matches(team_id, match_id, data)

    # Check whether there are three matches
    if last_three != None:

        # Filter dataset by match_ids and team_id
        data_last_three = data[(data["Match_ID"].isin(last_three)) & (data["Team_ID"] == team_id)]

        # Get total fouls
        total_fouls = sum(data_last_three["Fouls"])
        foul_stats["Total_Fouls"] = total_fouls

        # Get yellow cards
        ycs = sum(data_last_three["Yellow_Cards"])
        foul_stats["Yellow_Cards"] = ycs

        # Yellow card + Red Cards / Total Fouls
        ratio = (ycs + sum(data_last_three["Red_Cards"])) / total_fouls
        foul_stats["Cards/Fouls"] = ratio

    return foul_stats


def get_fk_stats(team_id, match_id, data=data):
    """
    Return list with freekick stats

    Parameter specification:
    team_id: int indicating the team_id
    match_id: int indicating the match_id
    data: pandas dataframe with freekick data
    """

    # Dictionary for shot stats
    fk_stats = {"Match_ID": match_id, "Team_ID": team_id}

    # Get the three last match_ids
    last_three = get_last_matches(team_id, match_id, data)

    # Check whether there are three matches
    if last_three != None:

        # Filter dataset by match_ids and team_id
        data_last_three = data[(data["Match_ID"].isin(last_three)) & (data["Team_ID"] == team_id)]

        # Get total freekicks
        total_fk = sum(data_last_three["FK_Tot"])
        fk_stats["Total_FKs"] = total_fk

        # Get short free kick ratio
        short_fk = sum(data_last_three["FK_St"]) / sum(data_last_three["FK_Tot"])
        fk_stats["Short_FKs"] = short_fk

    return fk_stats


def get_save_stats(team_id, match_id, data=data):
    """
    Return list with saves stats

    Parameter specification:
    team_id: int indicating the team_id
    match_id: int indicating the match_id
    data: pandas dataframe with saves data
    adj_data: pandas dataframe with shots data
    """

    # Dictionary for saves stats
    saves_stats = {"Match_ID": match_id, "Team_ID": team_id}

    # Get the three last match_ids
    last_three = get_last_matches(team_id, match_id, data)

    # Check whether there are three matches
    if last_three != None:

        # Filter dataset by match_ids and team_id
        data_last_three = data[(data["Match_ID"].isin(last_three)) & (data["Team_ID"] == team_id)]
        conceded_data = data[(data["Match_ID"].isin(last_three))
                             & (data["Team_ID"] != team_id)]

        # Total saves
        total_saves = sum(data_last_three["Saves"])
        saves_stats["Total_Saves"] = total_saves

        # Saves to shots ratio
        ratio = total_saves / sum(conceded_data["Shots"])
        saves_stats["Saves/Shots"] = ratio

    return saves_stats


def get_corner_stats(team_id, match_id, data=data):
    """
    Return list with corner stats

    Parameter specification:
    team_id: int indicating the team_id
    match_id: int indicating the match_id
    data: pandas dataframe with corner data
    """

    # Dictionary for corner stats
    corner_stats = {"Match_ID": match_id, "Team_ID": team_id}

    # Get the three last match_ids
    last_three = get_last_matches(team_id, match_id, data)

    # Check whether there are three matches
    if last_three != None:

        # Filter dataset by match_ids and team_id
        data_last_three = data[(data["Match_ID"].isin(last_three)) & (data["Team_ID"] == team_id)]

        # Successful corners
        succ_corners = sum(data_last_three["Corners"] - data_last_three["Corner_Unsuccessful"])
        total_corners = sum(data_last_three["Corners"])
        corner_stats["Succ_Ratio"] = succ_corners / total_corners

    return corner_stats


def get_pass_stats(team_id, match_id, data=data):
    """
    Return dictionary with corner stats

    Parameter specification:
    team_id: int indicating the team_id
    match_id: int indicating the match_id
    data: pandas dataframe with passes data
    """

    # Dictionary for passes stats
    passes_stats = {"Match_ID": match_id, "Team_ID": team_id}

    # Get the three last match_ids
    last_three = get_last_matches(team_id, match_id, data)

    # Check whether there are three matches
    if last_three != None:

        # Filter dataset by match_ids and team_id
        data_last_three = data[(data["Match_ID"].isin(last_three)) & (data["Team_ID"] == team_id)]

        # Count total passes
        pass_atts = sum(data_last_three["Pass_Att"])
        passes_stats["Passes_Att"] = pass_atts

        # Passes completed %
        comp_per = sum(data_last_three["Pass_Comp"]) / sum(data_last_three["Pass_Att"])
        passes_stats["Pass_Comp%"] = comp_per

    return passes_stats


def get_other_stats(team_id, match_id, data=data):
    """
    Return dictionary with other stats

    Parameter specification:
    team_id: int indicating the team_id
    match_id: int indicating the match_id
    data: pandas dataframe with data
    """

    # Dictionary for other stats
    other_stats = {"Match_ID": match_id, "Team_ID": team_id}

    # Get the three last match_ids
    last_three = get_last_matches(team_id, match_id, data)

    # Check whether there are three matches
    if last_three != None:

        # Filter dataset by match_ids and team_id
        data_last_three = data[(data["Match_ID"].isin(last_three)) & (data["Team_ID"] != team_id)]

        # Count total passes
        blocked_shots = sum(data_last_three["Shots_Blocked"])
        other_stats["Shots_Blocked"] = blocked_shots

        # Passes completed %
        conceded_corners = sum(data_last_three["Corners"])
        other_stats["Conceded_Corners"] = conceded_corners

    return other_stats


# Process phases data

phases_data = phases_data[phases_data["Status"] == "['Current', 'Completed']"]
scores_data = phases_data[["AwayScore", "HomeScore", "MatchID"]]
scores_data = scores_data.groupby(by="MatchID").sum().reset_index()
team_data = match_data[["MatchID", "HomeTeamID", "AwayTeamID"]]
scores_data = scores_data.merge(team_data, on="MatchID", how="left")

winners = []

for x in scores_data.index:
    if scores_data.iloc[x]["AwayScore"] > scores_data.iloc[x]["HomeScore"]:
        winners.append(scores_data.iloc[x]["AwayTeamID"])
    elif scores_data.iloc[x]["HomeScore"] > scores_data.iloc[x]["AwayScore"]:
        winners.append(scores_data.iloc[x]["HomeTeamID"])
    else:
        winners.append("Draw")

scores_data["Winner"] = winners

knockout_dummy = []

for x in match_data.index:
    if match_data.iloc[x]["Type"] != "Group":
        knockout_dummy.append(1)
    else:
        knockout_dummy.append(0)

scores_data["KnockOut"] = knockout_dummy


def get_wins(match_id, team_id, data=scores_data, adj_data=data):
    """
    Returns number of wins by team for the three matches before the indicated match_id

    Parameter specification:
    match_id: int indicating the match id
    team_id: int indicating the team id
    data: pandas dataframe with scores data
    adj_data: pandas dataframe to extract the last three matches
    """

    # create dictionary with wins dummy
    wins_dic = {"MatchID": match_id, "TeamID": team_id}

    # last three matches
    last_three = get_last_matches(team_id, match_id, adj_data)

    if last_three != None:

        # filter dataset by these three
        data = data[data["MatchID"].isin(last_three)]

        # filter dataset by the team_id
        data = data[(data["HomeTeamID"] == team_id) | (data["AwayTeamID"] == team_id)]

        # count wins
        one_win = 0 if sum(data["Winner"] == team_id) != 1 else 1
        two_win = 0 if sum(data["Winner"] == team_id) != 2 else 1
        three_win = 0 if sum(data["Winner"] == team_id) != 3 else 1

        # create keys
        wins_dic["One_Win"] = one_win
        wins_dic["Two_Win"] = two_win
        wins_dic["Three_Win"] = three_win

    return wins_dic


match_data["Time"] = match_data["MatchDateUTC"].apply(lambda d: d[:10] + " " + d[11:-1])

# Transfrom dates

match_data["Time"] = match_data["Time"].apply(lambda d: datetime.strptime(d, "%Y-%m-%d %H:%M:%S"))
match_data = match_data.sort_values("Time", ascending=True)


def last_matches(team_id, match_id, data=match_data):
    """
    Returns an intenger indicating the number of matches the team played before

    team_id: intenger indicating the team id
    match_id: integer indicating the match id
    data: pandas dataframe with match_data
    """

    # Get competition_id
    competition_id = data[data["MatchID"] == match_id]["CompetitionID"].values[0]

    # Filter by competition_id
    comp_data = data[data["CompetitionID"] == competition_id]

    # Filter dataset by team_id
    team_data = comp_data[(comp_data["HomeTeamID"] == team_id) |
                          (comp_data["AwayTeamID"] == team_id)]

    # Order dataset by time
    team_data = team_data.sort_values("Time", ascending=True).reset_index()

    # Get all the data
    upto_match = team_data[:team_data[team_data["MatchID"] == match_id].index[0]]

    # Get number of matches
    matches = len(upto_match)

    return matches


home_matches = []
away_matches = []

for row in match_data.iterrows():
    for team in ["HomeTeamID", "AwayTeamID"]:
        team_id = row[1][team]
        match_id = row[1]["MatchID"]
        match = last_matches(int(team_id), match_id)
        if team == "HomeTeamID":
            home_matches.append(match)
        else:
            away_matches.append(match)

match_data["BeforeHome"] = home_matches
match_data["BeforeAway"] = away_matches

train_data = match_data[(match_data["BeforeHome"] >= 3) | (
    match_data["BeforeAway"] >= 3)][["MatchID", "HomeTeamID", "AwayTeamID"]]
train_data.to_csv("ids_teams.csv")

variables = []

for row in train_data.iterrows():
    for set in [["HomeTeamID", "AwayTeamID"], ["AwayTeamID", "HomeTeamID"]]:
        team_id = row[1][set[0]]
        opp_id = row[1][set[1]]
        match_id = row[1]["MatchID"]
        shot_stats = get_shot_stats(team_id, match_id)
        corner_stats = get_corner_stats(team_id, match_id)
        fk_stats = get_fk_stats(team_id, match_id)
        pass_stats = get_pass_stats(team_id, match_id)
        foul_stats = get_foul_stats(opp_id, match_id)
        tackle_stats = get_tackle_stats(opp_id, match_id)
        save_stats = get_save_stats(opp_id, match_id)
        other_stats = get_other_stats(opp_id, match_id)
        stats = {**shot_stats, **corner_stats, **fk_stats, **
                 pass_stats, **foul_stats, **tackle_stats, **save_stats, **other_stats}
        variables.append(stats)

data_df = pd.DataFrame(variables)

scores_data = scores_data[scores_data["MatchID"].isin(train_data["MatchID"])]

matchids = list(scores_data["MatchID"])
hometeams = list(scores_data["HomeTeamID"])
awayteams = list(scores_data["AwayTeamID"])
homescore = list(scores_data["HomeScore"])
awayscore = list(scores_data["AwayScore"])
knockout = list(scores_data["KnockOut"])

y_data = []
matchidsdf = matchids * 2
teamsdf = hometeams + awayteams
scoresdf = homescore + awayscore
knockoutsdf = knockout * 2
y_data.append(matchidsdf)
y_data.append(teamsdf)
y_data.append(scoresdf)
y_data.append(knockoutsdf)
ydf = pd.DataFrame(y_data).transpose()
ydf.columns = ["Match_ID", "Team_ID", "Goals", "Knockout"]

final_data = pd.merge(ydf, data_df, on=["Match_ID", "Team_ID"])
final_data = final_data.rename(columns={"Total_Fouls": "Opp_Total_Fouls", "Yellow_Cards": "Opp_Yellow_Cards", "Cards/Foulds": "Opp_Cards/Fouls",
                                        "Tackles_Successful%": "OppTackles_Successful%", "Aggressiveness": "Opp_Aggressiveness",
                                        "Total_Saves": "Opp_Total_Saves", "Saves/Shots": "Opp_Saves/Shots", "Shots_Blocked": "Opp_Shots_Blocked",
                                        "Conceded_Corners": "Opp_Conceded_Corners"})
final_data.to_csv("model_data.csv")

# match_data["HomeTeamLastMatches"] = match_data
