from ReservationInfo import *
from ReservationManager import *
import time
import threading

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

class ReservationSystem:
    
    def __init__(self, debug_level=1):
        # The higher the debug level, the more info we will print
        self.THREAD_POLLING_RATE = 1 # seconds
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

    def _get_current_time(self):
        """ Returns the current expoch time

        This should be overridden in unit test so that time can start at 0.
        """
        return time.time()

    def _check_in_flight(self):
        while self.run_thread is True:
            time.sleep(self.THREAD_POLLING_RATE)
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