import concurrent.futures
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import TimeoutException

import Alerts
import PATH

class Event:
    def __init__(self, Player, Event, url, end):
        self.breakloop = False

        self.player = Player
        self.event = Event
        self.end = end

        self.eventList = []

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument('headless')

        self.driver = webdriver.Chrome(PATH.getPath('chromedriver'), options=chrome_options)

        self.driver.get(url)
        self.main()

    def main(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            t1 = executor.submit(self.loopEvent)
            t2 = executor.submit(self.manualterminate)
            t3 = executor.submit(self.scheduledterminate)
        self.driver.quit()




    def manualterminate(self):
        while not self.breakloop:
            try:
                bloop = input("breakloop? \n")

                if bloop == 'yes':
                    self.breakloop = True
                    break
            except ValueError:
                self.manualterminate()

    def scheduledterminate(self):
        while not self.breakloop:
            time.sleep(10)

            if self.end < datetime.now():
                self.breakloop = True

    def checkEvent(self):
        element = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.game-details'))).text
        if (self.player) in element and (self.event) in element:
            time = WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.time-stamp'))).text
            score = WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.combined-score'))).text

            if (time, element, score) not in self.eventList:
                self.eventList.append((time, element, score))
                print(time + ": " + element)
                Alerts.send_message(time + ": " + element)


    def loopEvent(self):
        n = 0
        try:
            while not self.breakloop:
                self.checkEvent()
                time.sleep(.25)
        except TimeoutException:
            print("Game hasn't started yet")
            time.sleep(10)
            n+=1
            if n > 100:
                exit()
            self.loopEvent()

        self.breakloop = True





if __name__ == "__main__":
    E = Event(PATH.PLAYER, PATH.EVENT,
                           "https://www.espn.com/nba/playbyplay?gameId=401307452", datetime.now())

