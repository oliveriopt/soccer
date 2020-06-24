from datetime import date
from src.a_date_calculation import *
import pandas as pd
import src.variables as var
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class CreateTable:

    def __init__(self, year):
        self.year = year
        self.file = pd.read_csv(var.filter_raw_normalized + "stats_" + str(self.year) + ".csv", sep=",", header=0,
                                encoding='unicode_escape', index_col=0)
        self.number_weeks_total = self.file.tail(n=1)["nWeekHome"]
        self.teams = []
        self.table = pd.DataFrame()
        self.home = pd.DataFrame()
        self.away = pd.DataFrame()

    def identify_teams_id(self) -> None:
        """
        Identify teams
        :param df:
        :return:
        """
        home_teams_id = list(self.file["IdHomeTeam"].tolist())
        away_teams_id = list(self.file["IdAwayTeam"].tolist())
        self.teams = list(set(home_teams_id + away_teams_id))
        self.teams.sort()

    def create_table_per_team(self) -> None:
        """
        Create table per team
        :return:
        """
        for team_id in self.teams:
            home = self.file.loc[(self.file["IdHomeTeam"] == team_id)].reset_index(drop=True)
            home = home.rename(columns={"FTHG": "FTG_asH", "FTR": "FT_RESULT", "HTHG": "HTG_asH",
                                        "HTR": "HT_RESULT", "HS": "Shoot_asH", "HST": "ShootTarget_asH",
                                        "HF": "Fouls_asH", "HC": "Corner_asH", "HY": "YellowC_asH", "HR": "RedC_asH",
                                        "FTAG": "FT_against_H", "HTAG": "HT_against_H",
                                        "AS": "Shoot_against_H", "AST": "ShootTarget_against_H",
                                        "AF": "Fouls_against_H",
                                        "AC": "Corner_against_H", "AR": "RedC_againts_H", "AY": "YellowC_against_H"})
            home["nWeekHome"] = home.index + 1
            home.drop(["nWeekAway", "IdAwayTeam"], axis=1,
                      inplace=True)
            home.loc[(home["FT_RESULT"] == "H"), "FT_RESULT"] = "Winn"
            home.loc[(home["FT_RESULT"] == "D"), "FT_RESULT"] = "Draw"
            home.loc[(home["FT_RESULT"] == "A"), "FT_RESULT"] = "Lost"
            home.loc[(home["HT_RESULT"] == "H"), "HT_RESULT"] = "Winn"
            home.loc[(home["HT_RESULT"] == "D"), "HT_RESULT"] = "Draw"
            home.loc[(home["HT_RESULT"] == "A"), "HT_RESULT"] = "Lost"

            away = self.file.loc[(self.file["IdAwayTeam"] == team_id)].reset_index(drop=True)
            away = away.rename(columns={"FTAG": "FTG_asA", "FTR": "FT_RESULT", "HTAG": "HTG_asA",
                                        "HTR": "HT_RESULT", "AS": "Shoot_asA", "AST": "ShootTarget_asA",
                                        "AF": "Fouls_asA", "AC": "Corner_asA", "AY": "YellowC_asA", "AR": "RedC_asA",
                                        "FTHG": "FT_against_A", "HTHG": "HT_against_A",
                                        "HS": "Shoot_against_A", "HST": "ShootTarget_against_A",
                                        "HF": "Fouls_against_A",
                                        "HC": "Corner_against_A", "HR": "RedC_againts_A", "HY": "YellowC_against_A"})
            away["nWeekAway"] = away.index + 1
            away.drop(["nWeekHome", "IdHomeTeam"], axis=1,
                      inplace=True)
            away.loc[(away["FT_RESULT"] == "H"), "FT_RESULT"] = "Lost"
            away.loc[(away["FT_RESULT"] == "D"), "FT_RESULT"] = "Draw"
            away.loc[(away["FT_RESULT"] == "A"), "FT_RESULT"] = "Winn"
            away.loc[(away["HT_RESULT"] == "H"), "HT_RESULT"] = "Lost"
            away.loc[(away["HT_RESULT"] == "D"), "HT_RESULT"] = "Draw"
            away.loc[(away["HT_RESULT"] == "A"), "HT_RESULT"] = "Winn"

            self.home = self.home.append(home, ignore_index=True)
            self.away = self.away.append(away, ignore_index=True)

        self.home["Date"] = pd.to_datetime(self.home["Date"], format="%Y-%m-%d")
        self.away["Date"] = pd.to_datetime(self.away["Date"], format="%Y-%m-%d")
        self.home.reset_index(drop=True)
        self.away.reset_index(drop=True)

    def calculate_cumsum(self, cumsum: pd.DataFrame, Home_Away: str, variables_analysis: list) -> None:
        """
        Calculate cumsum over all parameteres
        :param cumsum: dataframe to analysis the cumsum
        :param idTeam: home or away teams
        :return:
        """

        temp = pd.DataFrame()
        for team in self.teams:
            team_hist = cumsum.loc[cumsum["Id" + Home_Away + "Team"] == team].reset_index(drop=True)
            print(team_hist)
            for item in variables_analysis:
                for period in var.periods:
                    if isinstance(period, str):
                        team_hist[item + "_last_" + str(period) + "_cumsum"] = team_hist[item].cumsum(skipna=True)
                        team_hist[item + "_last_" + str(period) + "_cumsum"] = team_hist[item + "_last_" + str(period) +
                                                                                        "_cumsum"] - team_hist[item]
                        team_hist[item + "_last_" + str(period) + "_mean"] = team_hist[item + "_last_" + str(period) + "_cumsum"] / \
                                                                             team_hist["nWeek" + Home_Away]
                    else:
                        team_hist[item + "_last_" + str(period) + "_cumsum"] = team_hist[item].rolling(period + 1).sum()
                        team_hist[item + "_last_" + str(period) + "_cumsum"] = team_hist[item + "_last_" + str(period) +
                                                                                        "_cumsum"] - team_hist[item]
                        team_hist[item + "_last_" + str(period) + "_mean"] = team_hist[item + "_last_" + str(period) + "_cumsum"] / \
                                                                             period



            temp = temp.append(team_hist)
        return temp

    def calculate_scores(self) -> None:
        temp = CreateTable.calculate_cumsum(self, self.home, "Home", var.analysis_per_team_home)
        self.home = temp.copy().sort_values(by="Date").reset_index(drop=True)

        temp = CreateTable.calculate_cumsum(self, self.away, "Away", var.analysis_per_team_away)
        self.away = temp.copy().sort_values(by="Date").reset_index(drop=True)

    def write_output(self) -> None:
        self.home.round(2).to_csv(var.indicators_base_cumsum + "home_" + str(self.year) + ".csv")
        self.away.round(2).to_csv(var.indicators_base_cumsum + "away_" + str(self.year) + ".csv")


for year in var.all_years[:1]:
    print(year)
    table_teams = CreateTable(year)
    table_teams.identify_teams_id()
    table_teams.create_table_per_team()
    table_teams.calculate_scores()
    table_teams.write_output()
