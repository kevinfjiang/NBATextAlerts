"""
This is my first public project, thank you for taking a look. This is me testing
out webscraping and Crontab.

During each basketball game, a new terminal will open. If you would like to exit the bot,
type 'yes' into it.

Running this program sets a weekly scrape of the NBA schedule of all teams and a daily check if
a specified team is playing tonight. Both occur at 11 am on Sunday, or daily. Feel free to change

Run this script once and you should be all set
"""

from crontab import CronTab
import getpass
from scrapy.crawler import CrawlerProcess

from NBA.NBA.spiders import espn_spider
import PATH



def main():
    #Sets up daily check. Once you add your constants to the PATH file, you
    #just run setup.py and it should automate for you, checking daily at 8 AM
    #if there's a game
    cron = CronTab(user=getpass.getuser())
    job = cron.new(command="{} {}".format(PATH.getPath('PYTHON'), PATH.getPath('botHelper')))
    job.hour.on(11)
    job.minute.on(0)

    #Sets up a weekly schedule update to see if there are more games. This ensures
    #changing schedules are constantly updated
    secondjob = cron.new(command="cd {} && scrapy crawl espn".format(PATH.getPath('scraper')))
    secondjob.hour.on(11)
    secondjob.minute.on(0)
    secondjob.dow.on('SUN')

    cron.write()

    #Sets up initial schedule by scraping while the script runs
    process = CrawlerProcess()
    process.crawl(espn_spider.ESPNSpider)
    process.start()




if __name__ == "__main__":
    main()