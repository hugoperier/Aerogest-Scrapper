from bs4 import BeautifulSoup
import locale

def extract_tooltip(dt):
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

def extract_instructor_resas(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("td", {"class": "referenceContentTD"})
    tooltips = []
    for row in rows:
        resa = row.find("div", {"class": "reservation"})
        if (resa):
            dt = resa["data-tooltip"]
            tooltip = extract_tooltip(dt)
            tooltips.append(tooltip)
    return tooltips

class AerogestScrapper:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.login()
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

    def login(self):
        self.session.post(self.config["login_uri"], data={
            "login": self.config["login"],
            "pass": self.config["password"],
            "aeroclub": self.config["aeroclub"],
            "action2": "Connexion"
        })
        self.session.cookies.set("hasConsent", "true")
        self.session.cookies.set("Aerogest-reservation-str", self.config["aeroclub"])

    def getScheduleByDate(self, date):
        dateFormatted = date.strftime("%A+%d %m %Y&button=mc").replace(" ", "%2F")        
        daily_uri = self.config["daily_uri"] + "?askedDate=" + dateFormatted
        req_daily = self.session.get(daily_uri)
        availableAreas = self.getAvailableAreas(req_daily.text)
        reservedAreas = self.getReservedAreas(req_daily.text)



    def getAvailableAreas(self, content):
        soup = BeautifulSoup(req_daily.text, "html.parser")
        rows = soup.find_all("td", {"class": "referenceContentTD"})
        #print(rows)
        for row in rows:
            #available_area = row.select_one('div[style*="#B8F3A8"]')
            available_area = row.find('div', style=lambda value: value and 'background-color: #B8F3A8' in value)
            if (available_area):
                print(available_area)
            else:
                print("nothing")