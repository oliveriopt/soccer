import pandas as pd
import src.variables as var

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class Analysis:

    def __init__(self, year):
        self.year = year
        self.prob = pd.read_csv(var.probabilities + "prob_" + str(self.year) + ".csv", sep=",", header=0,
                                encoding='unicode_escape', index_col=0)
        self.list_teams = pd.read_csv(var.input_team, sep=',', encoding='unicode_escape')
        self.count_teams = pd.DataFrame(index=range(self.list_teams.shape[0] * len(var.all_years[:1])),
                                        columns=["IdTeam", "year",
                                                 "Home Range -100, -5", "Home Range -5, 5", "Home Range 5, 100",
                                                 "Draw Range -100, -5 asHome", "Draw Range -5, 5 asHome",
                                                 "Draw Range 5, 100 as Home"
                                                 "Draw Range -100, -5 asAway", "Draw Range -5, 5 asAway",
                                                 "Draw Range 5, 100 asAway"
                                            , "Away Range -100, -5", "Away Range -5, 5", "Away Range 5, 100"])
        self.teams = list(set(list(self.prob["Id_Team_Home"].values)))

    def create_difference(self):
        for period in var.periods:
            for market in var.markets[0:3]:
                text = "Prob_" + market + "_last_" + str(period)
                self.prob["Diff_" + market + "_last_" + str(period)] = self.prob[text] - self.prob["Average_" +
                                                                                                   market]
            #    print(self.prob.tail())

    def calculate_percentage_stdev(self):

        for market in var.markets:
            self.prob["Percent_Stdev" + market] = (self.prob["Std_dev_" + market]) * 100. / self.prob["Average_" +
                                                                                                      market]
            print(self.prob["Percent_Stdev" + market].mean())

    def calculate_teams(self):
        temp = pd.DataFrame(columns=["IdTeam", "year",
                                     "Home Range -100, -5", "Home Range -5, 5", "Home Range 5, 100",
                                     "Draw Range -100, -5 asHome", "Draw Range -5, 5 asHome",
                                     "Draw Range 5, 100 as Home"
                                     "Draw Range -100, -5 asAway", "Draw Range -5, 5 asAway", "Draw Range 5, 100 asAway"
            , "Away Range -100, -5", "Away Range -5, 5", "Away Range 5, 100"])
        temp["IdTeam"] = self.teams
        temp["year"] = [self.year] * temp.shape[0]
        temp_Home_in = self.prob[(self.prob["Diff_H_last_10"] >= -5) & (self.prob["Diff_H_last_10"] <= 5)]
        temp_Draw_in = self.prob[(self.prob["Diff_D_last_10"] >= -5) & (self.prob["Diff_D_last_10"] <= 5)]
        temp_Away_in = self.prob[(self.prob["Diff_A_last_10"] >= -5) & (self.prob["Diff_A_last_10"] <= 5)]
        temp["Home Range -5, 5"] = temp_Home_in['Id_Team_Home'].value_counts()
        temp["Draw Range -5, 5 asHome"] = temp_Draw_in['Id_Team_Home'].value_counts()
        temp["Draw Range -5, 5 asAway"] = temp_Draw_in['Id_Team_Away'].value_counts()
        temp["Away Range -5, 5"] = temp_Away_in['Id_Team_Away'].value_counts()

        temp_Home_in = self.prob[(self.prob["Diff_H_last_10"] < -5)]
        temp_Draw_in = self.prob[(self.prob["Diff_D_last_10"] < -5)]
        temp_Away_in = self.prob[(self.prob["Diff_A_last_10"] < -5)]
        temp["Home Range -100, -5"] = temp_Home_in['Id_Team_Home'].value_counts()
        temp["Draw Range -5, 5 asHome"] = temp_Draw_in['Id_Team_Home'].value_counts()
        temp["Draw Range -5, 5 asAway"] = temp_Draw_in['Id_Team_Away'].value_counts()
        temp["Away Range -100, -5"] = temp_Away_in['Id_Team_Away'].value_counts()

        temp_Home_in = self.prob[(self.prob["Diff_H_last_10"] > 5)]
        temp_Draw_in = self.prob[(self.prob["Diff_D_last_10"] > 5)]
        temp_Away_in = self.prob[(self.prob["Diff_A_last_10"] > 5)]
        temp["Home Range 5, 100"] = temp_Home_in['Id_Team_Home'].value_counts()
        temp["Draw Range -5, 5 asHome"] = temp_Draw_in['Id_Team_Home'].value_counts()
        temp["Draw Range -5, 5 asAway"] = temp_Draw_in['Id_Team_Away'].value_counts()
        temp["Away Range 5, 100"] = temp_Away_in['Id_Team_Away'].value_counts()
        return (temp)

        pass

    def write_file(self):
        self.prob = self.prob[(self.prob["nWeekHome"] >= 8) & (self.prob["nWeekAway"] >= 8)]
        self.prob.round(3).to_csv(var.analysis + "ana_" + str(self.year) + ".csv")


dist_teams = pd.DataFrame()
for year in var.all_years:
    print(year)
    analysis = Analysis(year)
    analysis.create_difference()
    temp = analysis.calculate_teams()
    dist_teams = dist_teams.append(temp).reset_index(drop=True)
    analysis.write_file()
dist_teams = dist_teams.merge(analysis.list_teams, on='IdTeam').sort_values(by="year").reset_index(drop=True)
dist_teams.round(0).to_csv(var.analysis + "distr_teams.csv")

print(dist_teams)
