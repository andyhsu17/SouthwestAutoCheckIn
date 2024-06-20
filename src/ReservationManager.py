import heapq

from ReservationInfo import ReservationInfo
from enum import Enum


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

