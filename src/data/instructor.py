from functools import reduce
from src.data.reservation import Reservation
from src.utils.time import date_from_flat_hour

class Instructor:
    def __init__(self, trigram, types, availabilities):
        self.trigram = trigram
        self.types = types
        self.availabilities = availabilities
        self.reservations = []
        self.free_slots = []

    def push_reservation(self, reservation):
        self.reservations.append(reservation)
        self.free_slots = []
        self.reservations = sorted(self.reservations, key=lambda x: x.start.hour)

        for availability in self.availabilities:
            now = availability["start"]
            for resa in self.reservations:
                if resa.start.hour < availability["start"].hour:
                    continue
                if resa.end.hour > availability["end"].hour:
                    break
                
                # check if there is a difference of time between now and the start of the reservation
                if resa.start.hour > now.hour:
                    self.free_slots.append({"start": now, "end": resa.start})
                now = resa.end
            if now.hour < availability["end"].hour:
                self.free_slots.append({"start": now, "end": availability["end"]})

    def print(self):
        print(f"======={self.trigram}========")
        print(f"Trigram: {self.trigram}")
        print(f"Types: {self.types}")
        print(f"Schedules: ", end="")
        for schedule in self.availabilities:
            print(f"{schedule['start'].strftime('%H:%M')} -> {schedule['end'].strftime('%H:%M')}", end=" ; ")
        print()
        print(f"Free slots: ", end="")
        for slot in self.free_slots:
            print(f"{slot['start'].strftime('%H:%M')} -> {slot['end'].strftime('%H:%M')}", end=" ; ")
        print()
        if len(self.reservations) > 0:
            print(f"Reservations:")
        for resa in self.reservations:
            resa.print()
        print()

    @staticmethod
    def from_raw(data, availabilities, date):
        trigram = data.get("Trigramme", "")
        types = list(filter(lambda x: x != "", data.get("FIA", []).split("<br/>")))
        availabilities = list(map(lambda x: {"start": date_from_flat_hour(date, x.get("start", 0)), "end": date_from_flat_hour(date, x.get("end", 0))}, availabilities))
        return Instructor(trigram, types, availabilities)