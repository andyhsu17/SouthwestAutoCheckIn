import sys
sys.path.append('src')
from ReservationSystem import *
import unittest
from unittest.mock import MagicMock, Mock


class ReservationSystemProxy(ReservationSystem):
    """ Reservation System inherited class
    """
    def create_reservation_force_check_in_time(self, first_name, last_name, reservation_number, check_in_time):
        SouthwestApi.get_flight_time=MagicMock(return_value=check_in_time + (24 * 60 * 60))
        self.add_reservation(first_name, last_name, reservation_number)

class ReservationSystemTest(unittest.TestCase):
    def setUp(self):
        # Scheduler._create_sleep_thread_epoch=MagicMock(return_value=None)
        self.system = ReservationSystemProxy()

    def tearDown(self):
        self.system.__del__()

    def test_get_first_reservation(self):
        self.assertEqual(self.system.get_first_reservation(), None)
        self.system.add_reservation("Andy", "Hsu", "KNJ653")
        self.assertEqual(self.system.get_first_reservation().first_name, "Andy")

    def test_create_reservation_scheduler(self):
        self.assertNotEqual(self.system.scheduler, None)

    def test_create_reservation_duplicate(self):
        self.system.add_reservation("Andy", "Hsu", "KNJ653")
        self.assertEqual(self.system.add_reservation("Andy", "Hsu", "KNJ653"),\
                         ErrorCode.RESERVATION_EXISTS)

    def test_create_reservation(self):
        self.system.add_reservation("Andy", "Hsu", "KNJ653")
        self.assertEqual(self.system.get_first_reservation().first_name, "Andy")
        self.assertEqual(self.system.get_number_of_reservations(), 1)
        self.system.add_reservation("Esther", "Hsu", "KNJ654")
        self.assertEqual(self.system.get_number_of_reservations(), 2)
        self.system.add_reservation("Candy", "Hsu", "KNl655")
        self.assertEqual(self.system.get_number_of_reservations(), 3)
        self.system.add_reservation("Tim", "Hsu", "KNJ656")
        self.assertEqual(self.system.get_number_of_reservations(), 4)

    def test_delete_reservations(self):
        self.system.add_reservation("Andy", "Hsu", "KNJ653")
        self.assertEqual(self.system.get_first_reservation().first_name, "Andy")
        self.assertEqual(self.system.get_number_of_reservations(), 1)
        self.system.delete_reservation("KNJ653")
        self.assertEqual(self.system.get_first_reservation(), None)
        self.assertEqual(self.system.get_number_of_reservations(), 0)

        self.system.add_reservation("Esther", "Hsu", "L8M194")
        self.system.add_reservation("Candy", "Hsu", "PEE1NA")
        self.assertEqual(self.system.get_number_of_reservations(), 2)

        self.system.delete_reservation("PEE1NA")
        self.assertEqual(self.system.get_number_of_reservations(), 1)

        self.system.add_reservation("Tim", "Hsu", "UHR249")
        self.system.add_reservation("Tim", "Hsu", "YTE923")
        self.system.add_reservation("Tim", "Hsu", "NWI093")
        self.assertEqual(self.system.get_number_of_reservations(), 4)

        self.system.delete_reservation("UHR249")
        self.system.delete_reservation("YTE923")
        self.system.delete_reservation("NWI093")
        self.system.delete_reservation("L8M194")
        self.assertEqual(self.system.get_number_of_reservations(), 0)

    def test_delete_unknown_reservation(self):
        self.assertEqual(self.system.get_number_of_reservations(), 0)
        self.assertEqual(self.system.delete_reservation("UHR249"), ErrorCode.UNKNOWN_RESERVATION)
        self.assertEqual(self.system.get_number_of_reservations(), 0)
        self.system.add_reservation("Tim", "Hsu", "UHR249")
        self.assertEqual(self.system.get_number_of_reservations(), 1)
        self.assertEqual(self.system.delete_reservation("LHR248"), ErrorCode.UNKNOWN_RESERVATION)
        self.assertEqual(self.system.delete_reservation("UHR249"), ErrorCode.SUCCESS)
        self.assertEqual(self.system.get_number_of_reservations(), 0)

    def test_reservation_heap(self):
        self.system.create_reservation_force_check_in_time("Danny", "Tran", "LNJ653", 1)
        self.assertEqual(self.system.get_first_reservation().first_name, "Danny")
        self.assertEqual(self.system.get_first_reservation().check_in_time, 1)

        self.system.create_reservation_force_check_in_time("Andy", "Hsu", "KNJ653", 2)
        self.assertEqual(self.system.get_first_reservation().first_name, "Danny")
        self.assertEqual(self.system.get_first_reservation().check_in_time, 1)

        self.system.create_reservation_force_check_in_time("Tim", "Kang", "MNJ653", 3)
        self.assertEqual(self.system.get_first_reservation().first_name, "Danny")
        self.assertEqual(self.system.get_first_reservation().check_in_time, 1)

        self.system.create_reservation_force_check_in_time("Ken", "Ogden", "NNJ653", 0)
        self.assertEqual(self.system.get_first_reservation().first_name, "Ken")
        self.assertEqual(self.system.get_first_reservation().check_in_time, 0)



if __name__ == '__main__':
    unittest.main()
