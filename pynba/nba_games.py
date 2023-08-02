#! /usr/bin/env python3

import requests
import lxml.html as lxml
import datetime
import readline
import argparse
from team_colors import *
from subprocess import run
from bs4 import BeautifulSoup
from colorama import Fore, Style


def team_schedule(url):
    pass


"""
This is to print a single game line
    @param  away        the name of the away team
    @param  home        the name of the home team
    @param  game_time   either the game results or the time it starts in EST
    @param  tv_network  the tv network the game is being shown on
"""


def print_game(away, home, game_time, tv_network):
    # This causes teams not in team_col to be displayed as black on white
    away = str(team_col.get(away) or team_col["Unknown"]) +\
                                     away.center(15) + Style.RESET_ALL
    home = str(team_col.get(home) or team_col["Unknown"]) +\
                                    home.center(15) + Style.RESET_ALL
    if game_time == "LIVE":
        game_time = Fore.RED + "  ● LIVE  " + Style.RESET_ALL
    elif len(game_time) > 8 and game_time != "Postponed":
        game_time = Fore.GREEN + game_time.split(" ")[0] + "-" +\
                                     game_time.split(" ")[1] + Fore.RED +\
                                     game_time.split(" ")[2] + "-" +\
                                     game_time.split(" ")[3] + Style.RESET_ALL
        game_time = ''.join(game_time)
    else:
        game_time = game_time.center(12) + Style.RESET_ALL

    # This means tv_network is the series lead of a playoff game
    if len(tv_network) > 5:
        print("{}@{}:{}".format(away, home, game_time))
        tv_network = tv_network + Style.RESET_ALL
        print(tv_network)
    else:
        tv_network = tv_network.center(6) + Style.RESET_ALL
        print("{}@{}:{}:{}".format(away, home, game_time, tv_network))


def get_day_table(single_game):
    try:
        away_team = single_game.find_class("events__col")[0].\
                                find_class("AnchorLink")[1].text_content()
    except IndexError:
        away_team = single_game.find_class("events__col")[0].text_content()
    try:
        home_team = single_game.find_class("colspan__col")[0].\
                                find_class("AnchorLink")[1].text_content()
    except IndexError:
        home_team = single_game.find_class("colspan__col")[0].\
                                find_class("Table__Team")[0].text_content()
    try:
        if single_game.find_class("date__col") == []:
            game_or_time = single_game.find_class("teams__col")[0].\
                                    find_class("AnchorLink")[0].text_content()
        else:
            game_or_time = single_game.find_class("date__col")[0].\
                                    find_class("AnchorLink")[0].text_content()
    except IndexError:
        game_or_time = "LIVE"
    try:
        tv_net = single_game.find_class("broadcast__col")[0].\
                             find_class("network-name")[0].text_content()
    except IndexError:
        try:
            tv_net = single_game.find_class("broadcast__col")[0]\
                                     .find_class("")[0]
            tv_net = lxml.tostring(tv_net).decode('ascii')
            soup = BeautifulSoup(tv_net, 'lxml')
            for img_tag in soup.find_all('img'):
                tv_net = img_tag.get('alt')
        except IndexError:
            try:
                tv_net = single_game.find_class("gameNote")[0].text_content()
            except IndexError:
                tv_net = ""
    return [away_team, home_team, game_or_time, tv_net]


"""
This is to collect the information for all the games in a given week
The ESPN webpage is structured like this
|------Day-----|    |-----Games-----|    |-Day/Title-|     |----Data----|
<ScheduleTables> -> <ResponsiveTable> -> <Table_Title>
                                      -> <Table__TBODY> -> <-events__col-->
                                                        -> <-colspan__col->
                                                        -> <--date__col--->
                                                        -> <broadcast__col>
There is a different ResponsiveTable depending on wheater the game finished.
events_col has the away team, colspan_col has the home team, date_col has the
time, broadcast__col has the tv_network
    @param  url   the espn url to get the game details
"""


def get_week_schedule(url):
    print(url)
    page = requests.get(url)
    tree = lxml.fromstring(page.text)
    elements = tree.find_class("ScheduleTables")
    for element in elements:
        day = element.find_class("Table__Title")
        if isinstance(day, list):
            day = day[0].text_content()
        else:
            day = day.text_content()
        print('\n\033[1m' + day.center(54, "_"))
        for table in element.find_class("ResponsiveTable"):
            games = table.find_class("Table__TBODY")[0]
            for single_game in games.find_class("Table__TR--sm"):
                game_info = get_day_table(single_game)
                print_game(game_info[0], game_info[1],
                           game_info[2], game_info[3])


"""
This is just for testing
"""


def test_teams(team_col):
    for team in team_col:
        print_game(team, team, "LIVE", "ESPN")
    print('\n\n')
    exit(0)


def get_selected_week(factor, base_url):
    today = datetime.datetime.now()
    today += datetime.timedelta(days=7*factor)
    dt_string = today.strftime("%Y%m%d")
    url = base_url + "/_/date/" + dt_string
    print('\n' + 'Week {}'.format(factor).center(54, '-'))
    get_week_schedule(url)


if __name__ == "__main__":
    options = ["This Week", "Last Week", "Next Week", "Exit"]
    arguments = argparse.ArgumentParser(
        description="This program can display the nba game schdule for a given week"
    )

    arguments.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="enter interactive mode",
    )

    arguments.add_argument(
        "-l",
        "--league",
        type=str,
        nargs=1,
        metavar=["('NBA', 'NHL', 'NFL')"],
        default=["NBA"],
        help="enter a sports league form the available options"
    )

    arguments.add_argument(
        "-w",
        "--week",
        type=int,
        nargs=1,
        metavar=['week_number'],
        default=[0],
        help="enter a index of week you want to see from current"
    )

    arguments.add_argument(
        "-r",
        "--range",
        type=int,
        nargs=2,
        metavar=['week1', 'week2'],
        help="enter two relative week number and get all games between them"
    )

    arguments.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="enter two relative week number and get all games between them"
    )

    arguments.add_argument(
        "-e",
        "--experiment",
        action="store_true",
        help="instead of selecting from the preset leagues type a league" +
            " and see if it works"
    )

    flags = arguments.parse_args()
    today = datetime.datetime.now()

    if flags.experiment:
        base_url = "https://www.espn.com/" + flags.league[0].lower() +\
                   "/schedule"
        team_col = team_col_NBA
    else:
        match flags.league[0].upper():
            case "NBA":
                base_url = "https://www.espn.com/nba/schedule"
                team_col = team_col_NBA
            case "NFL":
                base_url = "https://www.espn.com/nfl/schedule"
                team_col = team_col_NFL
            case "NHL":
                base_url = "https://www.espn.com/nhl/schedule"
                team_col = team_col_NHL
            case "MLB":
                base_url = "https://www.espn.com/mlb/schedule"
                team_col = team_col_MLB

    if flags.test:
        test_teams(team_col)
        exit(0)

    index = 0
    while flags.interactive:
        print("Select an option from below".center(54, "_"))
        print("1:{}\n2:{}\n3:{}\n4:{}\n".format(options[0], options[1],
                                                options[2], options[3]))
        user_input = int(input("-> "))
        run(["clear"])
        match user_input:
            case 1:
                index = 0
            case 2:
                index -= 1
            case 3:
                index += 1
            case 4:
                exit(0)
        get_selected_week(index, base_url)

    if flags.range is not None:
        for ii in range(flags.range[0], flags.range[1] + 1):
            get_selected_week(ii, base_url)
    else:
        get_selected_week(flags.week[0], base_url)
