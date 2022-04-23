from bs4 import BeautifulSoup
import locale
import requests
import re
import cssutils
import datetime

class DailyScrapper:
    def __init__(self, config):
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.config = config
        self.session = requests.Session()
        self.available_color = "#B8F3A8"
        self.total_minutes = 1020
        self.start_hour = 6
        self.date = datetime.datetime.now()
        self.login()

    def login(self):
        self.session.post(f'{self.config["AEROGEST_INFOS"]["HOST"]}/Connection/logon', data={
            "login": self.config["CREDENTIALS"]["LOGIN"],
            "pass": self.config["CREDENTIALS"]["PASSWORD"],
            "aeroclub": self.config["AEROGEST_INFOS"]["CLUB_ID"],
            "action2": "Connexion"
        })
        self.session.cookies.set("hasConsent", "true")
        self.session.cookies.set("Aerogest-reservation-str", self.config["AEROGEST_INFOS"]["CLUB_ID"])

    def extract(self):
        dateFormatted = self.date.strftime("%A+%d %m %Y&button=mc").replace(" ", "%2F")        
        req_daily = self.session.get(f'{self.config["AEROGEST_INFOS"]["HOST"]}/Booking/PlanningDateChange?askedDate={dateFormatted}')
        airplane_availability = self.getAirplaneAvailability(req_daily.text)
        instructors_availability = self.getInstructorsAvailability(airplane_availability)


    def getAirplaneAvailability(self, html):
        timeblockTable = BeautifulSoup(html, "html.parser").find_all("table", {"class": "timeblockTable"})[1]

        rows = timeblockTable.find_all("tr")
        for row in rows:
            referenceHeader = row.find("td", {"class": "referenceHeader"})
            if not referenceHeader:
                continue
            header = getHeader(referenceHeader)
            availability = getAvailability(row)
            schedules = getSchedules(row)

    def getHeader(self, referenceHeader):
        dt = referenceHeader["data-tooltip"].text
        dtLines = dt.split("<br>")
        header = {}
        for line in dtLines:
            [key, value] = line.split(":")
            header[key] = value.strip()
        return header

    def getReservations(self, row):
        referenceContentTD = row.find_all("td", {"class": "referenceContentTD"})
        reservations = row.find_all("div", {"class": "reservation"})
        for reservation in reservations:
            dt = reservation["data-tooltip"]
            reservationParsed = self.extract_tooltip(dt)

    def extract_tooltip(self, dt):
        dt_soup = BeautifulSoup(dt, "html.parser")
        infos = dt_soup.find_all("td")
        resa = {}
        while infos:
            if infos[0].text.endswith(":"):
                key = infos[0].text.strip(":")
                resa[key] = []
            else:
                if (infos[0].text != ""):
                    resa[key].append(infos[0].text.strip())
            infos = infos[1:]
        for key in resa:
            if (resa[key].__len__() == 1):
                resa[key] = resa[key][0]
        return resa

    def getAvailability(self, row):
        referenceContentTD = row.find_all("td", {"class": "referenceContentTD"})
        greenZones = row.find_all('div', style=lambda value: value and 'background-color: #B8F3A8' in value)
        availability = []
        for greenZone in greenZones:
            style = cssutils.parseStyle(greenZone.get('style'))
            width = float((style['width']).replace("%", ""))
            left = float(style['left'].replace("%", ""))
            schedule = {}
            schedule.start = (round(left / 100 * TOTAL_MINUTES) / 60) + START_HOUR
            schedule.end = (round(width / 100 * TOTAL_MINUTES) / 60) + schedule.start
            availability.append(schedule)
        return availability


    def getAvailableAreas(self, content):
        soup = BeautifulSoup(req_daily.text, "html.parser")
        rows = soup.find_all("td", {"class": "referenceContentTD"})
        #print(rows)
        for row in rows:
            available_area = row.find('div', style=lambda value: value and 'background-color: #B8F3A8' in value)
            if (available_area):
                print(available_area)
            else:
                print("nothing")