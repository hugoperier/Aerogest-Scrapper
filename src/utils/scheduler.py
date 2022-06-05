from time import sleep
import logging
from src.utils.mailer import Mailer
from src.utils.formatReservation import text_format

class Scheduler:
    def __init__(self, scrapper, configuration):
        self.logger = logging.getLogger("Scheduler")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]:  %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.scrapper = scrapper
        self.interval = int(configuration["SCHEDULER"].get("INTERVAL", 60)) * 60
        self.notifier = []
        if (configuration["MAILER"].getboolean("ENABLED", False) == True):
            self.addNotifier("Mailer", Mailer(configuration["MAILER"]))

    def run(self):
        self.logger.info("Scheduler started")
        prevMatches = []
        while True:
            try:
                matches = self.scrapper.find()
                if (len(matches) > 0 and not text_format(matches) == text_format(prevMatches)):
                    self.logger.info(f"{len(matches)} matches found")
                    for notifier in self.notifier:
                        notifier.notify(matches)
                    prevMatches = matches
                else:
                    self.logger.info("No new matches")
            except Exception as e:
                self.logger.error(str(e))
                for notifier in self.notifier:
                        notifier.notifyError(str(e))
            sleep(self.interval)

    def addNotifier(self, name, notifier):
        self.logger.info(f"{name} notifier enabled")
        self.notifier.append(notifier)
