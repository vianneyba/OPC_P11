class Booking:

    booking_list = []

    def __init__(self, club_name, competition_name, nb_places):
        self.club_name = club_name
        self.competition_name = competition_name
        self.nb_places = int(nb_places)
        Booking.booking_list.append(self)

    def add_places(self, nb_places):
        self.nb_places += nb_places

    @classmethod
    def already_booked(cls, club_name, competition_name):
        for booked in cls.booking_list:
            if (booked.club_name == club_name) and (booked.competition_name == competition_name):
                return booked
        return None