import pathlib as path

cwd = path.Path.cwd().parent
features_main = ["type", "game_id", "home_team", "away_team", "week", "season", "home_score", "away_score"]
league = "EPL"

###PATHS FOR SAVE FILE
input_raw = str(cwd) + "/input/" + league + "/01_raw/"
input_team = str(cwd) + "/input/" + league + "/teams/teams.csv"
filter_raw = str(cwd) + "/input/" + league + "/02_filter_raw/"
filter_raw_normalized = str(cwd) + "/input/" + league + "/03_filter_raw_normalized/"
indicators_base_cumsum = str(cwd) + "/input/" + league + "/04_indicators_base_cumsum/"
strengths = str(cwd) + "/input/" + league + "/05_strengths/"
probabilities = str(cwd) + "/input/" + league + "/06_probabilities/"
analysis = str(cwd) + "/input/" + league + "/07_analysis/"

analysis_per_team_home = ["Shoot_asH", "ShootTarget_asH", "Fouls_asH", "Corner_asH", "FTG_asH", "HTG_asH",
                          "YellowC_asH",
                          "RedC_asH", "FT_against_H", "HT_against_H", "Shoot_against_H", "ShootTarget_against_H",
                          "Fouls_against_H", "Corner_against_H", "RedC_againts_H", "YellowC_against_H"]
analysis_per_team_away = ["Shoot_asA", "ShootTarget_asA", "Fouls_asA", "Corner_asA", "FTG_asA", "HTG_asA",
                          "YellowC_asA",
                          "RedC_asA", "FT_against_A", "HT_against_A", "Shoot_against_A", "ShootTarget_against_A",
                          "Fouls_against_A", "Corner_against_A", "RedC_againts_A", "YellowC_against_A"]

matrix_FT_goals = ["FTG_asH", "FT_against_H", "FTG_asA", "FT_against_A"]

periods = [3, 6, 10, "infinity"]

years_train = list(range(2003, 2005))
years_test = list(range(2014, 2020))
all_years = list(range(2003, 2020))

features_games = ["idGame", "nWeekHome", "nWeekAway", "Date", "year", "IdHomeTeam", "IdAwayTeam", "FTHG",
                  "FTAG", "FTR", "HTHG", "HTAG",
                  "HTR",
                  "Referee", "HS",
                  "AS",
                  "HST", "AST", "HF", "AF", "HC", "AC", "HY", "AY", "HR", "AR"]

features_id = ['idGame', 'IdHomeTeam', 'IdAwayTeam', 'nWeekHome', 'nWeekAway', "Date", 'year']
features_prob = ["idGame", "Date", "Id_Team_Home", "Id_Team_Away", "nWeekHome", "nWeekAway", "Referee",
                 "Goals_H", "Goals_A", "multiplication_home_last_3", "multiplication_away_last_3",
                 "multiplication_home_last_6", "multiplication_away_last_6", "multiplication_home_last_10",
                 "multiplication_away_last_10", "multiplication_home_last_infinity",
                 "multiplication_away_last_infinity"]

brokers = ["B365", "BS", "BW", "GB", "IW",
           "LB", "PS", "P", "SO", "SB", "SJ", "SY", "VC", "WH"]
brokers_P = ["idGame", "Date", "Id_Team_Home", "Id_Team_Away",
             "nWeekHome", "nWeekAway", "PH", "PD", "PA", "WHH", "WHD", "WHA",
             "B365H", "B365D", "B365A"]

markets = ["H", "D", "A", ">2.5", "<2.5"]

reorder = ["idGame", "Date", "Referee", "Id_Team_Home", "Id_Team_Away", "nWeekHome", "nWeekAway", "year", "Goals_H",
           "Goals_A", "Prob_H_last_3", "Prob_D_last_3", "Prob_A_last_3", "Prob_H_last_6",
           "Prob_D_last_6",
           "Prob_A_last_6", "Prob_H_last_10", "Prob_D_last_10", "Prob_A_last_10", "Prob_H_last_infinity",
           "Prob_D_last_infinity", "Prob_A_last_infinity", "Average_H", "Std_dev_H", \
           "Average_D",
           "Std_dev_D", "Average_A", "Std_dev_A", "Average_>2.5", "Std_dev_>2.5", "Average_<2.5",
           "Std_dev_<2.5"]
