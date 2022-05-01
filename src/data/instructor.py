from functools import reduce

class Instructor:
    def __init__(self, trigram, types, availability):
        self.trigram = trigram
        self.types = types
        self.availability = availability

    def print(self):
        print(f"======={self.trigram}========")
        print(f"Trigram: {self.trigram}")
        print(f"Types: {self.types}")
        print(f"Schedules: {self.availability}")

    @staticmethod
    def from_raw(data, availability):
        trigram = data.get("Trigramme", "")
        types = list(filter(lambda x: x != "", data.get("FIA", []).split("<br/>")))
        return Instructor(trigram, types, availability)