import requests
import pickle
import os.path
from datetime import date, timedelta
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from predict import predict


def convertMoneyLine(input):
    if input > 0:
        return 100 / (100 + input)
    return (0 - input) / (100 - input)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


lines = requests.get("http://lines.bookmaker.eu/")
tree = ElementTree.fromstring(lines.content)

playerDataInput = open('playerData.pkl', 'rb')
playerData = pickle.load(playerDataInput)
playerDataInput.close()

if os.path.isfile('lines.pkl'):
    linesInput = open('lines.pkl', 'rb')
    lines = pickle.load(linesInput)
    linesInput.close()
else:
    lines = {}

if os.path.isfile('returns.pkl'):
    returnsOutput = open('returns.pkl', 'rb')
    returns = pickle.load(returnsOutput)
    returnsOutput.close()
else:
    returns = 0

baseUrl = "http://www.espn.com/tennis/dailyResults?matchType=msingles&date="
for gmdt in lines:
    results = requests.get(baseUrl + gmdt)
    soup = BeautifulSoup(results.text, "html5lib")
    matches = soup.findAll("div", {"class": "matchContainer"})
    for match in matches:
        p1 = match.find('td', {'class': 'teamLine'})
        p2 = match.find('td', {'class': 'teamLine2'})

        winner = ""
        loser = ""
        winnerLine = ""
        loserLine = ""
        lineIndex = -1
        lineId = ""
        winnerId = 0
        loserId = 0

        if p1.find("div", {"class": "arrowWrapper"}):
            winner = p1.text
            loser = p2.text
        elif p2.find("div", {"class": "arrowWrapper"}):
            winner = p2.text
            loser = p1.text

        for i in range(0, len(lines[gmdt].copy())):
            wp1 = similar(winner, lines[gmdt][i]['p1']) > 0.6
            wp2 = similar(winner, lines[gmdt][i]['p2']) > 0.6
            lp1 = similar(loser, lines[gmdt][i]['p1']) > 0.6
            lp2 = similar(loser, lines[gmdt][i]['p2']) > 0.6
            if ((wp1 and lp2) or (wp2 and lp1)):
                lineIndex = i
                if wp1:
                    lineId = "odds1"
                    winnerLine = lines[gmdt][i]['p1']
                    loserLine = lines[gmdt][i]['p2']
                elif wp2:
                    lineId = "odds2"
                    winnerLine = lines[gmdt][i]['p2']
                    loserLine = lines[gmdt][i]['p1']
                for id in playerData:
                    if (similar(winner, playerData[id]['name']) > 0.6):
                        winnerId = id
                    elif (similar(loser, playerData[id]['name']) > 0.6):
                        loserId = id

        if (
            (winner != "") and (loser != "") and (winnerLine != "") and
            (loserLine != "") and (winnerId != 0) and (loserId != 0)
        ):
            pred = predict(winnerId, loserId)
            line = lines[gmdt][lineIndex][lineId]
            returns += pred - line
            lines[gmdt].pop(lineIndex)

for league in tree[0]:
    if league.attrib['IdLeague'] == '12331':
        newDates = []

        for element in league:
            if element.tag == 'game':
                gmdt = element.attrib['gmdt']
                p1 = element.attrib['vtm']
                p2 = element.attrib['htm']
                odds1 = convertMoneyLine(int(element[0].attrib['voddst']))
                odds2 = convertMoneyLine(int(element[0].attrib['hoddst']))

                value = {'p1': p1, 'p2': p2, 'odds1': odds1, 'odds2': odds2}

                if gmdt not in lines:
                    newDates.append(gmdt)
                    lines[gmdt] = [value]
                elif gmdt in newDates:
                    lines[gmdt].append(value)

oldDate = date.today() - timedelta(5)
oldDateInt = int(oldDate.strftime("%Y%m%d"))
for gmdt in lines.copy():
    if int(gmdt) < oldDateInt:
        lines.pop(gmdt)

print(returns)

linesOutput = open('lines.pkl', 'wb')
pickle.dump(lines, linesOutput)
linesOutput.close()

returnsOutput = open('returns.pkl', 'wb')
pickle.dump(returns, returnsOutput)
returnsOutput.close()
