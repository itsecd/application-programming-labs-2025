class Person:
    def __init__(self, surname="-", name="-", gender="-", birth="-", contact="-", city="-"):
        self.surname = surname
        self.name = name
        self.gender = gender
        self.birth = birth
        self.contact = contact
        self.city = city

    def __str__(self):
        return f"{self.surname};{self.name};{self.gender};{self.birth};{self.contact};{self.city}"

