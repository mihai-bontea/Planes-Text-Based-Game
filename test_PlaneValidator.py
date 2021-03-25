import unittest
from PlaneValidator import PlaneValidator
from Board import Board
from Plane import Plane

class TestPlaneValidator(unittest.TestCase):

    def test_basic_check(self):
        self.assertTrue(PlaneValidator.basic_check(Plane("U", 1, "A")))
        self.assertTrue(PlaneValidator.basic_check(Plane("D", 8, "H")))
        self.assertTrue(PlaneValidator.basic_check(Plane("L", 2, "D")))
        self.assertTrue(PlaneValidator.basic_check(Plane("R", 6, "E")))

    def test_does_it_fit(self):
        self.assertTrue(PlaneValidator.does_it_fit(Plane("U", 3 , "D")))
        self.assertTrue(PlaneValidator.does_it_fit(Plane("D", 5 , "D")))
        self.assertTrue(PlaneValidator.does_it_fit(Plane("L", 4 , "C")))
        self.assertTrue(PlaneValidator.does_it_fit(Plane("R", 4 , "F")))

        self.assertFalse(PlaneValidator.does_it_fit(Plane("U", 1 , "A")))

    def test_no_overlap(self):
        board = Board()
        plane = Plane("U", 3 , "D")
        self.assertTrue(PlaneValidator.no_overlap(plane, board))
        board.add_plane(plane)
        self.assertFalse(PlaneValidator.no_overlap(plane, board))

    


if __name__ == '__main__':
    unittest.main()