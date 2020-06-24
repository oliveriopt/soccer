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
        self.teams = list(self.home["IdTeam"].values)
        self.dates_home = list(set(list(self.home["Date"].values)))
        self.dates_away = list(set(list(self.away["Date"].values)))
        self.dates_home.sort()
        self.dates_away.sort()

    def running_time(self) -> tuple:
        """"
        Calculate the means given every date
        """

        mean_home = pd.DataFrame(index=np.arange(len(self.dates_home)))
        mean_away = pd.DataFrame(index=np.arange(len(self.dates_away)))

        self.home.sort_values(by="Date")
        self.away.sort_values(by="Date")
        index = 0
        for date_g in self.dates_home:
            temp = self.home[self.home["Date"] <= date_g]
            temp = temp.sort_values(by=["Date", "IdTeam"], ascending=[False, True]).reset_index(drop=True)
            temp = temp.drop_duplicates(subset=["IdTeam"], keep='first')
            number_teams = temp.shape[0]
            for item in var.analysis_per_team_home:
                for period in var.periods:
                    mean_home.at[index, "n_teams"] = number_teams
                    mean_home.at[index, "Date"] = date_g
                    mean_home.at[index, item + "_last_" + str(period) + "_mean"] = temp[item + "_last_" + str(
                        period)].mean()
            index += 1

        index = 0
        for date_g in self.dates_away:
            temp = self.away[self.away["Date"] <= date_g]
            temp = temp.sort_values(by=["Date", "IdTeam"], ascending=[False, True]).reset_index(drop=True)
            temp = temp.drop_duplicates(subset=["IdTeam"], keep='first')
          #  print(temp)
            number_teams = temp.shape[0]
            for item in var.analysis_per_team_away:
                for period in var.periods:
                    mean_away.at[index, "n_teams"] = number_teams
                    mean_away.at[index, "Date"] = date_g
                    mean_away.at[index, item + "_last_" + str(period) + "_mean"] = temp[item + "_last_" + str(
                        period)].mean()
            index += 1
        mean_home.sort_values(by="Date")
        mean_away.sort_values(by="Date")
        return mean_home, mean_away

    def calculate_strengths(self, mean_home: pd.DataFrame, mean_away: pd.DataFrame):
        result_home = pd.merge(self.home, mean_home, how="left", on="Date")
        result_away = pd.merge(self.away, mean_away, how="left", on="Date")
        # print(result_home)
        for item in var.analysis_per_team_home:
            for period in var.periods:
                st = item + "_last_" + str(period)
                self.home[st + "_strength"] = result_home[st] / result_home[st + "_mean"]
                self.home[st + "_mean"] = result_home[st + "_mean"]
        for item in var.analysis_per_team_away:
            for period in var.periods:
                st = item + "_last_" + str(period)
                self.away[st + "_strength"] = result_away[st] / result_away[st + "_mean"]
                self.away[st + "_mean"] = result_away[st + "_mean"]

    def save_files(self, mean_home: pd.DataFrame, mean_away: pd.DataFrame) -> None:
        self.home.round(3).to_csv(var.strengths + "home_" + str(self.year) + ".csv")
        self.away.round(3).to_csv(var.strengths + "away_" + str(self.year) + ".csv")
#     mean_home.round(3).to_csv(var.strengths + "mean_home_" + str(self.year) + ".csv")
#    mean_away.round(3).to_csv(var.strengths + "mean_away_" + str(self.year) + ".csv")
