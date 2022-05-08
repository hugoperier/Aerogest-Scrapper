import uuid
from functools import reduce
from datetime import datetime

class Reservation:
    def __init__(self, created, title, start, end, destination, flight_time, free_seats, r_type, description, registrations):
        self.dateformat = "%d/%m/%Y %H:%M"
        self.id = uuid.uuid4()
        self.created = datetime.strptime(created, self.dateformat)
        self.title = title
        self.start = datetime.strptime(start, self.dateformat)
        self.end = datetime.strptime(end, self.dateformat)
        self.destination = destination
        self.flight_time = flight_time
        self.free_seats = free_seats
        self.r_type = r_type
        self.description = description
        self.registrations = registrations
        self.trigram = ""
        trigram = [I for I in self.title[-3:] if I.isupper()]
        if len(trigram) == 3:
            self.trigram = trigram[0] + trigram[1] + trigram[2]
        
        
    def print(self):
        print(f">>>>>>>{self.title}<<<<<<<<")
        print(f"Created: {datetime.strftime(self.created, self.dateformat)}")
        print(f"Title: {self.title}")
        print(f"Start: {datetime.strftime(self.start, self.dateformat)}")
        print(f"End: {datetime.strftime(self.end, self.dateformat)}")
        print(f"Destination: {self.destination}")
        print(f"Flight time: {self.flight_time}")
        print(f"Free seats: {self.free_seats}")
        print(f"Type: {self.r_type}")
        print(f"Description: {self.description}")
        print(f"Registrations: {self.registrations}")
        print(f"Trigram: {self.trigram}")
        
    @staticmethod
    def from_raw(data):
        created = data.get("Date création", "")
        title = data.get("Titre", "")
        start = data.get("Début", "")
        end = data.get("Fin", "")
        destination = data.get("Destinations", "")
        flight_time = data.get("Temps moteur", "")
        free_seats = data.get("Places libres", "")
        r_type = data.get("Type", "")
        description = data.get("Description", "")
        registrations = list(filter(lambda x: x != "", data.get("Inscriptions", [])))
        return Reservation(created, title, start, end, destination, flight_time, free_seats, r_type, description, registrations)

        