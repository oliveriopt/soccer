from scipy.stats import poisson

import pandas as pd
import numpy as np
import src.variables as var
import src.dic_matrix as dict_indic

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class CreateMatrix:

    def __init__(self, year):
        self.year = year
        self.home = pd.read_csv(var.strengths + "home_" + str(self.year) + ".csv", sep=",", header=0,
                                encoding='unicode_escape', index_col=0)
        self.away = pd.read_csv(var.strengths + "away_" + str(self.year) + ".csv", sep=",", header=0,
                                encoding='unicode_escape', index_col=0)
        self.teams = list(self.home["IdTeam"].values)
        self.odds = pd.read_csv(var.filter_raw_normalized + "odds_" + str(self.year) + ".csv", sep=",", header=0,
                                encoding='unicode_escape', index_col=0)
        self.result = pd.DataFrame

    def merge_strengths(self, home: pd.DataFrame, away: pd.DataFrame):
        header = list(dict_indic.dict_FT_h.keys())
        home = home[header]
        home = home.rename(columns=dict_indic.dict_FT_h)
        header = list(dict_indic.dict_FT_a.keys())
        away = away[header]
        away = away.rename(columns=dict_indic.dict_FT_a)
        self.result = pd.merge(home, away, on=["idGame", "Date", "year", "Referee"])

        for period in var.periods:
            self.result["multiplication_home_last_" + str(period)] = self.result["Goals_H_SA_last_" + str(period)] * \
                                                                     self.result[
                                                                         "Goals_A_SD_last_" +
                                                                         str(period)] \
                                                                     * self.result[
                                                                         "Goals_H_SA_last_" + str(period) + "_mean"]

            self.result["multiplication_away_last_" + str(period)] = self.result["Goals_A_SA_last_" + str(period)] * \
                                                                     self.result[
                                                                         "Goals_H_SD_last_" +
                                                                         str(period)] \
                                                                     * self.result[
                                                                         "Goals_A_SA_last_" + str(period) + "_mean"]
        self.result = self.result[var.features_prob]

    def build_matrix(self, multip):
        list_prob = []

        for period in var.periods:
            mat = pd.DataFrame(index=np.arange(7), columns=np.arange(7))
            for x in np.arange(7):
                for y in np.arange(7):
                    mat.at[x, y] = poisson.pmf(float(x), multip["multiplication_home_last_" + str(period)]) * \
                                   poisson.pmf(
                                       float(y), multip["multiplication_away_last_" + str(period)]) * 100
            prob_home = prob_draw = prob_away = 0
            for x in np.arange(7):
                for y in np.arange(7):
                    if x == y: prob_draw = mat.at[x, y] + prob_draw
                    if x > y: prob_home = mat.at[x, y] + prob_home
                    if x < y: prob_away = mat.at[x, y] + prob_away

            list_prob.append([prob_home, prob_draw, prob_away])
        return list_prob

    def odds_average(self):
        self.odds.sort_values(by="idGame")
        result = self.odds.reindex(columns=var.features_id)
        for market in var.markets:
            header = [suit + market for suit in var.brokers]
            temp = self.odds.reindex(columns=header)
            temp = 1 / temp
            temp["Average_" + market] = (temp[header].mean(axis=1, skipna=True))*100
            temp["Std_dev_" + market] = (temp[header].std(axis=1, skipna=True))*100
            result = pd.concat([result, temp[["Average_" + market, "Std_dev_" + market]]], axis=1)
        result = result.rename(columns={'IdHomeTeam': "Id_Team_Home", 'IdAwayTeam': "Id_Team_Away"})
        return result

    def save_files(self):
        avg_odds = CreateMatrix.odds_average(self)
        self.result.round(3).reset_index(drop=True).to_csv(var.probabilities + "prob_" + str(self.year) + ".csv")
        self.result = pd.merge(self.result, avg_odds, on=["idGame", "Date"])
        self.result = self.result.drop(["Id_Team_Home_x", "Id_Team_Away_x", "nWeekHome_x", "nWeekAway_x"],
                                       axis=1)
        self.result = self.result.rename(columns={"Id_Team_Home_y": "Id_Team_Home", "Id_Team_Away_y": "Id_Team_Away",
                                                  "nWeekHome_y": "nWeekHome", "nWeekAway_y": "nWeekAway"})
        self.result = self.result[var.reorder]
        self.result.round(3).reset_index(drop=True).to_csv(var.probabilities + "prob_" + str(self.year) + ".csv")

    def create_dataframe_home_away(self):
        CreateMatrix.merge_strengths(self, self.home, self.away)
        for ind, row in self.result.iterrows():
            list_prob = CreateMatrix.build_matrix(self, row)
            for period in var.periods:
                self.result.at[ind, "Prob_H_last_" + str(period)] = list_prob[var.periods.index(period)][0]
                self.result.at[ind, "Prob_D_last_" + str(period)] = list_prob[var.periods.index(period)][1]
                self.result.at[ind, "Prob_A_last_" + str(period)] = list_prob[var.periods.index(period)][2]
