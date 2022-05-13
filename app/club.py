class Club:
    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = int(points)

    def enough_point(self, numberOfPlaces, coef):
        return int(numberOfPlaces) * coef <= self.points

    def purchase_place(self, numberOfPlaces, coef):
        if self.enough_point(numberOfPlaces, coef):
            self.points -= numberOfPlaces * coef
        else:
            raise ValueError("there is not enough points")
