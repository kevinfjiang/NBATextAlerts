# NBATextAlerts  
**Notifies user when Ben Simmons (or any player) shoots a 3 (or any other statistic)**

Hi r/NBA,

TL:DR; I created a program that automatically texts you 
whenever Ben Simmons makes a 3 and it runs every 76ers game. Last week Ben Simmons made
a 3, and I don't have time to watch every 76ers game waiting 
for him to hit another. Thus, I created a bot that will automatically
text me ~~when~~ if he makes a 3 again. I created this at the request of my brother.

<span style="background-color: #FFFF00">This code only works for Mac, sorry!</span>

## 0. Install packages, Run:
Download the entire repository and unzip. Place the folder NBATextAlerts where ever

    pip install -r requirements.txt

Also, install [chromedriver](https://chromedriver.chromium.org/downloads) for the latest version of chrome

## 1. Text Messaging Set Up: 
[Twilio Link](https://www.twilio.com/)  
First sign up for a Twilio account, input 
your email and phone number.   
You can fill out random stuff for the information about 
the project. You can only text one number per account,
so to text multiple people, you gotta sign up multiple times


Note: You have a limit to the number of texts. You get allocated 14 dollars and each text "costs"
.07 cents, so you get 200 texts per account (more than enough for me)

Now after you sign up go to the home tab in the top left and click Dashboard. 
Create a new phone number, and you should see something similar. Then open <span style="background-color: #FFFF00">Alerts.py</span>,
in the NBATextAlerts Folder and add the <span style="background-color: #FFFF00">ACCOUNT SID</span>, <span style="background-color: #FFFF00">AUTH TOKEN</span>, and <span style="background-color: #FFFF00">PHONE NUMBER</span> 
according to Alerts.py. See below for more information

<img src="https://github.com/kevinjiang019/NBATextAlerts/blob/c300dd4abe7a7df69d9a21f65be7e16ef8a1c795/Twilio%20%202.png" height="480" width="400" class="center">

## 2. Player and Event set up:
Open <span style="background-color: #FFFF00">PATH.py</span> in NBATextAlerts. Add the full name (with proper capitalization) and the event
to happen (ie 3 pointer, rebounds etc). Add to the dictionary for custom events based on the espn play by play text so check you have to check
out prior espn play-by-plays. Check out later in the text to figure find what the connstants that the web scraper will be searched for labled 
<span style="background-color: #FFFF00">PLAYER</span>, <span style="background-color: #FFFF00">EVENT</span>, <span style="background-color: #FFFF00">TEAM</span> in <span style="background-color: #FFFF00">PATH.py</span>.


## 3. Schedule Set Up:
Once all that is taken care of, and you're in the NBATextAlerts directory run: 

    python setup.py  
Here's what it does:  

1. Runs a web scraper(spider) that collects all nba team schedules and start and approximate end times and puts them in a folder on the desktop called "Nba Schedules"
2. Creates a cronjob to update these schedules weekly (On sunday at 11 am, which is changeable)
3. Creates a cronjob to run gameCheckBot.py daily at 11 am.


## 3b Inputs during game day:
While the code is running, it will ask you if you wanna "break loop" in the new opened terminal. Input yes to manually terminate the program.
Otherwise, it will auto terminate after the expected end game time.

If all you want are text alerts and you set everything up. You're all done. Assuming you set up Twilio properly, you will receive automated text alerts whenever your 
player does the specified action. You may ignore the rest

## π. How it works:
I'm a student, so I will explain my design decisions by file going by file.
I used crontab to automate this task mostly. 

**PATH.py**  
  Houses all the constants(player name, event)used and paths to files. For certain files, such as python or the directory location,
PATH.py will run a function to find the path, so you can store NBATextAlerts theoretically anywhere.

**setup.py**    
setup.py just creates the cronjobs aforementioned. It also runs a spider that collects NBA schedules which we will discuss next

**NBA.NBA.spiders.espn_spidery.py**  
This scrapes all "https://www.espn.com/nba/team/schedule/_/name/" for all teams and creates a folder of csvs
on your desktop of all schedules. It does this using scrapy and since the espn site is well formatted, grabs rows
and puts the locations into the csv cells. The start time, date, and link are self-explanatory, but the end time is
the start time + 2h45m since that's the length of a basketball game + overtime.

**botHelper.py**  
setup.py also runs botHelper.py daily. Everyday, botHelper.py checks if there's a game for the specified team.
If there is based on the csv file for the team, it collects the row for today's game and processes the info. It then will 
create a cronjob for the start time of the game. It then closes. Then, when it's time for the game, the cronjob will use botHelper.py
and will see the game has started, thus deploying gameCheckBot.py. It will also remove the cronjob when the bot deploys so every day, the only cronjobs
are the ones from **setup.py**. The cronjob will open a new terminal as cronjob doesn't handle input/outputs well, so don't be surprised.

**gameCheckBot.py**  
Here's the bulk. So this bot uses selenium and begins by getting the path to chrome driver. Then it opens the page for the 
play-by-play tab of tonights game. Since the gameid is predetermined, you can always access the play-by-play tab, although 
it may be empty. If it is empty, the scraper won't return anything and the program will sleep for 10 seconds and try again.  

The webscraper mechanism is controlled using threading, running 3 simultaneous programs. The most important is loopEvent()

1. **loopEvent()**: constantly checks the latest game detail. It then compares the latest to the criteria stataed in PATH.py.
If it matches, it records the time-stamp and the combined-score, if all 3, the text, time, and score, are new, it will add it 
   to a previously seen list and notify you the criteria have been met. Otherwise, it ignores it. 
2. **manualTerminate()**: it constantly checks for the input. If 'yes' is input, it will terminate, otherwise it loops
3. **ScheduledTerminate()**: if the actual time passes expected game end time, the program will terminate. Feel free to 
   change expected game end time in the CSV or in espn_spider.py

# 4. Closing Thoughts
If you made it this far, thank you so much for reading this. I appreciate anyone who took the time to look. 
I'd like to thank primarily my brother who gave me the idea. I'd also like to thank my stats grade for sacrificing 
itself for this project. Once again, I am a student, so I appreciate any and all constructive feedback, nor will I claim 
I am the only person with this silly idea. I have considrered creating a bot that tweets at Simmons everytime he makes a 3.


