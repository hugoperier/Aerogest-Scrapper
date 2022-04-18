import requests
from bs4 import BeautifulSoup
from src.scrapper import extract_instructor_resas
import re
import cssutils

def main():
    BASE_URI = "aerogest-reservation.com"
    CLUB_ID = "ac/bellegarde"
    AEROCLUB = "aeroclub_bellegarde"
    URI = "http://" + BASE_URI + "/" + CLUB_ID + ".htm"
    LOGIN = ""
    PASSWORD = ""
    AVAILABLE_COLOR = "#B8F3A8"
    TOTAL_MINUTES = 1020
    START_HOUR = 6

    LOGIN_URI = "https://" + BASE_URI + "/Connection/logon"
    BOOKING_URI = "https://" + BASE_URI + "/Booking/PlanningInstructor"
    DAILY_URI = "https://" + BASE_URI + "/Booking/PlanningDateChange?askedDate=mardi+19%2F04%2F2022&button=mc"

    session = requests.Session()
    session.post(LOGIN_URI, data={
        "login": LOGIN,
        "pass": PASSWORD,
        "aeroclub": AEROCLUB,
        "action2": "Connexion"
    })
    session.cookies.set("hasConsent", "true")
    session.cookies.set("Aerogest-reservation-str", AEROCLUB)

    req_daily = session.get(DAILY_URI)
    soup = BeautifulSoup(req_daily.text, "html.parser")
    rows = soup.find_all("td", {"class": "referenceContentTD"})
    #print(rows)
    for row in rows:
        #available_area = row.select_one('div[style*="#B8F3A8"]')
        available_area = row.find('div', style=lambda value: value and 'background-color: #B8F3A8' in value)
        if (available_area):
            print(available_area)
            style = cssutils.parseStyle(available_area.get('style'))
            width = float((style['width']).replace("%", ""))
            left = float(style['left'].replace("%", ""))

            start = (round(left / 100 * TOTAL_MINUTES) / 60) + START_HOUR
            end = (round(width / 100 * TOTAL_MINUTES) / 60) + start
            print(start, end)

        else:
            print("nothing")

    # req_booking = session.get(BOOKING_URI)
    # tooltips = extract_instructor_resas(req_booking.text)
    # for tooltip in tooltips:
    #     print(tooltip)

if __name__ == "__main__":
    main()