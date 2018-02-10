#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Zak
#
# Created:     09-02-2018
# Copyright:   (c) Zak 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import requests
import datetime
import time
import sys
from bs4 import BeautifulSoup

pairings_url_base = "https://magic.wizards.com/en/events/coverage/gphou18/round-"
standings_url_base = "https://magic.wizards.com/en/events/coverage/gphou18/round-"
players = ["Nadeau", "Blum"]
player_points = {}
#today = datetime.datetime.now()
today = datetime.datetime(2018, 1, 27)


def main():
    current_round = 1 if today.weekday() == 5 else 10;
    max_rounds = 10 if today.weekday() == 5 else 15
    while current_round <= max_rounds:
        while get_pairings(current_round) == False:
            time.sleep(10)
        while get_standings(current_round) == False:
            time.sleep(10)
        current_round += 1


def get_standings(round):

    standings_url = standings_url_base + str(round) + "-standings-" + str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2)
    response = requests.get(standings_url)
    if response.status_code == 404:
        return False
    print "Results for round " + str(round)

    html = response.text
    parsedhtml = BeautifulSoup(html, 'html.parser')
    table = parsedhtml.select("table.sortable-table tr")
    standings = []
    for row in table:
        try:
            rank = row.find_all("td")[0].get_text()
            player = row.find_all("td")[1].get_text()
            points = row.find_all("td")[2].get_text()
            for target_player in players:
                if target_player in player:
                    standings.append("Rank " + rank + ": " + player + " - " + points + " points")
                    if int(points) == player_points.get(target_player, 0) + 3:
                        print target_player + " WINS"
                    elif int(points) == player_points.get(target_player, 0) + 1:
                        print target_player + " DRAWS"
                    else:
                        print target_player + " LOSES"
                    player_points[target_player] = int(points)


        except IndexError:
            pass
    print "\nStandings after round " + str(round)
    for standing in standings:
        print standing
    print "\n"

def get_pairings(round):
    pairings_url = pairings_url_base + str(round) + "-pairings-" + str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2)
    response = requests.get(pairings_url)
    if response.status_code == 404:
        return False
    print "Pairings for round " + str(round)
    html = response.text
    parsedhtml = BeautifulSoup(html, 'html.parser')
    table = parsedhtml.select("table.sortable-table tr")

    for row in table:
        try:
            table_number = row.find_all("td")[0].get_text()
            p1 = row.find_all("td")[1].get_text()
            p2 = row.find_all("td")[4].get_text()
            for player in players:
                if player in p1 or player in p2:
                    print "Table " + table_number + ": " + p1 + " vs " + p2
        except Exception:
            pass


if __name__ == '__main__':
    main()
