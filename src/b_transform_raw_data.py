import pandas as pd
import src.variables as var

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class TransformRawData:

    def __init__(self, path, year, header_odds):
        self.path = path
        self.year = year
        self.file = pd.read_csv(self.path + str(self.year) + ".csv", sep=";", header=0,
                                encoding='unicode_escape')
        self.teams = []
        self.stats = pd.DataFrame
        self.odds = pd.DataFrame
        self.list_teams = pd.read_csv(var.input_team, sep=',', encoding='unicode_escape')
        self.header_odds = header_odds

    def identify_teams(self, df):
        """
        Identify teams
        :param df:
        :return:
        """
        home_teams = list(set(df["HomeTeam"].tolist()))
        away_teams = list(set(df["AwayTeam"].tolist()))
        self.teams = home_teams + away_teams

    def identify_first(self, arr1, arr2):

        if arr1[0] < arr2[0]:
            return arr1, arr2
        else:
            return arr2, arr1

    def create_tuple(self, home, away) -> list:

        week_array = []
        #  first, away = self.identify_first(arr1, arr2)
        for week in list(range(1, len(home) + len(away) + 1)):
            flag_home = False
            flag_away = False
            if len(home) > 0 and len(away) > 0:
                if home[0] < away[0]:
                    tup = (home[0], week, "home")
                    flag_home = True
                if home[0] > away[0]:
                    tup = (away[0], week, "away")
                    flag_away = True
            if not home:
                tup = (away[0], week, "away")
                flag_away = True
            if not away:
                tup = (home[0], week, "home")
                flag_home = True
            if flag_home:
                del home[0]
            if flag_away:
                del away[0]
            week_array.append(tup)
        return week_array

    def define_features(self):

        self.file["nWeekHome"] = None
        self.file["nWeekAway"] = None
        self.file['Date'] = pd.to_datetime(self.file['Date'], format="%d/%m/%Y")
        self.file["year"] = self.year

    def read_map_team_file(self) -> None:
        """
        Map id teams for main dataframe
        :return:
        """
        self.define_features()
        dictionary_teams = dict(zip(self.list_teams["NameTeam"].values, self.list_teams["IdTeam"].values))
        self.file["idGame"] = self.file["HomeTeam"].astype(str).str[:] + "_" + self.file["AwayTeam"].astype(
            str).str[:] + "_" + str(self.year)
        self.file['IdHomeTeam'] = self.file['HomeTeam'].map(dictionary_teams)
        self.file['IdAwayTeam'] = self.file['AwayTeam'].map(dictionary_teams)
        max_number_teams = self.list_teams.shape[0]
        for tm in range(max_number_teams):
            temp_home = list(self.file[self.file["IdHomeTeam"] == tm].sort_values(by="Date").index)
            temp_away = list(self.file[self.file["IdAwayTeam"] == tm].sort_values(by="Date").index)
            if (len(temp_home) > 0) and (len(temp_away) > 0):
                index_week = self.create_tuple(temp_home, temp_away)
                for index in index_week:
                    if index[2] == "home":
                        self.file.at[index[0], "nWeekHome"] = index[1]
                    if index[2] == "away":
                        self.file.at[index[0], "nWeekAway"] = index[1]

    def create_stats_odds_games(self) -> None:
        """
        Create output odds and stats files
        :return:
        """
        self.stats = self.file[var.features_games].sort_values(by="Date")
        features_odds = list(set(list(self.file.columns.values)).difference(set(var.features_games)))
        features_odds = list(set(features_odds).difference(set(['Div', 'HomeTeam', 'AwayTeam'])))
        features_odds.extend(['idGame', "nWeekHome", "nWeekAway", 'Date', 'year', 'IdHomeTeam', 'IdAwayTeam'])
        self.odds = self.file[features_odds].sort_values(by="Date")
        self.stats.reset_index(drop=True).to_csv(var.filter_raw + "stats_" + str(self.year) + ".csv")
        self.odds.reset_index(drop=True).to_csv(var.filter_raw + "odds_" + str(self.year) + ".csv")

    def map_header_odds(self) -> None:
        """
        Map list total of
        :return:
        """

        temp = list(self.odds.columns.values)
        self.header_odds.extend(temp)
        self.header_odds.sort()
        var.features_id.reverse()
        for item in var.features_id:
            self.header_odds.remove(item)
            self.header_odds.insert(0, item)
        return list(set(self.header_odds))


class MapOdss:

    def __init__(self, year, header_odds):
        self.year = year
        self.odds = pd.read_csv(var.filter_raw + "odds_" + str(self.year) + ".csv", sep=",", header=0,
                                encoding='unicode_escape', index_col=0)
        self.stats = pd.read_csv(var.filter_raw + "stats_" + str(self.year) + ".csv", sep=",", header=0,
                                 encoding='unicode_escape', index_col=0)
        self.header_odds = list(set(header_odds))

    def verify_header(self):

        for col in self.header_odds:
            if col not in list(self.odds.columns.values):
                self.odds[col] = None

        self.odds = self.odds[self.header_odds]

    def save_files(self):
        self.stats.to_csv(var.filter_raw_normalized + "stats_" + str(self.year) + ".csv")
        self.odds.to_csv(var.filter_raw_normalized + "odds_" + str(self.year) + ".csv")
