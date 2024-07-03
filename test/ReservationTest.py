import argparse
import sys
import time
import unittest
from unittest.mock import MagicMock

sys.path.append('src')
from CheckInSystem import *
from SouthwestApi import *
from db import *


verbosity = 0

class DbProxy(db):
    def __init__(self, db_name):
        self.db_name = db_name
        super(DbProxy, self).__init__(self.db_name)

class DbTest(unittest.TestCase):
    def setUp(self):
        global verbosity
        self.db = DbProxy('test_db')
        self.db.create_table()

    def tearDown(self):
        self.db.delete_all()

    def test_print_all(self):
        self.db.print_all()

    def test_add_to_db(self):
        res = ReservationInfo('Andy', 'Hsu', 'HSUMAN', 0)
        self.assertEqual(self.db.insert_data([res.get_tuple()]), True)
        data = self.db.get_all()
        self.assertEqual(len(data), 1)
        # row 0, column 3 is reservation number
        self.assertEqual(data[0][3], 'HSUMAN')

class SouthwestApiProxy(SouthwestApi):
    def __init__(self, verbosity):
        super(SouthwestApiProxy, self).__init__(verbosity)

class SouthwestApiTest(unittest.TestCase):
    def setUp(self):
        global verbosity
        self.api = SouthwestApiProxy(verbosity)

    def test_check_in_unknown_reservation(self):
        res = ReservationInfo('Andy', 'Hsu', 'HSUMAN', 0)
        self.assertEqual(self.api.check_in_flight(res), HttpCode.RESERVATION_NOT_FOUND.value)


class CheckInSystemProxy(CheckInSystem):
    """ Reservation System inherited class
    """
    def __init__(self, verbosity):
        super(CheckInSystemProxy, self).__init__(verbosity)
        self.current_time = 0

    def create_reservation_force_check_in_time(self, first_name, last_name, reservation_number, seconds_until_checkin):
        # Since the reservation system will always take the real flight time and subtract 24 hours from it, this is a hack
        # to add 24 hours to the time returned from get_flight_time(), which will ensure that we check in N seconds from this call
        self.southwest_api.get_flight_time=MagicMock(return_value=seconds_until_checkin + self.ONE_DAY_IN_SECONDS)

        # Fake southwest api to make sure it is always successful
        self.southwest_api.check_in_flight=MagicMock(return_value=HttpCode.SUCCESS)
        self.add_reservation(first_name, last_name, reservation_number)

    def _get_current_time(self) -> int:
        self.current_time = self.current_time + 1
        return self.current_time

class CheckInSystemTest(unittest.TestCase):
    def setUp(self):
        global verbosity
        self.system = CheckInSystemProxy(verbosity)

    def tearDown(self):
        self.system.__del__()

    def test_get_first_reservation(self):
        self.assertEqual(self.system.get_first_reservation(), None)
        self.system.add_reservation("Andy", "Hsu", "KNJ653")
        self.assertEqual(self.system.get_first_reservation().first_name, "Andy")

    def test_create_reservation_manager(self):
        self.assertNotEqual(self.system.reservation_manager, None)

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

    def test_check_time_expires(self):
        self.assertEqual(self.system.get_number_of_reservations(), 0)
        self.system.create_reservation_force_check_in_time("Danny", "Tran", "LNJ653", 2)
        self.assertEqual(self.system.get_first_reservation().first_name, "Danny")
        self.assertEqual(self.system.get_number_of_reservations(), 1)
        time.sleep(3)
        self.assertEqual(self.system.get_number_of_reservations(), 0)

if __name__ == '__main__':
    valid_verbosity_levels = range(0, 3)
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbosity', default=0)
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    verbosity = int(args.verbosity)

    sys.argv[1:] = args.unittest_args
    unittest.main()
