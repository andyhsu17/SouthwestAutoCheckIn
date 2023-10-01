import heapq
from threading import Timer
from enum import Enum

class ErrorCode(Enum):
    """ @brief Error code enum
    """
    SUCCESS = 0
    RESERVATION_EXISTS = 1
    UNKNOWN_RESERVATION = 2

class ReservationInfo:
    """ @brief Class that contains info needed per reservation
    """
    def __init__(self, first_name : str, last_name : str, reservation_number : str):
        self.first_name = first_name
        self.last_name = last_name
        self.reservation_number = reservation_number
        self.check_in_time = self._get_flight_time_from_southwest() - 24

    def __lt__(self, other):
        return self.check_in_time < other.check_in_time
    
    def _get_flight_time_from_southwest(self):
        """@brief Gets the flight time from southwest website
        """
        # Todo
        return 24

    def get_check_in_time(self):
        """ @brief Returns the check in time for this reservation
        """
        return self.check_in_time

class Scheduler:
    """Class to create, monitor, and handle all reservations to be made"""
    def __init__(self):
        self.reservation_heap = []
        self.reservation_numbers = set()
        self.t = Timer(10, self.check_for_events)

    def add_reservation(self, reservation : ReservationInfo):
        """ Adds a reservation to the system

        Args:
            reservation (ReservationInfo): Reservation to add
        """
        if reservation.reservation_number in self.reservation_numbers:
            print(f"Unable to add reservation number {reservation.reservation_number} since it already exists")
            return ErrorCode.RESERVATION_EXISTS
        self.reservation_numbers.add(reservation.reservation_number)
        heapq.heappush(self.reservation_heap, reservation)
        return ErrorCode.SUCCESS

    def delete_reservation(self, reservation_number : str):
        """ deletes a reservation from the system

        Args:
            reservation_number (str): Reservation to deletee
        """

        if not reservation_number in self.reservation_numbers:
            return ErrorCode.UNKNOWN_RESERVATION
        for i, reservation in enumerate(self.reservation_heap):
            if (reservation.reservation_number == reservation_number):
                self.reservation_heap[i] = self.reservation_heap[-1]
                self.reservation_heap.pop()
                heapq.heapify(self.reservation_heap)
        return ErrorCode.SUCCESS

    def get_first_reservation(self):
        """Gets the first reservation to be checked in for

        Returns:
            ReservationInfo: First reservation to be checked in for by time
        """
        if (self.get_number_of_reservations() == 0):
            return None
        return self.reservation_heap[0]

    def get_number_of_reservations(self):
        return len(self.reservation_heap)

    def check_for_events(self):
        print("Checking for events")


                

class ReservationSystem:
    
    def __init__(self):
        # The higher the debug level, the more info we will print
        self.debug = 1
        self.scheduler = Scheduler()

    def _log0(self, x):
        print(x)

    def _log1(self, x):
        if self.debug >= 1:
            print(x)

    def _log2(self, x):
        if self.debug >= 2:
            print(x)

    def add_reservation(self, first_name : str, last_name : str, reservation_number : str):
        """ Adds a reservation to the system

        Args:
            first_name (str): First name
            last_name (str): Last name
            reservation_number (str): Southwest confirmation code
        """
        reservation = ReservationInfo(first_name, last_name, reservation_number)
        return self.scheduler.add_reservation(reservation)
            
    def delete_reservation(self, reservation_number : str):
        return self.scheduler.delete_reservation(reservation_number)

    def get_first_reservation(self):
        return self.scheduler.get_first_reservation()

    def get_number_of_reservations(self):
        return self.scheduler.get_number_of_reservations()


    def printReservationsByName(self):
        for i in self.scheduler.reservation_heap:
            print(i.first_name)

def main():
    system = ReservationSystem()

    # while True:
    #     pass

if __name__ == '__main__':
    main()