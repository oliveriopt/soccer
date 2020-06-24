import src.variables as var
from src.c_create_table_by_team import *

for year in var.all_years:
    print(year)
    table_teams = CreateTable(year)
    table_teams.identify_teams_id()
    table_teams.create_table_per_team()
    table_teams.calculate_scores()
    table_teams.write_output()