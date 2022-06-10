from time import sleep
from src.utils.mailer import Mailer
from src.utils.formatReservation import text_format
from src.utils.logging import getLogger

class Scheduler:
    def __init__(self, scrapper, configuration):
        self.logger = getLogger("Scheduler")
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
