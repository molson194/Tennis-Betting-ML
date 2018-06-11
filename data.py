import requests
import pickle
from bs4 import BeautifulSoup


def parseProfile(key, value):
    if key == "Age":
        return int(value.split()[0])
    elif key == "Height":
        return int(value.split()[0])
    elif key == "Weight":
        return int(value.split()[0])
    elif key == "Plays":
        return value[:1]
    elif key == "Current Elo Rank":
        return int(value.split()[-1][1:-1])
    elif key == "Overall":
        return float(value.split("%")[0])
    elif key == "Hard":
        return float(value.split("%")[0])
    elif key == "Clay":
        return float(value.split("%")[0])
    elif key == "Grass":
        return float(value.split("%")[0])
    return None


def parsePerformance(key, value):
    keys = ["Deciding Set", "Tie Breaks"]

    if key in keys:
        return float(value.split("%")[0])
    return None


def parseStats(key, value):
    keys = ["Ace %", "Double Fault %", "1st Serve %", "1st Serve Won %",
            "2nd Serve Won %", "Break Points Saved %", "Service Points Won %",
            "Service Games Won %", "Ace Against %", "1st Srv. Return Won %",
            "2nd Srv. Return Won %", "Break Points Won %",
            "Return Points Won %", "Points Dominance", "Games Dominance",
            "Tie Breaks Won %", "Break Points Ratio", "Opponent Elo Rating"]

    if key in keys:
        return float(value.split("%")[0])
    return None


numPlayers = 100
baseUrl = "http://www.ultimatetennisstatistics.com"
playerData = {}  # Dictionary from player ID -> stat -> information
matchData = []  # Array of match data dictionaries

rankingsUrl = "/rankingsTableTable?current=1&rowCount=" + \
    str(numPlayers) + "&rankType=RANK"
rankings = requests.get(baseUrl + rankingsUrl)
players = rankings.json()["rows"]
for player in players:
    playerData[player["playerId"]] = {"name": player["name"]}

for id in playerData.keys():
    profileUrl = "/playerProfileTab?playerId=" + str(id)
    profile = requests.get(baseUrl + profileUrl)
    soup = BeautifulSoup(profile.text, "html5lib")
    for element in soup.find_all('tr'):
        try:
            a = element.find_all(['td', 'th'])
            key = a[0].get_text().strip()
            value = a[1].get_text().strip()
            parseValue = parseProfile(key, value)
            if parseValue:
                playerData[id][key] = parseValue
        except IndexError:
            pass

    performanceUrl = "/playerPerformance?playerId=" + str(id) + "&season=-1"
    performance = requests.get(baseUrl + performanceUrl)
    soup = BeautifulSoup(performance.text, "html5lib")
    for element in soup.find_all('tr'):
        try:
            a = element.find_all(['td', 'th'])
            key = a[0].get_text().strip()
            value = a[1].get_text().strip()
            parseValue = parsePerformance(key, value)
            if parseValue:
                playerData[id][key] = parseValue
        except IndexError:
            pass

    statisticsUrl = "/playerStatsTab?playerId=" + str(id) + "&season=-1"
    statistics = requests.get(baseUrl + statisticsUrl)
    soup = BeautifulSoup(statistics.text, "html5lib")
    for element in soup.find_all('tr'):
        try:
            a = element.find_all(['td', 'th'])
            key = a[0].get_text().strip()
            value = a[1].get_text().strip()
            parseValue = parseStats(key, value)
            if parseValue:
                playerData[id][key] = parseValue
        except IndexError:
            pass

    matchesUrl = "/matchesTable?playerId=" + \
        str(id) + "&current=1&rowCount=-1&season=-1"
    rankings = requests.get(baseUrl + matchesUrl)
    matches = rankings.json()["rows"]
    for match in matches:
        try:
            matchDict = {}
            matchDict["level"] = match["level"]
            matchDict["bestOf"] = match["bestOf"]
            matchDict["surface"] = match["surface"]
            matchDict["indoor"] = match["indoor"]
            matchDict["winnerId"] = match["winner"]["id"]
            matchDict["winnerElo"] = match["winner"]["eloRating"]
            matchDict["loserId"] = match["loser"]["id"]
            matchDict["loserElo"] = match["loser"]["eloRating"]
            matchData.append(matchDict)
        except KeyError:
            pass

matchDataOutput = open('matchData.pkl', 'wb')
pickle.dump(matchData, matchDataOutput)
matchDataOutput.close()

playerDataOutput = open('playerData.pkl', 'wb')
pickle.dump(playerData, playerDataOutput)
playerDataOutput.close()
