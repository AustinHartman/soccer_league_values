from bs4 import BeautifulSoup, Comment
import requests
import csv


"""
Class takes a transkermarkt.co.uk URL of a certain
soccer league and is setup to scrape data on number 
of players and values of every club in the league 
from 2006-2018
"""

# MUST set link at bottom to use


# Player class grabs basic statistical attributes on a player typically to be then loaded into a csv of many players
class Season:
    def __init__(self, url, file):
        self.url = url;
        self.file = file;

    def getTeam(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        page = requests.get(self.url, headers=headers)
        # [year, team, players, value]
        attributes = []
        soup = BeautifulSoup(page.content, "lxml")
        table = open(self.file, 'a')
        a = csv.writer(table)

        # locate table in soup which extracting data from
        teams_table = soup.find("table", "items")

        # divide up the table by teams in the table
        teams_name = teams_table.find_all("tr")

        # get the year from the URL
        year = self.url[-4:]

        for team in teams_name[2:]:

            data = team.findAll('a')
            try:
                attributes.append(year)
                attributes.append(data[1].text)
                attributes.append(data[-3].text)
                attributes.append(data[-1].text)
                a.writerow(attributes)
                attributes = []
            except:
                print("Row of table with following information was unable to be added", team.text)
        table.close()



def addHeaders(file):
    table = open(file, 'a')
    a = csv.writer(table)

    # headers added to top of the file... only to be added once (often right after a clear)
    a.writerow(['year', 'club', 'players', 'total value'])
    table.close()


# be careful when using this function as it will delete everything from the CSV
def clear(file):
    table = open(file, 'w')
    table.close()


clear('mls_club_values.csv')
addHeaders('mls_club_values.csv')

# link to league homepage
link = ""

for year_id in range(2005, 2018):
    url = link  + str(year_id)
    obj = Season(url, "mls_club_values.csv")
    obj.getTeam()