import heapq
from enum import Enum
import time
import threading

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

class SouthwestApi():
    def __init__(self):
        pass

    def get_flight_time(self, reservation_number : str) -> int:
        """Gets the flight time for this reservation from southwest website in epoch time
        """
        # Todo
        return 0

    def check_in_flight(self, reservation : ReservationInfo):
        self._post_info_to_southwest(reservation.first_name, reservation.last_name, reservation.reservation_number)
        pass

    def _post_info_to_southwest(self, first_name, last_name, reservation_numbere):
        """ Posts check in to southwest website
        """
        pass

    def _get_info_from_southwest(self):
        pass

class ErrorCode(Enum):
    """Error code enum
    """
    SUCCESS = 0
    RESERVATION_EXISTS = 1
    UNKNOWN_RESERVATION = 2


class ReservationManager:
    """Class to create, monitor, and handle all reservations to be made
    """
    def __init__(self):
        self.reservation_heap = []
        self.reservation_numbers = set()

    def add_reservation(self, reservation : ReservationInfo):
        """Adds a reservation to the system

        Args:
            reservation (ReservationInfo): Reservation to add
        """
        if reservation.reservation_number in self.reservation_numbers:
            return ErrorCode.RESERVATION_EXISTS
        self.reservation_numbers.add(reservation.reservation_number)
        heapq.heappush(self.reservation_heap, reservation)

        return ErrorCode.SUCCESS

    def delete_reservation(self, reservation_number : str):
        """Deletes a reservation from the system

        Args:
            reservation_number (str): Reservation to deletee
        """

        if not reservation_number in self.reservation_numbers:
            return ErrorCode.UNKNOWN_RESERVATION

        # Delete from heap
        for i, reservation in enumerate(self.reservation_heap):
            if (reservation.reservation_number == reservation_number):
                self.reservation_heap[i] = self.reservation_heap[-1]
                self.reservation_heap.pop()
                heapq.heapify(self.reservation_heap)
                # don't forget to remove it from our set
                self.reservation_numbers.remove(reservation_number)
                print(f"Successfully removed reservation: {reservation_number} from system")
                return ErrorCode.SUCCESS

        # Should never get here
        return ErrorCode.UNKNOWN_RESERVATION
        

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

class ReservationSystem:
    
    def __init__(self, debug_level=1):
        # The higher the debug level, the more info we will print
        self.debug = debug_level
        self.reservation_manager = ReservationManager()
        self.southwest_api = SouthwestApi()
        self.check_in_thread = threading.Thread(target=self._check_in_flight)
        self.run_thread = True
        self.check_in_thread.start()
        self.polling_time_seconds = 2 # Period to see if its time to check in yet
        self.ONE_DAY_IN_SECONDS = 24 * 60 * 60

    def __del__(self):
        self.run_thread = False

        # Waits until sleeping thread finishes before continuing
        self.check_in_thread.join()

    def _get_current_time(self) -> int:
        return time.time()

    def _check_in_flight(self):
        while self.run_thread is True:
            time.sleep(1)
            self._log2(f"running thread with reservations: {self.reservation_manager.get_number_of_reservations()}")
            if self.reservation_manager.get_number_of_reservations() == 0:
                self._log2("Thread could not find any reservations in queue, sleeping")
                continue

            if self._get_current_time() < self.reservation_manager.get_first_reservation().get_check_in_time():
                reservation = self.reservation_manager.get_first_reservation()
                self._log2(f"Thread found reservation for {reservation.first_name} {reservation.last_name}, but is not\
                           time to check in yet")
                continue

            reservation = self.reservation_manager.get_first_reservation()
            self.southwest_api.check_in_flight(reservation)
            self.reservation_manager.delete_reservation(reservation.reservation_number)

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
        # Subtract 24 hours in seconds, defaults to 0 in test
        check_in_time = self.southwest_api.get_flight_time(reservation_number) - self.ONE_DAY_IN_SECONDS
        reservation = ReservationInfo(first_name, last_name, reservation_number, check_in_time)
        return self.reservation_manager.add_reservation(reservation)
            
    def delete_reservation(self, reservation_number : str):
        return self.reservation_manager.delete_reservation(reservation_number)

    def get_first_reservation(self):
        return self.reservation_manager.get_first_reservation()

    def get_number_of_reservations(self):
        return self.reservation_manager.get_number_of_reservations()

    def printReservationsByName(self):
        for i in self.reservation_manager.reservation_heap:
            print(i.first_name)

def main():
    system = ReservationSystem()

    # while True:
    #     pass

if __name__ == '__main__':
    main()