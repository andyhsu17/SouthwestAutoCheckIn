import argparse
import sys
import time
import unittest
from unittest.mock import MagicMock
import heapq

sys.path.append('src')
from CheckInSystem import *
from SouthwestApi import *
from db import *


verbosity = 0

class DbProxy(db):
    def __init__(self, db_name, debug_level):
        self.db_name = db_name
        super(DbProxy, self).__init__(self.db_name, debug_level)

class DbTest(unittest.TestCase):
    def setUp(self):
        global verbosity
        self.db = DbProxy('test_db', verbosity)
        self.db.create_table()
        self.db.delete_all()

    def tearDown(self):
        self.db.delete_all()

    def test_print_all(self):
        self.db.print_all()

    def test_add_to_db(self):
        res = ReservationInfo('Andy', 'Hsu', 'HSUMAN', 0)
        self.assertEqual(self.db.insert_data([res.get_tuple()]), True)
        data = self.db.get_all()
        self.assertEqual(len(data), 1)
        # row 0, column 3 is reservation number of first entry
        self.assertEqual(data[0][3], 'HSUMAN')

    def test_add_multiple_to_db(self):
        res = ReservationInfo('Andy', 'Hsu', 'HSUMAN', 0)
        self.assertEqual(self.db.insert_data([res.get_tuple()]), True)
        res.first_name = 'Danny'
        res.reservation_number = 'NEWRES'
        self.assertEqual(self.db.insert_data([res.get_tuple()]), True)
        data = self.db.get_all()
        self.assertEqual(len(data), 2)
        # row 0, column 3 is reservation number
        self.assertEqual(data[0][3], 'HSUMAN')
        self.assertEqual(data[1][3], 'NEWRES')

    def test_no_data(self):
        data = self.db.get_all()
        self.assertEqual(len(data), 0)

    def test_delete(self):
        res = ReservationInfo('Andy', 'Hsu', 'HSUMAN', 0)
        self.assertEqual(self.db.insert_data([res.get_tuple()]), True)
        res.first_name = 'Danny'
        res.reservation_number = 'NEWRES'
        self.assertEqual(self.db.insert_data([res.get_tuple()]), True)
        data = self.db.get_all()
        self.assertEqual(len(data), 2)
        self.db.print_all()
        self.db.delete_reservation_by_name('HSUMAN')
        # self.assertEqual(len(data), 1)
        data = self.db.get_all()
        self.assertEqual(data[0][3], 'NEWRES')
    
    def test_load_persistence(self):
        res = ReservationInfo('Andy', 'Hsu', 'HSUMAN', 0)
        self.db.insert_data([res.get_tuple()])
        res = ReservationInfo('Tim', 'Kang', 'TIMMAN', 1)
        self.db.insert_data([res.get_tuple()])
        new_db = DbProxy('test_db', verbosity)
        data = new_db.get_all()
        self.assertEqual(data[0][3], 'HSUMAN')
        self.assertEqual(data[1][3], 'TIMMAN')

class SouthwestApiProxy(SouthwestApi):
    def __init__(self, verbosity):
        super(SouthwestApiProxy, self).__init__(verbosity)

class SouthwestApiTest(unittest.TestCase):
    def setUp(self):
        global verbosity
        self.api = SouthwestApiProxy(verbosity)

    def test_check_in_unknown_reservation(self):
        res = ReservationInfo('Andy', 'Hsu', 'HSUMAN', 0)
        result = self.api.check_in_flight(res)
        self.assertTrue(result == HttpCode.RESERVATION_NOT_FOUND.value or\
                        result == HttpCode.FORBIDDEN.value)


class CheckInSystemProxy(CheckInSystem):
    """ Reservation System inherited class
    """
    def __init__(self, verbosity, db_name):
        super(CheckInSystemProxy, self).__init__(verbosity, db_name)
        self.current_time = 0

    def create_reservation_force_check_in_time(self, first_name, last_name, reservation_number, seconds_until_checkin):
        # Since the reservation system will always take the real flight time and subtract 24 hours from it, this is a hack
        # to add 24 hours to the time returned from get_flight_time(), which will ensure that we check in N seconds from this call
        self.southwest_api.get_flight_time=MagicMock(return_value=seconds_until_checkin + self.ONE_DAY_IN_SECONDS)

        # Fake southwest api to make sure it is always successful
        self.southwest_api.check_in_flight=MagicMock(return_value=HttpCode.SUCCESS.value)
        self.add_reservation(first_name, last_name, reservation_number)

    def _get_current_time(self) -> int:
        self.current_time = self.current_time + self.polling_time_seconds
        return self.current_time

class CheckInSystemTest(unittest.TestCase):
    def setUp(self):
        global verbosity
        self.system = CheckInSystemProxy(verbosity, 'test_db')

    def tearDown(self):
        self.system.__del__()
        self.system.reservation_manager.db.delete_all()

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
        self.system.delete_reservation_by_name("KNJ653")
        self.assertEqual(self.system.get_first_reservation(), None)
        self.assertEqual(self.system.get_number_of_reservations(), 0)

        self.system.add_reservation("Esther", "Hsu", "L8M194")
        self.system.add_reservation("Candy", "Hsu", "PEE1NA")
        self.assertEqual(self.system.get_number_of_reservations(), 2)

        self.system.delete_reservation_by_name("PEE1NA")
        self.assertEqual(self.system.get_number_of_reservations(), 1)

        self.system.add_reservation("Tim", "Hsu", "UHR249")
        self.system.add_reservation("Tim", "Hsu", "YTE923")
        self.system.add_reservation("Tim", "Hsu", "NWI093")
        self.assertEqual(self.system.get_number_of_reservations(), 4)

        self.system.delete_reservation_by_name("UHR249")
        self.system.delete_reservation_by_name("YTE923")
        self.system.delete_reservation_by_name("NWI093")
        self.system.delete_reservation_by_name("L8M194")
        self.assertEqual(self.system.get_number_of_reservations(), 0)

    def test_delete_unknown_reservation(self):
        self.assertEqual(self.system.get_number_of_reservations(), 0)
        self.assertEqual(self.system.delete_reservation_by_name("UHR249"), ErrorCode.UNKNOWN_RESERVATION)
        self.assertEqual(self.system.get_number_of_reservations(), 0)
        self.system.add_reservation("Tim", "Hsu", "UHR249")
        self.assertEqual(self.system.get_number_of_reservations(), 1)
        self.assertEqual(self.system.delete_reservation_by_name("LHR248"), ErrorCode.UNKNOWN_RESERVATION)
        self.assertEqual(self.system.delete_reservation_by_name("UHR249"), ErrorCode.SUCCESS)
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
        time.sleep(2)
        self.assertEqual(self.system.get_number_of_reservations(), 0)

    def test_empty_db(self):
        self.assertEqual(self.system.reservation_manager.db.get_all(), [])
        self.assertEqual(self.system.get_number_of_reservations(), 0)

    def test_add_to_db(self):
        self.system.add_reservation("Andy", "Hsu", "KNJ653")
        self.system.add_reservation("Matt", "Bilello", "BILELL")
        self.assertEqual(self.system.get_number_of_reservations(), 2)
        self.assertEqual(self.system.reservation_manager.db.get_all()[0][3], 'KNJ653')
        self.assertEqual(self.system.reservation_manager.db.get_all()[1][3], 'BILELL')
        self.system.delete_reservation_by_name("KNJ653")
        self.assertEqual(self.system.get_number_of_reservations(), 1)
        self.assertEqual(self.system.reservation_manager.db.get_all()[0][3], 'BILELL')
    
    def test_init_from_persistence(self):
        # This test makes sure that when we init a database from persistence, it is sorted and
        # put into the heap correctly
        self.system.create_reservation_force_check_in_time("Danny", "Tran", "LNJ653", 1)
        self.system.create_reservation_force_check_in_time("Andy", "Hsu", "LAJ653", 0)
        self.system.create_reservation_force_check_in_time("Tim", "Blah", "AAAAB3", 9)
        self.system.create_reservation_force_check_in_time("Jack", "Blah", "AAAAB4", 21)
        self.system.create_reservation_force_check_in_time("rob", "Blah", "AAAAB5", 11)
        newsystem = CheckInSystemProxy(verbosity, 'test_db')
        data = newsystem.reservation_manager.db.get_all()
        prev = -1
        # Column 4 is check in time
        for i, obj in enumerate(data):
            self.assertTrue(obj[4] > prev)
            prev = obj[4]
        # Since the new system has its own check in thread, we need to delete it to make
        # sure the thread joins too
        newsystem.__del__()

    def test_init_from_persistence_check_heap(self):
        expected_times = [0, 1, 4, 7, 9]
        self.system.create_reservation_force_check_in_time("Danny", "Tran", "LNJ653", 1)
        self.system.create_reservation_force_check_in_time("Andy", "Hsu", "LAJ653", 0)
        self.system.create_reservation_force_check_in_time("Tim", "Blah", "AAAAB3", 4)
        self.system.create_reservation_force_check_in_time("Jack", "Blah", "AAAAB4", 9)
        self.system.create_reservation_force_check_in_time("rob", "Blah", "AAAAB5", 7)
        # Stop the thread that will pop from 
        self.system.run_thread = False
        newsystem = CheckInSystemProxy(verbosity, 'test_db')
        newsystem.run_thread = False
        reservation_heap = newsystem.reservation_manager.reservation_heap
        i = 0
        while len(reservation_heap) > 0:
            res = heapq.heappop(reservation_heap)
            self.assertEqual(res.check_in_time, expected_times[i])
            i += 1
        newsystem.__del__()

if __name__ == '__main__':
    valid_verbosity_levels = range(0, 3)
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbosity', default=0)
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    verbosity = int(args.verbosity)

    sys.argv[1:] = args.unittest_args
    unittest.main()
