#! /usr/bin/env python3

import requests
import lxml.html as lxml
import colorama
from bs4 import BeautifulSoup
from colorama import Fore, Style

page = requests.get("https://www.espn.com/nba/schedule")

nba_teams = {
    "Atlanta": ["#E03A3E", "#C1D32F"],
    "Boston": ["#007A33", "#BA9653"],
    "Brooklyn": ["#000000", "#FFFFFF"],
    "Charlotte": ["#1D1160", "#00788C"],
    "Chicago": ["#CE1141", "#000000"],
    "Cleveland": ["#6F263D", "#041E42"],
    "Dallas": ["#00538C", "#002B5E"],
    "Denver": ["#0E2240", "#FEC524"],
    "Detroit": ["#C8102E", "#1D42BA"],
    "Golden State": ["#1D428A", "#FFC72C"],
    "Houston": ["#CE1141", "#C4CED3"],
    "Indiana": ["#002D62", "#FDBB30"],
    "LA Clippers": ["#C8102E", "#1D428A"],
    "LA Lakers": ["#552583", "#FDB927"],
    "Memphis": ["#5D76A9", "#12173F"],
    "Miami": ["#98002E", "#F9A01B"],
    "Milwaukee": ["#00471B", "#F0EBD2"],
    "Minnesota": ["#0C2340", "#236192"],
    "New Orleans": ["#0C2340", "#85714D"],
    "New York": ["#006BB6", "#F58426"],
    "Oklahoma City": ["#007AC1", "#EF3B24"],
    "Orlando": ["#0077C0", "#C4CED3"],
    "Philadelphia": ["#006BB6", "#ED174C"],
    "Phoenix": ["#1D1160", "#E56020"],
    "Portland": ["#E03A3E", "#000000"],
    "Sacramento": ["#5A2D81", "#63727A"],
    "San Antonio": ["#C4CED3", "#000000"],
    "Toronto": ["#CE1141", "#000000"],
    "Utah": ["#002B5C", "#F9A01B"],
    "Washington": ["#002B5C", "#E31837"]
}

teams = {
    "Atlanta": "#E03A3E",
    "Boston": "#007A33",
    "Brooklyn": "#000000",
    "Charlotte": "#1D1160",
    "Chicago": "#CE1141",
    "Cleveland": "#6F263D",
    "Dallas": "#00538C",
    "Denver": "#0E2240",
    "Detroit": "#C8102E",
    "Golden State": "#1D428A",
    "Houston": "#CE1141",
    "Indiana": "#00275D",
    "Clippers": "#C8102E",
    "Lakers": "#552583",
    "Memphis": "#5D76A9",
    "Miami": "#98002E",
    "Milwaukee": "#00471B",
    "Minnesota": "#0C2340",
    "New Orleans": "#0C2340",
    "New York": "#006BB6",
    "Oklahoma City": "#007AC1",
    "Orlando": "#0077C0",
    "Philadelphia": "#006BB6",
    "Phoenix": "#1D1160",
    "Portland": "#E03A3E",
    "Sacramento": "#5A2D81",
    "San Antonio": "#C4CED4",
    "Toronto": "#CE1141",
    "Utah": "#002B5C",
    "Washington": "#002B5C"
}

def todays_game():
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

            game_time = single_game.find_class("date__col")[0].\
                                    find_class("AnchorLink")[0].text_content()

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

            print("{} @ {} : {} : {}".format(away_team, home_team, \
                                             game_time, tv_net))


if __name__ == "__main__":
    print("Options".center(40, "_"))
    #choice = input("-> ")
    todays_game()
