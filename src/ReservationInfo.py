class ReservationInfo:
    """Class that contains info needed per reservation
    """
    def __init__(self, first_name : str, last_name : str, reservation_number : str, check_in_time : int):
        self.first_name = first_name
        self.last_name = last_name
        self.reservation_number = reservation_number
        self.check_in_time = check_in_time

    def __lt__(self, other):
        return self.check_in_time < other.check_in_time
    
    # def _get_flight_time_from_southwest(self, reservation_number):
    #     """Gets the flight time for this reservation from southwest website in epoch time
    #     """
    #     # Todo
    #     return 24 * 60 * 60

    def get_check_in_time(self):
        """Returns the check in time for this reservation
        """
        return self.check_in_time
