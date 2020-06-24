import src.variables as var
from src.d_create_strengths_on_time import *

for year in var.all_years[:]:
    print(year)
    strengths = CalculateStrengthsTime(year)
    mean_home, mean_away = strengths.running_time()
    strengths.calculate_strengths(mean_home, mean_away)
    strengths.save_files(mean_home, mean_away)