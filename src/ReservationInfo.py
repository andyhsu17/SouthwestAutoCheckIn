def TupleToReservationInfo(tuple_in : tuple):
    if (len(tuple_in) != 4):
        print("ERROR: tuple is incorrect length")
    res = ReservationInfo(tuple_in[0], tuple_in[1], tuple_in[2], tuple_in[3])
    return res

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
    
    def get_check_in_time(self):
        """Returns the check in time for this reservation
        """
        return self.check_in_time

    def get_tuple(self):
        """Returns the tuple data for this reservation
        """
        return (self.first_name, self.last_name, self.reservation_number, self.check_in_time)
