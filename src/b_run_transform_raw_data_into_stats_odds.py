import src.variables as var
from src.b_transform_raw_data import TransformRawData, MapOdss

header_odds = []
for year in var.all_years:
    print(year)
    filter = TransformRawData(var.input_raw, year, header_odds)
    filter.read_map_team_file()
    filter.create_stats_odds_games()
    header_odds = filter.map_header_odds()

for year in var.all_years:
    normalize = MapOdss(year, filter.header_odds)
    normalize.verify_header()
    normalize.save_files()
