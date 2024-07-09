# Global Imports
import time
import threading

# Local Imports
from ReservationInfo import *
from ReservationManager import *
from SouthwestApi import *
from Logger import Logger

class CheckInSystem:
    def __init__(self, debug_level=0, db_name='reservations', should_run_thread=True):
        """ Constructor

        debug_level (int): O-2. The higher the debug level, the more verbose.
        """
        self.THREAD_POLLING_RATE_SECONDS = 1 # seconds
        self.reservation_manager = ReservationManager(debug_level, db_name)
        self.southwest_api = SouthwestApi(debug_level)
        self.check_in_thread = threading.Thread(target=self._check_in_flight)
        self.run_thread = should_run_thread
        self.check_in_thread.start()
        self.polling_time_seconds = 2 # Period to see if its time to check in yet
        self.ONE_DAY_IN_SECONDS = 24 * 60 * 60
        self.MAX_RETRIES = 10
        self.logger = Logger(debug_level)

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
        retry_count = 0
        while self.run_thread is True:
            time.sleep(self.THREAD_POLLING_RATE_SECONDS)
            self.logger._log2(f"running thread with {self.reservation_manager.get_number_of_reservations()} in queue")
            if self.reservation_manager.get_number_of_reservations() == 0:
                self.logger._log2("Thread could not find any reservations in queue, sleeping")
                continue

            if self._get_current_time() < self.reservation_manager.get_first_reservation().get_check_in_time():
                reservation = self.reservation_manager.get_first_reservation()
                self.logger._log2(f"Thread found reservation for {reservation.first_name} {reservation.last_name}, but is not\
                                  time to check in yet")
                continue

            reservation = self.reservation_manager.get_first_reservation()
            if self.southwest_api.check_in_flight(reservation) == HttpCode.SUCCESS:
                retry_count = 0
                ec = self.reservation_manager.pop_reservation()
                if ec != ErrorCode.SUCCESS:
                    self.logger._log2(f"Unable to remove reservation {reservation.reservation_number} with error code {ec}")
            else:
                self.logger._log2(f"Unable to check in for flight {reservation.reservation_number}. Retry count: {retry_count}")
                retry_count += 1
                if (retry_count >= self.MAX_RETRIES):
                    self.logger._log0(f"Trying to check in for flight {reservation.reservation_number} reached the\
                                      max retry count. Removing the reservation")
                    self.reservation_manager.pop_reservation()
                    retry_count = 0

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
            
    def delete_reservation_by_name(self, reservation_number : str):
        return self.reservation_manager.delete_reservation_by_name(reservation_number)

    def get_first_reservation(self):
        return self.reservation_manager.get_first_reservation()

    def get_number_of_reservations(self):
        return self.reservation_manager.get_number_of_reservations()

    def printReservationsByName(self):
        for res in self.reservation_manager.reservation_heap:
            print(f"{res.first_name} {res.last_name}")
