import sys
sys.path.append('../src')
import unittest
import ReservationSystem

class ReservationSystemTest(unittest.TestCase):
    def setUp(self):
        self.system = ReservationSystem.ReservationSystem()

    def tearDown(self):
        pass

    def test_get_first_reservation(self):
        self.assertEqual(self.system.getFirstReservation(), None)
        self.system.createReservation("Andy", "Hsu", "KNJ653")
        self.assertEqual(self.system.getFirstReservation().first_name, "Andy")

    def test_create_reservation_scheduler(self):
        self.assertNotEqual(self.system.scheduler, None)

    def test_create_reservation_duplicate(self):
        self.system.createReservation("Andy", "Hsu", "KNJ653")
        self.assertFalse(self.system.createReservation("Andy", "Hsu", "KNJ653"))

    def test_create_reservation(self):
        self.system.createReservation("Andy", "Hsu", "KNJ653")
        self.assertEqual(self.system.getFirstReservation().first_name, "Andy")
        self.assertEqual(self.system.getNumberOfReservations(), 1)
        self.system.createReservation("Esther", "Hsu", "KNJ654")
        self.assertEqual(self.system.getNumberOfReservations(), 2)
        self.system.createReservation("Candy", "Hsu", "KNl655")
        self.assertEqual(self.system.getNumberOfReservations(), 3)
        self.system.createReservation("Tim", "Hsu", "KNJ656")
        self.assertEqual(self.system.getNumberOfReservations(), 4)

    def test_delete_reservations(self):
        self.system.createReservation("Andy", "Hsu", "KNJ653")
        self.assertEqual(self.system.getFirstReservation().first_name, "Andy")
        self.assertEqual(self.system.getNumberOfReservations(), 1)
        self.system.deleteReservation("KNJ653")
        self.assertEqual(self.system.getFirstReservation(), None)
        self.assertEqual(self.system.getNumberOfReservations(), 0)

        self.system.createReservation("Esther", "Hsu", "L8M194")
        self.system.createReservation("Candy", "Hsu", "PEE1NA")
        self.assertEqual(self.system.getNumberOfReservations(), 2)

        self.system.deleteReservation("PEE1NA")
        self.assertEqual(self.system.getNumberOfReservations(), 1)

        self.system.createReservation("Tim", "Hsu", "UHR249")
        self.system.createReservation("Tim", "Hsu", "YTE923")
        self.system.createReservation("Tim", "Hsu", "NWI093")
        self.assertEqual(self.system.getNumberOfReservations(), 4)

        self.system.deleteReservation("UHR249")
        self.system.deleteReservation("YTE923")
        self.system.deleteReservation("NWI093")
        self.system.deleteReservation("L8M194")
        self.assertEqual(self.system.getNumberOfReservations(), 0)



if __name__ == '__main__':
    unittest.main()
