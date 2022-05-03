class Club:
    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = int(points)

    def enough_point(self, numberOfPlaces):
        return int(numberOfPlaces) <= self.points

    def purchase_place(self, numberOfPlaces):
        if self.enough_point(numberOfPlaces):
            self.points -= numberOfPlaces
        else:
            raise ValueError("there is not enough points")
