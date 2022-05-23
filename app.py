from src.scrapper import DailyScrapper
from src.ScheduleFinder import ScheduleFinder
import configparser
from src.utils.formatReservation import formatReservations

def main():
    fetch()

def fetch():
    config = getConfig()
    scheduleFinder = ScheduleFinder(config)
    matches = scheduleFinder.find()

    print("Found {} matches:".format(len(matches)))
    matchesFormatted = formatReservations(matches)
    print(matchesFormatted)

def getConfig():
    config = configparser.ConfigParser()
    config.read('default.conf')
    return config

if __name__ == "__main__":
    main()