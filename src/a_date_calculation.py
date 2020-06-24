from datetime import date, timedelta, datetime

import pandas as pd


def find_first_tuesday(first_game: date):
    day_first_game = date(first_game.year, first_game.month, first_game.day).weekday()
    print(day_first_game)
    if day_first_game > 1:
        diff_day = day_first_game - 1
    else:
        diff_day = 6
    first_tuesday = date(first_game.year, first_game.month, first_game.day - diff_day)
    return first_tuesday


def daterange(start_date, end_date):
    for n in range(0, int((end_date - start_date).days) + 1, 7):
        yield start_date + timedelta(n)


def create_list_tuesdays(first_tuesday: date, game_date: list) -> list:
    list_tuesdays = []
    last_day = date(game_date[-1].year, game_date[-1].month, game_date[-1].day + 7)
    for dt in daterange(first_tuesday, last_day):
        list_tuesdays.append(dt)
    print(list_tuesdays)
    return list_tuesdays


def index_week(list_tuesdays: list, game_date: list):
    list_couple = []
    couple = ()
   # print(len(game_date))
    for index in range(len(list_tuesdays)):
       # print(index)
        if index >= 1:
            count = 0
            j=0
            for game in game_date:
                if (list_tuesdays[index - 1] <= game) and (game < list_tuesdays[index]):

                    count += 1
                    print(index, j, list_tuesdays[index - 1], "___", game, "___", list_tuesdays[index], "___", count)
                j=j+1
            couple = (list_tuesdays[index], count)
        list_couple.append(couple)
    suma = 0

    for item in list_couple:
        print(item)
        if item:
            if item[1] == 0:
                list_couple.remove(item)
            if item[0] == None:
                list_couple.remove(item)

            if type(item[1]) == int:
                suma = suma + item[1]
    print(suma)
    return list_couple
