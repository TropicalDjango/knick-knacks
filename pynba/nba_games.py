#! /usr/bin/env python3

import requests
import lxml.html as lxml
import datetime
from subprocess import run
from bs4 import BeautifulSoup
from colorama import Fore, Style

"""
These are the ANSI color codes for the teams, I used
https://teamcolorcodes.com/nba-team-color-codes/ for the RGB values

the format is as follows

bold          Foreground   Background
|_____|     |____________|____________|
\033[1m \033[38;2;{R:G:B};48;2;{R:G:B}m

"""

team_col_away = {
    "Atlanta":          "\033[1m\033[38;2;253;185;39;48;2;200;16;46m",
    "Boston":           "\033[1m\033[38;2;255;255;255;48;2;0;122;51m",
    "Brooklyn":         "\033[1m\033[38;2;255;255;255;48;2;0;0;0m",
    "Charlotte":        "\033[1m\033[38;2;255;255;255;48;2;29;17;96m",
    "Chicago":          "\033[1m\033[38;2;255;255;255;48;2;206;17;65m",
    "Cleveland":        "\033[1m\033[38;2;253;187;48;48;2;134;0;56m",
    "Dallas":           "\033[1m\033[38;2;255;255;255;48;2;0;83;188m",
    "Denver":           "\033[1m\033[38;2;255;198;39;48;2;13;34;64m",
    "Detroit":          "\033[1m\033[38;2;237;23;76;48;2;0;45;98m",
    "Golden State":     "\033[1m\033[38;2;255;199;44;48;2;29;66;138m",
    "Houston":          "\033[1m\033[38;2;196;206;211;48;2;186;12;47m",
    "Indiana":          "\033[1m\033[38;2;253;187;48;48;2;0;45;98m",
    "Clippers":         "\033[1m\033[38;2;200;16;46;48;2;255;255;255m",
    "Los Angeles":      "\033[1m\033[38;2;253;185;39;48;2;85;37;130m",
    "Memphis":          "\033[1m\033[38;2;93;118;169;48;2;18;23;63m",
    "Miami":            '\033[1m\033[38;2;255;255;255;48;2;152;0;46m',
    "Milwaukee":        "\033[1m\033[38;2;240;235;210;48;2;0;71;27m",
    "Minnesota":        "\033[1m\033[38;2;35;97;146;48;2;12;35;64m",
    "New Orleans":      "\033[1m\033[38;2;180;151;90;48;2;0;22;65m",
    "New York":         "\033[1m\033[38;2;245;132;38;48;2;0;107;182m",
    "Oklahoma City":    "\033[1m\033[38;2;240;70;40;48;2;0;110;180m",
    "Orlando":          "\033[1m\033[38;2;196;206;211;48;2;0;125;197m",
    "Philadelphia":     "\033[1m\033[38;2;255;255;255;48;2;0;47;108m",
    "Phoenix":          "\033[1m\033[38;2;229;95;32;48;2;29;17;96m",
    "Portland":         "\033[1m\033[38;2;0;0;0;48;2;224;58;62m",
    "Sacramento":       "\033[1m\033[38;2;255;255;255;48;2;91;43;130m",
    "San Antonio":      "\033[1m\033[38;2;6;25;34;48;2;196;206;211m",
    "Toronto":          "\033[1m\033[38;2;6;25;34;48;2;206;17;65m",
    "Utah":             "\033[1m\033[38;2;249;160;27;48;2;0;43;92m",
    "Washington":       "\033[1m\033[38;2;0;43;92;48;2;227;24;4m"
}

team_col_home = {
    "Atlanta":          "\033[1m\033[38;2;253;185;39;48;2;200;16;46m",
    "Boston":           "\033[1m\033[38;2;255;255;255;48;2;0;122;51m",
    "Brooklyn":         "\033[1m\033[38;2;255;255;255;48;2;0;0;0m",
    "Charlotte":        "\033[1m\033[38;2;255;255;255;48;2;29;17;96m",
    "Chicago":          "\033[1m\033[38;2;255;255;255;48;2;206;17;65m",
    "Cleveland":        "\033[1m\033[38;2;253;187;48;48;2;134;0;56m",
    "Dallas":           "\033[1m\033[38;2;255;255;255;48;2;0;83;188m",
    "Denver":           "\033[1m\033[38;2;255;198;39;48;2;13;34;64m",
    "Detroit":          "\033[1m\033[38;2;237;23;76;48;2;0;45;98m",
    "Golden State":     "\033[1m\033[38;2;255;199;44;48;2;29;66;138m",
    "Houston":          "\033[1m\033[38;2;196;206;211;48;2;186;12;47m",
    "Indiana":          "\033[1m\033[38;2;253;187;48;48;2;0;45;98m",
    "Clippers":         "\033[1m\033[38;2;200;16;46;48;2;255;255;255m",
    "Los Angeles":      "\033[1m\033[38;2;253;185;39;48;2;85;37;130m",
    "Memphis":          "\033[1m\033[38;2;93;118;169;48;2;18;23;63m",
    "Miami":            '\033[1m\033[38;2;255;255;255;48;2;152;0;46m',
    "Milwaukee":        "\033[1m\033[38;2;240;235;210;48;2;0;71;27m",
    "Minnesota":        "\033[1m\033[38;2;35;97;146;48;2;12;35;64m",
    "New Orleans":      "\033[1m\033[38;2;180;151;90;48;2;0;22;65m",
    "New York":         "\033[1m\033[38;2;245;132;38;48;2;0;107;182m",
    "Oklahoma City":    "\033[1m\033[38;2;240;70;40;48;2;0;110;180m",
    "Orlando":          "\033[1m\033[38;2;196;206;211;48;2;0;125;197m",
    "Philadelphia":     "\033[1m\033[38;2;255;255;255;48;2;0;47;108m",
    "Phoenix":          "\033[1m\033[38;2;229;95;32;48;2;29;17;96m",
    "Portland":         "\033[1m\033[38;2;0;0;0;48;2;224;58;62m",
    "Sacramento":       "\033[1m\033[38;2;255;255;255;48;2;91;43;130m",
    "San Antonio":      "\033[1m\033[38;2;6;25;34;48;2;196;206;211m",
    "Toronto":          "\033[1m\033[38;2;6;25;34;48;2;206;17;65m",
    "Utah":             "\033[1m\033[38;2;249;160;27;48;2;0;43;92m",
    "Washington":       "\033[1m\033[38;2;0;43;92;48;2;227;24;4m"
}


"""
This is to print a single game line
    @param  away        the name of the away team
    @param  home        the name of the home team
    @param  game_time   either the game results or the time it starts in EST
    @param  tv_network  the tv network the game is being shown on
"""


def print_game(away, home, game_time, tv_network):
    away = team_col_away[away] + away.center(15) + Style.RESET_ALL
    home = team_col_home[home] + home.center(15) + Style.RESET_ALL
    if game_time == "LIVE":
        game_time = Fore.RED + "  ● LIVE  " + Style.RESET_ALL
    else:
        game_time = game_time.center(10) + Style.RESET_ALL
    if len(tv_network) > 5:
        print("{}@{}:{}".format(away, home, game_time))
        tv_network = tv_network + Style.RESET_ALL
        print(tv_network)
    else:
        tv_network = tv_network.center(6) + Style.RESET_ALL
        print("{}@{}:{}:{}".format(away, home, game_time, tv_network))


"""
This is to collect the information for all the games in a given week
The ESPN webpage is structured like this

|------Day-----|    |-----Games-----|    |-Day/Title-|     |----Data----|
<ScheduleTables> -> <ResponsiveTable> -> <Table_Title>
                                      -> <Table__TBODY> -> <-events__col-->
                                                        -> <-colspan__col->
                                                        -> <--date__col--->
                                                        -> <broadcast__col>
There is a different ResponsiveTable depending on wheater or the game finished
or nor. events_col has the away team, colspan_col has the home team, date_col
has the time, broadcast__col has the tv_network

    @param  url   the espn url to get the game details
"""


def week_schedule(url):
    run(["clear"])
    page = requests.get(url)
    tree = lxml.fromstring(page.text)
    elements = tree.find_class("ScheduleTables")
    for element in elements:
        #print(lxml.tostring(element).decode('ascii'))
        day = element.find_class("Table__Title")
        if isinstance(day, list):
            day = day[0].text_content()
        else:
            day = day.text_content()
        print('\n')
        print(day.center(54, "_"))
        for table in element.find_class("ResponsiveTable"):
            games = table.find_class("Table__TBODY")[0]
            for single_game in games.find_class("Table__TR--sm"):
                away_team = single_game.find_class("events__col")[0].\
                                        find_class("AnchorLink")[1].text_content()

                home_team = single_game.find_class("colspan__col")[0].\
                                        find_class("AnchorLink")[1].text_content()
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
                        tv_net = single_game.find_class("broadcast__col")[0].\
                            find_class("")[0]
                        tv_net = lxml.tostring(tv_net).decode('ascii')
                        soup = BeautifulSoup(tv_net, 'lxml')
                        for img_tag in soup.find_all('img'):
                            tv_net = img_tag.get('alt')
                    except IndexError:
                        try:
                            tv_net = single_game.find_class("gameNote")[0].\
                               text_content()
                        except IndexError:
                            tv_net = ""

                series_lead = single_game.find_class("events__col")[0].\
                                          find_class("gameNote")[0].text_content()
                print_game(away_team, home_team, game_or_time, tv_net)
            print(''.center(54, '-'))


"""
This is just for testing
"""


def test_teams(time, network):
    for team in team_col_home:
        print_game(team, team, time, network)
    print('\n\n')
    exit(0)

if __name__ == "__main__":
    base_url = "https://www.espn.com/nba/schedule"
    options = ["This Week", "Last Week", "Next Week", "Exit"]
    while 1:
        print("Select an option from below".center(54, "_"))
        print("1:{}\n2:{}\n3:{}\n4:{}\n".format(options[0], options[1],
                                                options[2], options[3]))
        user_input = int(input("-> "))
        today = datetime.datetime.now()
        match user_input:
            case 1:
                week_schedule(base_url)
            case 2:
                today -= datetime.timedelta(days=7)
                dt_string = today.strftime("%Y%m%d")
                url = base_url + "/_/date/" + dt_string
                week_schedule(url)
            case 3:
                today += datetime.timedelta(days=7)
                dt_string = today.strftime("%Y%m%d")
                url = base_url + "/_/date/" + dt_string
                week_schedule(url)
            case 4:
                exit(0)
        
