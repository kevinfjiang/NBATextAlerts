"""
This file contains constants. Please fill them out first so your code works properly
Specify, player, event, and their team

If something is wrong, it's probably in the path finding for specific folders

This is my first public project, thank you for taking a look. This is me testing
out webscraping and Crontab.

During each basketball game, a new terminal will open. If you would like to exit the bot,
type 'yes' into it.

Don't forget to input your phone number and tokens into Alerts.py
"""

from pathlib import Path
import sys
#Input player name, event you want to be alerted about(see dictionary below) and team name
#Only change these values and dictionary if you want the bot to work properly
player_full_name = "Giannis Antetokounmpo"
event = "Scores"
team = "Milwaukee Bucks"



# Dictionary to modify the criteria, based on the ESPN play-by-play
# for example, a player making a 3 pointer will always be "[playername] makes"
# and a little later it will say "three point". This dictionary is like a glossary
# for what comes adjacent to player name and what is aalways contained
eventkey = {"2 pointer": [" makes", "two point"],
            "3 pointer": [" makes", "three point"],
            "Scores": [" makes",""],
            "Rebound":["", "Rebound"]
            }

#How the dictionary will be used. This allows the program to search sharper
PLAYER = player_full_name + eventkey[event][0]
EVENT = eventkey[event][1]
TEAM = team


"""Constants to not change, don't touch these!"""
def getPath(Address):
    if Address == 'PYTHON':
        return sys.executable
    elif Address == 'botHelper' or Address == 'scraper':
        fileHelper = {
            'botHelper': "/botHelper.py",
            'scraper': "/NBA/NBA/"
        }
        return getDirectory('NBATextAlerts/') + fileHelper[Address]
    else:
        return getDirectory(Address)


def getDirectory(file):
    p = Path('/Users/')
    return str(list(p.glob('**/{}'.format(file)))).split("'")[1]
