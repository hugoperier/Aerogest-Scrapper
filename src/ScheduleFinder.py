from datetime import datetime, timedelta
from src.scrapper import DailyScrapper
import locale

class ScheduleFinder:
    def __init__(self, configuration):
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.days = configuration["SCHEDULESFINDER"].get("WEEKDAYS", "*").split(",")
        self.duration = int(configuration["SCHEDULESFINDER"].get("DURATION", 2))
        self.instructors = configuration["SCHEDULESFINDER"].get("INSTRUCTORS", "*").split(",")
        self.airplane = configuration["SCHEDULESFINDER"].get("AIRPLANE", "*").split(",")
        self.searchRange = int(configuration["SCHEDULESFINDER"].get("SEARCHRANGE", 30))
        self.scrapper = DailyScrapper(configuration)
        
    def find(self):
        matches = []
        for i in range(self.searchRange):
            if not (self.scrapper.date.strftime("%A").lower() in self.days or "*" in self.days):
                continue

            self.scrapper.extract()
            instructors_availabilities = self.findInstructors()
            airplanes_availabilities = self.findAirplanes()

            for instructor_availability in instructors_availabilities:
                for airplane_availability in airplanes_availabilities:
                    start = max(instructor_availability["schedule"]["start"], airplane_availability["schedule"]["start"])
                    end = min(instructor_availability["schedule"]["end"], airplane_availability["schedule"]["end"])
                    if (end <= start):
                        continue
                    if (end - start >= timedelta(minutes=self.duration)):
                        matches.append({
                            "instructor": instructor_availability["instructor"],
                            "airplane": airplane_availability["airplane"],
                            "schedule": {
                                "start": start,
                                "end": end
                            }
                        })
            self.scrapper.date += timedelta(days=1)
        return matches
            
    def findInstructors(self):
        matches = []
        for instructor in self.scrapper.instructors:
                if not (instructor.trigram in self.instructors or "*" in self.instructors):
                    continue
                for schedule in instructor.free_slots:                    
                    if schedule["end"] - schedule["start"] >= timedelta(minutes=self.duration):
                        matches.append({
                         "instructor": instructor,
                         "schedule": schedule   
                        })
        return matches

    def findAirplanes(self):
        matches = []
        for airplane in self.scrapper.airplanes:
                if not (airplane.registration in self.airplane or "*" in self.airplane):
                    continue
                for schedule in airplane.free_slots:
                    if schedule["end"] - schedule["start"] >= timedelta(minutes=self.duration):
                        matches.append({
                            "airplane": airplane,
                            "schedule": schedule
                        })
        return matches