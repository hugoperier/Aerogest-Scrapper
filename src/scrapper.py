from bs4 import BeautifulSoup
import locale
import requests
import cssutils
import datetime
from src.data.airplane import Airplane
from src.data.reservation import Reservation
from src.data.instructor import Instructor
from src.utils.exceptions import ParserException

class DailyScrapper:
    def __init__(self, config):
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.config = config
        self.session = requests.Session()
        self.session.cookies.set("hasConsent", "true")
        self.session.cookies.set("Aerogest-reservation-str", self.config["AEROGEST_INFOS"]["CLUB_ID"])
        self.available_color = "#B8F3A8"
        self.total_minutes = 1020
        self.start_hour = 6
        self.date = datetime.datetime.now()        
        self.login()
        self.airplanes = []
        self.instructors = []
        self.reservations = []

    def login(self):
        login = self.config["CREDENTIALS"]["LOGIN"]
        password = self.config["CREDENTIALS"]["PASSWORD"]
        self.session.post(f'{self.config["AEROGEST_INFOS"]["HOST"]}/Connection?login={login}&mdp={password}&conserverconnexion=false&action%3ALogOn=Connexion')        

    def extract(self):
        self.airplanes = []
        self.instructors = []
        self.reservations = []

        data = self.getData()
        timeblockTables = data.find_all("table", {"class": "timeblockTab"})
        if (len(timeblockTables) < 2):
            raise ParserException(data, f"No timeblockTables found -> Expected 2 got {len(timeblockTables)} {self.date.strftime('%d/%m/%Y %H:%M')}")

        airplane_data = self.getAirplaneAvailability(timeblockTables[0])
        instructors_data = self.getInstructorsAvailability(timeblockTables[1])
        
        for ap in airplane_data:
            airplane = Airplane.from_raw(ap["header"], self.date)
            self.airplanes.append(airplane)
            for schedule in ap["schedules"]:
                reservation = Reservation.from_raw(schedule)
                self.reservations.append(reservation)
                airplane.push_reservation(reservation)
        for inst in instructors_data:
            instructor = Instructor.from_raw(inst["header"], inst["availability"], self.date)
            self.instructors.append(instructor)
            for schedule in inst["schedules"]:
                reservation = Reservation.from_raw(schedule)
                if (not filter(lambda x: str(reservation) == str(reservation), self.reservations)):
                    self.reservations.append(reservation)
                instructor.push_reservation(reservation)
    
    def getData(self):
        dateFormatted = self.date.strftime("%A+%d %m %Y&button=mc").replace(" ", "%2F")        
        req_daily = self.session.get(f'{self.config["AEROGEST_INFOS"]["HOST"]}/Booking/PlanningDateChange?askedDate={dateFormatted}')

        data = BeautifulSoup(req_daily.text, "html.parser").find("div", {"class": "contenuPage"})
        if not data:
            raise ParserException(data, "No contenuePage found")     
        return data

    def getAirplaneAvailability(self, data):
        rows = data.find_all("tr")
        airplaneAvailabilities = []
        for row in rows:
            referenceHeader = row.find("td", {"class": "referenceHeader"})
            if not referenceHeader:
                continue
            header = self.getHeader(referenceHeader)
            schedules = self.getReservations(row)
            airplaneAvailabilities.append({
                "header": header,
                "schedules": schedules
            })
        return airplaneAvailabilities

    def getInstructorsAvailability(self, data):
        rows = data.find_all("tr")
        instructorAvailabilities = []
        for row in rows:
            referenceHeader = row.find("td", {"class": "referenceHeader"})
            if not referenceHeader:
                continue
            header = self.getHeader(referenceHeader)
            availability = self.getAvailability(row)
            schedules = self.getReservations(row)
            instructorAvailabilities.append({
                "header": header,
                "availability": availability,
                "schedules": schedules
            })
        return instructorAvailabilities

    def getHeader(self, referenceHeader):
        dt = referenceHeader["data-tooltip"]
        dtLines = dt.split("<br>")
        header = {}
        for line in dtLines:
            [key, value] = line.split(":")
            header[key.strip()] = value.strip()
        return header

    def getReservations(self, row):
        reservations = row.find_all("div", {"class": "reservation"})
        reservationsParsed = []
        for reservation in reservations:
            dt = reservation["data-tooltip"]
            reservationParsed = self.extract_tooltip(dt)
            reservationsParsed.append(reservationParsed)
        return reservationsParsed

    def extract_tooltip(self, dt):
        dt_soup = BeautifulSoup(dt, "html.parser")
        infos = dt_soup.find_all("td")
        resa = {}
        while infos:
            if infos[0].text.endswith(":"):
                key = infos[0].text.strip(":").strip()
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
        greenZones = row.find_all('div', style=lambda value: value and 'background-color: #B8F3A8' in value)
        availability = []
        for greenZone in greenZones:
            style = cssutils.parseStyle(greenZone.get('style'))
            width = float((style['width']).replace("%", ""))
            left = float(style['left'].replace("%", ""))
            schedule = {}
            schedule['start'] = (round(left / 100 * self.total_minutes) / 60) + self.start_hour
            schedule['end'] = (round(width / 100 * self.total_minutes) / 60) + schedule['start']
            availability.append(schedule)
        return self.reduce_availability(availability)


    # reduce the list of availability if start and end are contained in another
    # ex of input availabilities = [{'start': 10.5, 'end': 12.5}, {'start': 14.0, 'end': 16.0}, {'start': 11.0, 'end': 15.0}, {'start': 11.0, 'end': 15.0}, {'start': 16.0, 'end': 17.0}]
    # should become [{'start': 10.5, 'end': 17}]
    def reduce_availability(self, availabilities):
        availabilities = sorted(availabilities, key=lambda x: x['start'])
        reduced_availability = []
        for availability in availabilities:
            if not reduced_availability:
                reduced_availability.append(availability)
            else:
                last_availability = reduced_availability[-1]
                if (availability['start'] >= last_availability['start'] and availability['end'] <= last_availability['end']):
                    pass
                elif (availability['start'] <= last_availability['end'] and availability['end'] >= last_availability['end']):
                    reduced_availability.pop()
                    reduced_availability.append({'start': last_availability['start'], 'end': availability['end']})
                else:
                    reduced_availability.append(availability)
        return reduced_availability