from datetime import date, datetime, timedelta
import pandas as pd
import os.path

from crontab import CronTab
import getpass

import gameCheckBot
import PATH

def main(player, event, schedule):
    completeName = os.path.join(PATH.getPath('NBATextAlerts/'), schedule)


    df = pd.read_csv(completeName)

    df1 = df[df['date'].str.contains(str(date.today()))]


    if df1.empty:
        exit()

    start = datetime.strptime(df1.loc[0].at['date'] + " " + df1.loc[0].at['start time'],
                                                                        "%Y-%m-%d %H:%M:%S")

    cron = CronTab(user=getpass.getuser())
    item = cron.find_comment("NBA schedule {} {} on {}".format(player, event, df1.loc[0].at['date']))



    if len(list(item)) == 0:
        job = cron.new(command='''osascript -e 'tell application "Terminal" to do script "{} {}"' '''.format(PATH.getPath("python"), PATH.getPath("botHelper")),
                       comment="NBA schedule {} {} on {}".format(player, event, df1.loc[0].at['date']))
        job.hour.on(start.hour)
        job.minute.on(start.minute)

        cron.write()


    if start <= datetime.now():
        cron.remove_all(comment="NBA schedule {} {} on {}".format(player, event, df1.loc[0].at['date']))
        cron.write()

        end = datetime.strptime(df1.loc[0].at['date'] + " " + df1.loc[0].at['end time'],
                            "%Y-%m-%d %H:%M:%S")

        if end <= datetime.strptime(df1.loc[0].at['date'] + " 5:00 AM",
                                    "%Y-%m-%d %H:%M %p"):
            end = end + timedelta(days=1)

        E = gameCheckBot.Event(player, event, "https://www.espn.com/nba/playbyplay?gameId=" + df1.loc[0].at['URL'].split('=')[1], end)



if __name__ == "__main__":
    main(PATH.PLAYER, PATH.EVENT, PATH.TEAM + " Schedule.csv")
