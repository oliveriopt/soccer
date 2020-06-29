from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import src.variables as var

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class CalculateStrengthsTime:

    def __init__(self, year):
        self.year = year
        self.home = pd.read_csv(var.indicators_base_cumsum + "home_" + str(self.year) + ".csv", sep=",", header=0,
                                encoding='unicode_escape', index_col=0)
        self.away = pd.read_csv(var.indicators_base_cumsum + "away_" + str(self.year) + ".csv", sep=",", header=0,
                                encoding='unicode_escape', index_col=0)
        self.teams = list(self.home["IdHomeTeam"].values)
        self.dates_home = list(set(list(self.home["Date"].values)))
        self.dates_away = list(set(list(self.away["Date"].values)))
        #  self.home['Date'] = pd.to_datetime(self.home['Date'], format='%Y-%m-%d')
        #  self.away['Date'] = pd.to_datetime(self.away['Date'], format='%Y-%m-%d')
        self.dates_home.sort()
        self.dates_away.sort()

    def calculate_mean_by_date(self, df_analysis: pd.DataFrame, Home_Away: str, analysis_per_team: list):
        """
        Calculate from mean by team, the mean by round
        :param df_analysis: home or away data
        :param Home_Away: string to identify home or away teams
        :param analysis_per_team: variables to analysis from var file
        :return:
        """

        df_mean = pd.DataFrame(index=np.arange(len(self.dates_home)))
        index = 0
        for date_g in self.dates_home:
            day = str(datetime.strptime(date_g, "%Y-%m-%d") - timedelta(days=1))
            temp = df_analysis[df_analysis["Date"] <= day]
            temp = temp.sort_values(by=["Date", "Id" + Home_Away + "Team"], ascending=[False, True]).reset_index(
                drop=True)
            temp = temp.drop_duplicates(subset=["Id" + Home_Away + "Team"], keep='first').reset_index(drop=True)

            number_teams = temp.shape[0]
            for item in analysis_per_team:
                for period in var.periods:
                    df_mean.at[index, "n_teams"] = number_teams
                    df_mean.at[index, "Date"] = date_g
                    df_mean.at[index, item + "_last_" + str(period) + "_mean_by_date"] = temp[item + "_last_" + str(
                        period) + "_mean_by_team"].mean()
            index += 1
        df_mean.sort_values(by="Date")
        return df_mean

    def running_time(self) -> tuple:
        """
        Calculate mean by date for home and away rounds
        :return:
        """

        self.home.sort_values(by="Date")
        self.away.sort_values(by="Date")

        mean_home = CalculateStrengthsTime.calculate_mean_by_date(self, self.home, "Home", var.analysis_per_team_home)
        mean_away = CalculateStrengthsTime.calculate_mean_by_date(self, self.away, "Away", var.analysis_per_team_away)
        return mean_home, mean_away

    def calculate_strengths_by_home_away(self, df_analysis: pd.DataFrame, mean: pd.DataFrame,
                                         analysis_per_team: list) -> pd.DataFrame:
        """
        Calculate strengths for home and away
        :param df_analysis:
        :param mean:
        :param analysis_per_team:
        :return:
        """
        result = pd.merge(df_analysis, mean, how="left", on="Date")
        for item in analysis_per_team:
            for period in var.periods:
                st = item + "_last_" + str(period)
                df_analysis[st + "_strength"] = result[st + "_mean_by_team"] / result[st + "_mean_by_date"]
        return df_analysis

    def calculate_strengths(self, mean_home: pd.DataFrame, mean_away: pd.DataFrame):

        self.home = CalculateStrengthsTime.calculate_strengths_by_home_away(self, self.home, mean_home,
                                                                            var.analysis_per_team_home)
        self.away = CalculateStrengthsTime.calculate_strengths_by_home_away(self, self.away, mean_away,
                                                                            var.analysis_per_team_away)

    def save_files(self) -> None:
        self.home.round(3).to_csv(var.strengths + "home_" + str(self.year) + ".csv")
        self.away.round(3).to_csv(var.strengths + "away_" + str(self.year) + ".csv")
