from src.ScheduleFinder import ScheduleFinder
from src.utils.scheduler import Scheduler
from src.utils.formatReservation import text_format
import configparser

def main():
    config = getConfig()
    scheduleFinder = ScheduleFinder(config)
    schedulerEnabled = bool(config["SCHEDULER"].get("ENABLED", False))
    if (schedulerEnabled):
        scheduler = Scheduler(scheduleFinder, config)
        scheduler.run()
    else:
        matches = scheduleFinder.find()
        matchesFormatted = text_format(matches)
        print(matchesFormatted)

def getConfig():
    config = configparser.ConfigParser()
    config.read('default.conf')
    return config

if __name__ == "__main__":
    main()