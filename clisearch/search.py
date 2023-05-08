#! /usr/bin/env python3

from __future__ import unicode_literals
import readline
import requests
import bs4
from colorama import Fore, Style
from googlesearch import search
google_search_url = 'https://duckduckgo.com/?q='


def open_link(url):
    print("url: {}".format(url))
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.text, "html.parser")
    print(soup)
    headers = soup.find_all('h1')
    for info in headers:
        print(info.getText())
        print("--------------")
    return


if __name__ == "__main__":
    ii = 1
    search_results = []
    print(Fore.GREEN + "Google Search".center(40, "_") + Style.RESET_ALL)
    while True:
        print("Enter Search Term".center(40, "_"))
        query = input("->")
        for jj in search(query, tld="co.in", num=10, stop=10, pause=2):
            print(str(ii) + ":" + jj)
            search_results.append(jj)
            ii += 1
        usr = input("Select a link: ")
        open_link(search_results[int(usr)-1])
