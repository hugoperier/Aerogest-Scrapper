from src.scrapper import DailyScrapper
from src.ScheduleFinder import ScheduleFinder
import configparser

def main():
    config = getConfig()
    scheduleFinder = ScheduleFinder(config)
    matches = scheduleFinder.find()

    print("Found {} matches:".format(len(matches)))
    for match in matches:
        print("=================")
        print("Instructor: {}".format(match["instructor"].trigram))
        print("Airplane: {}".format(match["airplane"].registration))
        print("Start: {}".format(match["schedule"]["start"].strftime("%d/%m/%Y %H:%M")))
        print("End: {}".format(match["schedule"]["end"].strftime("%d/%m/%Y %H:%M")))
        print("=================")
        print()

def getConfig():
    config = configparser.ConfigParser()
    config.read('default.conf')
    return config

if __name__ == "__main__":
    main()