import processing_marks as m
import numpy as np
import json
import pandas as pd

first_id = 2019282
second_id = 2019377
third_id = 2019613
fourth_id = 2019641
fifth_id = 2021587
sixth_id = 2021711
seventh_id = 2025053
eigth_id = 2025148

ids = []
ids.extend(list(np.arange(first_id, second_id + 1)))
ids.extend(list(np.arange(third_id, fourth_id + 1)))
ids.extend(list(np.arange(fifth_id, sixth_id + 1)))
ids.extend(list(np.arange(seventh_id, eigth_id + 1)))

passes_data = []
tackle_data = []
shot_data = []
fk_data = []
corner_data = []
passes_data = []
foul_data = []
saves_data = []

for x in ids:

    with open(str(x) + "_Marks.json") as f:
        marks_data = json.load(f)

    marks = ["MarkGuid", "Tags", "Attributes", "Subjects", "BallTouch"]
    tags = ["Tackle", "Shot", "FreeKick", "Corner",
            "BallTouch", "Save", "Foul", "Yellowcard", "RedCard"]

    marks_data = m.clean_keys(marks_data, marks)
    marks_data = m.clean_marks(marks_data, tags)

    for boolean in [True, False]:

        tackle_data.append(m.get_tackles(marks_data, x, boolean))
        shot_data.append(m.get_shots(marks_data, x, boolean))
        fk_data.append(m.get_fk(marks_data, x, boolean))
        corner_data.append(m.get_corner(marks_data, x, boolean))
        passes_data.append(m.get_passes(marks_data, x, boolean))
        foul_data.append(m.get_fouls_cards(marks_data, x, boolean))
        saves_data.append(m.get_saves(marks_data, x, boolean))

tackle_names = ["Match_ID", "Team_ID", "Tack_Att", "Tack_Succ", "TS_Short", "TS_Med", "TS_Long"]
shot_names = ["Match_ID", "Team_ID", "Shots", "Shots_BigChance",
              "Shots_OnTarget", "Shots_OffTarget", "Shots_Blocked", "Shots_St", "Shots_Med"]
fk_names = ["Match_ID", "Team_ID", "FK_Tot", "FK_Ind", "FK_Dir",
            "FK_St", "FK_Med", "FK_Lg", "FK_Cross", "FK_Unsuccessful"]
corner_names = ["Match_ID", "Team_ID", "Corners", "Corner_Short", "Corner_Cross",
                "Corner_Medium", "Corner_Long", "Corner_Unsuccessful", "Corner_Shot", "Corner_OnTarget"]
passes_names = ["Match_ID", "Team_ID", "Pass_Att", "Pass_Att_St", "Pass_Att_Med",
                "Pass_Att_Lg", "Pass_Comp", "Pass_Comp_St", "Pass_Comp_Med", "Pass_Comp_Lg"]
foul_names = ["Match_ID", "Team_ID", "Fouls", "Yellow_Cards", "Red_Cards"]
saves_names = ["Match_ID", "Team_ID", "Saves", "Saves_Short", "Saves_Medium", "Saves_Long"]

tackle_df = pd.DataFrame(tackle_data, columns=tackle_names)
shot_df = pd.DataFrame(shot_data, columns=shot_names)
fk_df = pd.DataFrame(fk_data, columns=fk_names)
corner_df = pd.DataFrame(corner_data, columns=corner_names)
pass_df = pd.DataFrame(passes_data, columns=passes_names)
foul_df = pd.DataFrame(foul_data, columns=foul_names)
saves_df = pd.DataFrame(saves_data, columns=saves_names)

tackle_df.to_csv("tackle_data.csv")
shot_df.to_csv("shots_data.csv")
fk_df.to_csv("fk_data.csv")
corner_df.to_csv("corner_data.csv")
pass_df.to_csv("passes_data.csv")
foul_df.to_csv("foul_data.csv")
saves_df.to_csv("saves_data.csv")

dfs = [tackle_df, shot_df, fk_df, corner_df, pass_df, foul_df, saves_df]
data = reduce(lambda left, right: pd.merge(left, right, on=["Match_ID", "Team_ID"]), dfs)
data.drop(["Unnamed: 0_x", "Unnamed: 0_y", "Unnamed: 0"], axis=1, inplace=True)
data.to_csv("final_data.csv")
