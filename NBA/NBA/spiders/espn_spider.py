import scrapy
from datetime import datetime
import os.path
import pandas as pd

import PATH

path = PATH.getPath('NBATextAlerts/')

class ESPNSpider(scrapy.Spider):
    name = "espn"
    start_urls = [
        'https://www.espn.com/nba/team/schedule/_/name/bos',
        'https://www.espn.com/nba/team/schedule/_/name/bkn',
        'https://www.espn.com/nba/team/schedule/_/name/ny/',
        'https://www.espn.com/nba/team/schedule/_/name/phi/',
        'https://www.espn.com/nba/team/schedule/_/name/tor/',
        'https://www.espn.com/nba/team/schedule/_/name/chi/',
        'https://www.espn.com/nba/team/schedule/_/name/cle/',
        'https://www.espn.com/nba/team/schedule/_/name/det/',
        'https://www.espn.com/nba/team/schedule/_/name/ind/',
        'https://www.espn.com/nba/team/schedule/_/name/mil/',
        'https://www.espn.com/nba/team/schedule/_/name/atl/',
        'https://www.espn.com/nba/team/schedule/_/name/cha/',
        'https://www.espn.com/nba/team/schedule/_/name/mia/',
        'https://www.espn.com/nba/team/schedule/_/name/orl/',
        'https://www.espn.com/nba/team/schedule/_/name/wsh/',
        'https://www.espn.com/nba/team/schedule/_/name/den/',
        'https://www.espn.com/nba/team/schedule/_/name/min/',
        'https://www.espn.com/nba/team/schedule/_/name/okc/',
        'https://www.espn.com/nba/team/schedule/_/name/por/',
        'https://www.espn.com/nba/team/schedule/_/name/utah/',
        'https://www.espn.com/nba/team/schedule/_/name/gs/',
        'https://www.espn.com/nba/team/schedule/_/name/lac/',
        'https://www.espn.com/nba/team/schedule/_/name/lal/',
        'https://www.espn.com/nba/team/schedule/_/name/phx/',
        'https://www.espn.com/nba/team/schedule/_/name/sac/',
        'https://www.espn.com/nba/team/schedule/_/name/dal/',
        'https://www.espn.com/nba/team/schedule/_/name/hou/',
        'https://www.espn.com/nba/team/schedule/_/name/mem/',
        'https://www.espn.com/nba/team/schedule/_/name/no/',
        'https://www.espn.com/nba/team/schedule/_/name/sas/'


    ]


    def getConvertDateFormat(self, sel, date):
        parsedArray = date[0].split(' ')

        monthnum= {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
        }
        month = monthnum[parsedArray[1]]

        day = parsedArray[2]

        if month in ['10', '11', '12'] and datetime.now().month < 6:
            year = datetime.now().year - 1
        elif month in ['10', '11', '12'] and datetime.now().month > 6:
            year = datetime.now().year
        elif datetime.now().month > 6:
            year = datetime.now().year + 1
        else:
            year = datetime.now().year

        url = sel.xpath("./td//a[contains(text(), ':')]/@href").extract_first()
        end = date[1].replace(' ', ':')
        end = end.split(':')
        endtime = getEndtime(end)
        days = str(year) + month + day



        return url, datetime.strptime(days, "%Y%m%d").date(), \
               datetime.strptime(date[1], "%I:%M %p").time(), \
               datetime.strptime(endtime, "%I:%M%p").time()

    def parse(self, response):

        dateTimes = {
            'URL': [],
            'date': [],
            'start time': [],
            'end time': []
        }

        teamName = response.xpath("//title/text()").extract_first()
        parts = teamName.split(' ')
        teamName = " ".join(parts[1:(len(parts)-2)])


        for sel in list(response.xpath("//tr[@class='Table__TR Table__TR--sm Table__even']")):
            try:
                title = sel.xpath("./td/span//text()").extract()

                if title[0] != 'DATE' and (title[1] != 'W' or title[1] != 'L') and title[0] != 'TBD':
                    url, date, start, end = self.getConvertDateFormat(sel, title)
                    dateTimes['date'].append(date)
                    dateTimes['URL'].append(url)
                    dateTimes['start time'].append(start)
                    dateTimes['end time'].append(end)
            except IndexError:
                pass

        df = pd.DataFrame(dateTimes, columns=['URL', 'date', 'start time', 'end time'])


        createExcel(df, teamName)


def getEndtime(end):
    end[1] = int(end[1]) + 45
    if end[1] > 60:
        end[1]-=60
        end[0] = int(end[0]) + 1
    end[0] = int(end[0]) + 2
    if end[0] >= 12:
        if end[0] > 12:
            end[0] = end[0] - 12
        end[2] = 'AM'
    return str(end[0]) + ":" + str(end[1]) + end[2]

def createExcel(df, name):
    newpath = os.path.join(path, 'Nba Schedules/')

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    save_path = os.path.expanduser(newpath)
    completeName = os.path.join(save_path, name + ".csv")

    df.to_csv(completeName, index=True, header=True)

