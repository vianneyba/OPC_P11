class Competition:

    def __init__(self, name, date, numberOfPlaces):
        self.name = name
        self.date = date
        self.numberOfPlaces = int(numberOfPlaces)

    def enough_place(self, placesRequired):
        return int(placesRequired) <= self.numberOfPlaces

    def set_number_of_places(self, placesRequired):
        if self.enough_place(placesRequired):
            self.numberOfPlaces -= placesRequired
        else:
            raise ValueError("there is not enough place available")
