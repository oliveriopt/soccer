import src.variables as var
from src.e_create_goal_matrix import *

for year in var.all_years[:]:
    print(year)
    game = CreateMatrix(year)
    game.create_dataframe_home_away()
    game.odds_average()
    game.save_files()