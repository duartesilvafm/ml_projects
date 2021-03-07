import pandas as pd
import numpy as np
import json


def clean_keys(marks_data, marks):
    """
    Clean rows
    """

    for mark in marks_data:

        for x in list(mark):

            if x not in marks:
                del mark[x]

    return marks_data


def clean_marks(marks_data, tags):
    """
    Returns json marks file cleaned with only the appropiate instances
    """

    mark_events = []

    for mark in marks_data:

        if set(tags) & set(mark["Tags"]) != set():
            mark_events.append(mark)

    return mark_events


def get_tackles(marks, match_id, home):

    # match_id, team_id, tackles attempted, successful tackles, short successful tackles, medium successful tackles, long successful tackle

    if home == True:
        team = get_HomeTeam(match_id)

    else:
        team = get_AwayTeam(match_id)

    tack_att = 0
    tack_suc = 0
    short_tack_suc = 0
    med_tack_suc = 0
    long_tack_suc = 0

    for mark in marks:

        event_id = mark["MarkGuid"]

        if "Tackle" in mark["Tags"] and check_team(event_id, team, marks):
            tack_att += 1

            if "Successful" in mark["Attributes"]:
                tack_suc += 1

                if "Short" in mark["Attributes"]:
                    short_tack_suc += 1

                if "Medium" in mark["Attributes"]:
                    med_tack_suc += 1

                if "Long" in mark["Attributes"]:
                    long_tack_suc += 1

    tackle_stats = [match_id, team, tack_att, tack_suc, short_tack_suc, med_tack_suc, long_tack_suc]

    return tackle_stats


def get_shots(marks, match_id, home):

    if home == True:
        team = get_HomeTeam(match_id)

    else:
        team = get_AwayTeam(match_id)

    shots_tot = 0
    shots_big = 0
    shots_on = 0
    shots_off = 0
    shots_bl = 0
    shots_st = 0
    shots_med = 0

    for mark in marks:

        event_id = mark["MarkGuid"]

        if "Shot" in mark["Tags"] and check_team(event_id, team, marks):
            shots_tot += 1

            if "BigChance" in mark["Tags"]:
                shots_big += 1

            if "OnTarget" in mark["Attributes"]:
                shots_on += 1

            if "OffTarget" in mark["Attributes"]:
                shots_off += 1

            if "Medium" in mark["Attributes"]:
                shots_med += 1

            if "Short" in mark["Attributes"]:
                shots_st += 1

            if "Blocked" in mark["Attributes"]:
                shots_bl += 1

    shot_stats = [match_id, team, shots_tot, shots_big,
                  shots_on, shots_off, shots_bl, shots_st, shots_med]

    return shot_stats


def get_fk(marks, match_id, home):

    if home == True:
        team = get_HomeTeam(match_id)

    else:
        team = get_AwayTeam(match_id)

    fk_tot = 0
    fk_ind = 0
    fk_dir = 0
    fk_st = 0
    fk_med = 0
    fk_lg = 0
    fk_cross = 0
    fk_un = 0

    for mark in marks:

        event_id = mark["MarkGuid"]

        if "FreeKick" in mark["Tags"] and check_team(event_id, team, marks):
            fk_tot += 1

            if "Indirect" in mark["Attributes"]:
                fk_ind += 1

            if "Direct" in mark["Attributes"]:
                fk_dir += 1

            if "Short" in mark["Attributes"]:
                fk_st += 1

            if "Medium" in mark["Attributes"]:
                fk_med += 1

            if "Long" in mark["Attributes"]:
                fk_lg += 1

            if "Cross" in mark["Attributes"]:
                fk_cross += 1

            if "DoNotCountPass" in mark["Attributes"]:
                fk_un += 1

    data = [match_id, team, fk_tot, fk_ind, fk_dir, fk_st, fk_med, fk_lg, fk_cross, fk_un]

    return data


def get_corner(marks, match_id, home):

    if home == True:
        team = get_HomeTeam(match_id)

    else:
        team = get_AwayTeam(match_id)

    corner_tot = 0
    corner_short = 0
    corner_cross = 0
    cross_med = 0
    cross_long = 0
    cross_un = 0
    corner_shot = 0
    corner_ontarget = 0

    for mark in marks:

        event_id = mark["MarkGuid"]

        if "Corner" in mark["Tags"] and check_team(event_id, team, marks):
            corner_tot += 1

            if "Short" in mark["Attributes"]:
                corner_short += 1

            if "Cross" in mark["Attributes"]:
                corner_cross += 1

            if "Medium" in mark["Attributes"]:
                cross_med += 1

            if "Long" in mark["Attributes"]:
                cross_long += 1

            if "DoNotCountPass" in mark["Attributes"]:
                cross_un += 1

            if "Shot" in mark["Tags"]:
                corner_shot += 1

                if "OnTarget" in mark["Attributes"]:
                    corner_ontarget += 1

    data = [match_id, team, corner_tot, corner_short, corner_cross,
            cross_med, cross_long, cross_un, corner_shot, corner_ontarget]

    return data


def get_passes(marks, match_id, home):

    if home == True:
        team = get_HomeTeam(match_id)

    if home == False:
        team = get_AwayTeam(match_id)

    pass_att = 0
    pass_att_st = 0
    pass_att_med = 0
    pass_att_lg = 0
    pass_comp = 0
    pass_comp_st = 0
    pass_comp_med = 0
    pass_comp_lg = 0

    for mark in marks:

        event_id = mark["MarkGuid"]

        if "BallTouch" in mark["Tags"] and check_team(event_id, team, marks):

            if "DoNotCountPass" in mark["Attributes"]:
                pass_att += 1

                if "Short" in mark["Attributes"]:
                    pass_att_st += 1

                if "Medium" in mark["Attributes"]:
                    pass_att_med += 1

                if "Long" in mark["Attributes"]:
                    pass_att_lg += 1

            if "CountAsPass" in mark["BallTouch"]["PassingStatus"]:
                pass_att += 1
                pass_comp += 1

                if "Short" in mark["Attributes"]:
                    pass_att_st += 1
                    pass_comp_st += 1

                if "Medium" in mark["Attributes"]:
                    pass_att_med += 1
                    pass_comp_med += 1

                if "Long" in mark["Attributes"]:
                    pass_att_lg += 1
                    pass_comp_lg += 1

    data = [match_id, team, pass_att, pass_att_st, pass_att_med,
            pass_att_lg, pass_comp, pass_comp_st, pass_comp_med, pass_comp_lg]

    return data


def get_fouls_cards(marks, match_id, home):

    if home == True:
        team = get_HomeTeam(match_id)

    else:
        team = get_AwayTeam(match_id)

    fouls = 0
    yellow_cards = 0
    red_cards = 0

    for mark in marks:

        event_id = mark["MarkGuid"]

        if "Foul" in mark["Tags"] and check_foul(event_id, team, marks):
            fouls += 1

        if "Yellowcard" in mark["Tags"] and check_card(event_id, team, marks):
            yellow_cards += 1

            if "RedCard" in mark["Tags"]:
                red_cards += 1

        if "RedCard" in mark["Tags"] and check_card(event_id, team, marks):

            if "Yellowcard" not in mark["Tags"]:
                red_cards += 1

    data = [match_id, team, fouls, yellow_cards, red_cards]

    return data


def get_saves(marks, match_id, home):

    if home == True:
        team = get_HomeTeam(match_id)

    if home == False:
        team = get_AwayTeam(match_id)

    saves_total = 0
    saves_short = 0
    saves_medium = 0
    saves_long = 0

    for mark in marks:

        event_id = mark["MarkGuid"]

        if "Save" in mark["Tags"] and check_team(event_id, team, marks):
            saves_total += 1

            if "Short" in mark["Attributes"]:
                saves_short += 1

            if "Medium" in mark["Attributes"]:
                saves_medium += 1

            if "Long" in mark["Attributes"]:
                saves_long += 1

    data = [match_id, team, saves_total, saves_short, saves_medium, saves_long]

    return data


lineup_data = pd.read_csv("lineup_data.csv")


def get_HomeTeam(match_id, data=lineup_data):
    """
    Returns home team id
    """

    home_team = data.loc[data["MatchID"] == match_id]["HomeTeam"].iloc[0]

    return str(home_team)


def get_AwayTeam(match_id, data=lineup_data):
    """
    Returns away team id
    """

    away_team = data.loc[data["MatchID"] == match_id]["AwayTeam"].iloc[0]

    return str(away_team)


def check_team(event_id, team_id, data):
    """
    Check whether team performing the action is the indicated one
    """

    data = pd.DataFrame.from_dict(data, orient='columns')
    subjects = data[data["MarkGuid"] == event_id]["Subjects"].iloc[0]

    for x in subjects:

        if x["Verb"] == "Performed" and x["Type"] == "Team" and x["SubjectID"] == team_id:

            return True

    return False


def check_foul(event_id, team_id, data):
    """
    Check whether team performing the action is the indicated one
    """

    data = pd.DataFrame.from_dict(data, orient='columns')
    subjects = data[data["MarkGuid"] == event_id]["Subjects"].iloc[0]

    for x in subjects:

        if x["Verb"] == "Committed" and x["Type"] == "Team" and x["SubjectID"] == team_id:

            return True

    return False


def check_card(event_id, team_id, data):
    """
    Check whether team performing the action is the indicated one
    """

    data = pd.DataFrame.from_dict(data, orient='columns')
    subjects = data[data["MarkGuid"] == event_id]["Subjects"].iloc[0]

    for x in subjects:

        if x["Verb"] == "Suffered" and x["Type"] == "Team" and x["SubjectID"] == team_id:

            return True

    return False
