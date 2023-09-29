import heapq
from enum import Enum

class ErrorCode(Enum):
    SUCCESS = 0
    RESERVATION_EXISTS = 1

class ReservationInfo:
    def __init__(self, first_name : str, last_name : str, reservation_number : str):
        self.first_name = first_name
        self.last_name = last_name
        self.reservation_number = reservation_number
        self.check_in_time = self._getFlightTimeFromSouthwest() - 24

    def __lt__(self, other):
        return self.check_in_time < other.check_in_time
    
    def _getFlightTimeFromSouthwest(self):
        '''Gets the flight time from southwest website
        '''
        # Todo
        return 24

    def getCheckInTime(self):
        return self.check_in_time

class Scheduler:
    def __init__(self):
        self.reservation_heap = []
        self.reservation_numbers = set()

    def addReservation(self, reservation : ReservationInfo):
        if reservation.reservation_number in self.reservation_numbers:
            print(f"Unable to add reservation number {reservation.reservation_number} since it already exists")
            return ErrorCode.RESERVATION_EXISTS
        self.reservation_numbers.add(reservation.reservation_number)
        heapq.heappush(self.reservation_heap, reservation)
        return ErrorCode.SUCCESS

    def deleteReservation(self, reservation_number : str):
        for i, reservation in enumerate(self.reservation_heap):
            if (reservation.reservation_number == reservation_number):
                self.reservation_heap[i] = self.reservation_heap[-1]
                self.reservation_heap.pop()
                heapq.heapify(self.reservation_heap)

    def getFirstReservation(self):
        if (self.getNumberOfReservations() == 0):
            return None
        return self.reservation_heap[0]

    def getNumberOfReservations(self):
        return len(self.reservation_heap)

                

class ReservationSystem:
    
    def __init__(self):
        self.debug = 1
        self.scheduler = Scheduler()

    def _log0(x):
        print(x)

    def _log1(x):
        if self.debug >= 1:
            print(x)

    def _log2(x):
        if self.debug >= 2:
            print(x)

    def createReservation(self, first_name : str, last_name : str, reservation_number : str):
        reservation = ReservationInfo(first_name, last_name, reservation_number)
        return self.scheduler.addReservation(reservation)
            
    def deleteReservation(self, reservation_number : str):
        self.scheduler.deleteReservation(reservation_number)

    def getFirstReservation(self):
        return self.scheduler.getFirstReservation()

    def getNumberOfReservations(self):
        return self.scheduler.getNumberOfReservations()


    def printReservationsByName(self):
        for i in self.scheduler.reservation_heap:
            print(i.first_name)

def main():
    system = ReservationSystem()

    # while True:
    #     pass

if __name__ == '__main__':
    main()