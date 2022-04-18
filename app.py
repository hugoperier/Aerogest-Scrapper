import requests
from bs4 import BeautifulSoup
from src.scrapper import extract_instructor_resas
import re

def main():
    BASE_URI = "aerogest-reservation.com"
    CLUB_ID = "ac/bellegarde"
    AEROCLUB = "aeroclub_bellegarde"
    URI = "http://" + BASE_URI + "/" + CLUB_ID + ".htm"
    LOGIN = ""
    PASSWORD = ""
    AVAILABLE_COLOR = "#B8F3A8"

    LOGIN_URI = "https://" + BASE_URI + "/Connection/logon"
    BOOKING_URI = "https://" + BASE_URI + "/Booking/PlanningInstructor"
    DAILY_URI = "https://" + BASE_URI + "/Booking/Planning"

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
    for row in rows:
        print(row)
        available_area = row.select_one("div[style*='#B8F3A8']")
        if (available_area):
            print(available_area)
    print("nothing")

    # req_booking = session.get(BOOKING_URI)
    # tooltips = extract_instructor_resas(req_booking.text)
    # for tooltip in tooltips:
    #     print(tooltip)

if __name__ == "__main__":
    main()