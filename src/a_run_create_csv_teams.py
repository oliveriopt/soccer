from src.b_transform_raw_data import TransformRawData
from sklearn import preprocessing

import csv
import src.variables as var

import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def read_files(list_teams=[]) -> list:
    """
    Read files for create list of teams
    :param teams:
    :return:
    """

    for year in var.all_years:
        print(year)
        transform = TransformRawData(var.input_raw, year, var.league)
        transform.identify_teams(transform.file)
        list_teams.extend(transform.teams)
    lis = list(set(list_teams))
    lis.sort()

    return lis


def create_list_teams(teams: list) -> list:
    """
    Create list of teams
    :param teams:
    :return:
    """
    teams = list(set(teams))
    teams.sort()
    decod_teams = list(range(len(teams)))
    return decod_teams


def export_teams_csv(teams: list, decod_teams: list) -> None:
    """
    Export decoder team to csv file
    :param teams:
    :param decod_teams:
    :return:
    """
    with open(var.input_team, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["NameTeam", "IdTeam"])
        writer.writerows(zip(teams, list(decod_teams)))

### CREATE LIST OF TEAMS
teams = read_files()
decod_teams = create_list_teams(teams)
export_teams_csv(teams, decod_teams)

