import heapq

from ReservationInfo import *
from Logger import Logger
from enum import Enum
from db import db


class ErrorCode(Enum):
    """Error code enum
    """
    SUCCESS = 0
    RESERVATION_EXISTS = 1
    UNKNOWN_RESERVATION = 2


class ReservationManager:
    """Class to create, monitor, and handle all reservations to be made
    """
    def __init__(self, debug_level, db_name):
        self.reservation_numbers = set()
        self.logger = Logger(debug_level)
        self.db = db(db_name, debug_level)
        self.reservation_heap = [TupleToReservationInfo(reservation_tuple[1:]) for reservation_tuple in self.db.get_all()]
        for obj in self.reservation_heap:
            self.logger._log2(obj.check_in_time, obj.reservation_number, obj.first_name, obj.last_name)
        heapq.heapify(self.reservation_heap)

    def add_reservation(self, reservation : ReservationInfo):
        """Adds a reservation to the system

        Args:
            reservation (ReservationInfo): Reservation to add
        """
        if reservation.reservation_number in self.reservation_numbers:
            return ErrorCode.RESERVATION_EXISTS
        self.reservation_numbers.add(reservation.reservation_number)
        heapq.heappush(self.reservation_heap, reservation)
        self.db.add_reservation(reservation)

        return ErrorCode.SUCCESS

    def pop_reservation(self):
        # Delete from heap
        res = heapq.heappop(self.reservation_heap)
        # don't forget to remove it from our set
        self.reservation_numbers.remove(res.reservation_number)
        try:
            self.db.delete_reservation_by_name(res.reservation_number)
        except Exception as e:
            self.logger._log0(f"Did not find reservation {res.reservation_number} in database. Continuing.")
        self.logger._log2(f"Successfully removed reservation: {res.reservation_number} from system")
        return ErrorCode.SUCCESS

    def delete_reservation_by_name(self, reservation_number : str):
        """Deletes a reservation from the system by name

        Args:
            reservation_number (str): Reservation to delete
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
                try:
                    self.db.delete_reservation_by_name(reservation_number)
                except Exception as e:
                    self.logger._log0(f"Did not find reservation {reservation_number} in database. Continuing.")
                self.logger._log2(f"Successfully removed reservation: {reservation_number} from system")
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

