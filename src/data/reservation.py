import uuid
from functools import reduce

class Reservation:
    def __init__(self, created, title, start, end, destination, flight_time, free_seats, r_type, description, registrations):
        self.id = uuid.uuid4()
        self.created = created
        self.title = title
        self.start = start
        self.end = end
        self.destination = destination
        self.flight_time = flight_time
        self.free_seats = free_seats
        self.r_type = r_type
        self.description = description
        self.registrations = registrations

    def print(self):
        print(f"======={self.title}========")
        print(f"Created: {self.created}")
        print(f"Title: {self.title}")
        print(f"Start: {self.start}")
        print(f"End: {self.end}")
        print(f"Destination: {self.destination}")
        print(f"Flight time: {self.flight_time}")
        print(f"Free seats: {self.free_seats}")
        print(f"Type: {self.r_type}")
        print(f"Description: {self.description}")
        print(f"Registrations: {self.registrations}")
        
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

        