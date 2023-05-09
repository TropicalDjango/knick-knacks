#! /usr/bin/env python3

import requests
import lxml.html as lxml
import colorama
from bs4 import BeautifulSoup
from colorama import Fore, Style

page = requests.get("https://www.espn.com/nba/schedule")

team_col = {
    "Atlanta": "\033[1m\033[38;2;255;255;255;48;2;200;16;46m",
    "Boston": "\033[1m\033[38;2;255;255;255;48;2;0;122;51m",
    "Brooklyn": "\033[1m\033[38;2;255;255;255;48;2;0;0;0m",
    "Charlotte": "\033[1m\033[38;2;29;17;96;48;2;0;120;140m",
    "Chicago": "\033[1m\033[38;2;6;25;34;48;2;206;17;65m",
    "Cleveland": "\033[1m\033[38;2;134;0;56;48;2;253;187;48m",
    "Dallas": "\033[1m\033[38;2;187;196;202;48;2;0;43;92m",
    "Denver": "\033[1m\033[38;2;255;198;39;48;2;13;34;64m",
    "Detroit": "\033[1m\033[38;2;200;16;46;48;2;29;66;138m",
    "Golden State": "\033[1m\033[38;2;255;199;44;48;2;29;66;138m",
    "Houston": "\033[1m\033[38;2;206;17;65;48;2;6;25;34m",
    "Indiana": "\033[1m\033[38;2;253;187;48;48;2;0;45;98m",
    "Clippers": "\033[1m\033[38;2;0;0;0;48;2;255;255;255m",
    "Los Angeles": "\033[1m\033[38;2;85;37;130;48;2;253;185;39m",
    "Memphis": "\033[1m\033[38;2;93;118;169;48;2;18;23;63m",
    "Miami": '\033[1m\033[38;2;152;0;26;48;2;255;255;255m',
    "Milwaukee": "\033[1m\033[38;2;240;235;210;48;2;0;71;27m",
    "Minnesota": "\033[1m\033[38;2;35;97;146;48;2;12;35;64m",
    "New Orleans": "\033[1m\033[38;2;180;151;90;48;2;0;22;65m",
    "New York": "\033[1m\033[38;2;245;132;38;48;2;0;107;182m",
    "Oklahoma City": "\033[1m\033[38;2;239;59;36;48;2;0;125;195m",
    "Orlando": "\033[1m\033[38;2;196;206;211;48;2;0;125;197m",
    "Philadelphia": "\033[1m\033[38;2;237;23;76;48;2;0;108;182m",
    "Phoenix": "\033[1m\033[38;2;229;95;32;48;2;29;17;96m",
    "Portland": "\033[1m\033[38;2;224;58;62;48;2;6;25;34m",
    "Sacramento": "\033[1m\033[38;2;255;255;255;48;2;91;43;130m",
    "San Antonio": "\033[1m\033[38;2;0;0;0;48;2;196;206;211m",
    "Toronto": "\033[1m\033[38;2;0;0;0;48;2;206;17;65m",
    "Utah": "\033[1m\033[38;2;249;160;27;48;2;0;43;92m",
    "Washington": "\033[1m\033[38;2;227;24;55;48;2;196;206;212m"
}

def print_game(away, home, game_time, tv_network):
    away = team_col[away] + away.center(15) + Style.RESET_ALL

    home = team_col[home] + home.center(15) + Style.RESET_ALL

    if game_time == "LIVE":
        game_time = Fore.RED + game_time.center(10) + Style.RESET_ALL
    else:
        game_time = game_time.center(10) + Style.RESET_ALL

    tv_network = tv_network.center(5) + Style.RESET_ALL
    print("{}@{}:{}:{}".format(away, home, game_time, tv_network))


def week_schedule():
    tree = lxml.fromstring(page.text)
    elements = tree.find_class("ResponsiveTable")
    for element in elements:
        table = lxml.tostring(element)
        #print(lxml.tostring(element).decode('ascii'))
        day = element.find_class("Table__Title")[0].text_content()
        
        print(day.center(40, "_"))

        games = element.find_class("Table__TBODY")[0]
        for single_game in games.find_class("Table__TR--sm"):
            away_team = single_game.find_class("events__col")[0].\
                                    find_class("AnchorLink")[1].text_content()

            home_team = single_game.find_class("colspan__col")[0].\
                                    find_class("AnchorLink")[1].text_content()
            try:
                game_time = single_game.find_class("date__col")[0].\
                                        find_class("AnchorLink")[0].text_content()
            except IndexError:
                game_time = "LIVE"

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
                    tv_net = ""

            series_lead = single_game.find_class("events__col")[0].\
                                      find_class("gameNote")[0].text_content()
            print_game(away_team, home_team, game_time, tv_net)
        print('\n')


if __name__ == "__main__":
    week_schedule()

