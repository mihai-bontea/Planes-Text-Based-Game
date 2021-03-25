import unittest
from Plane import Plane

class PLaneTest(unittest.TestCase):
    
    def test_cockpit_coords(self):
        upwards_plane = Plane("U", 3, "D")
        downwards_plane = Plane("D", 6, "D")
        leftwards_plane = Plane("L", 4, "C")
        rightwards_plane = Plane("R", 4, "F")

        self.assertEqual(upwards_plane.cockpit_coords, (2, 3))
        self.assertEqual(downwards_plane.cockpit_coords, (5, 3))
        self.assertEqual(leftwards_plane.cockpit_coords, (3, 2))
        self.assertEqual(rightwards_plane.cockpit_coords, (3, 5))

    def test_body_length(self):
        upwards_plane = Plane("U", 3, "D")
        downwards_plane = Plane("D", 6, "D")
        leftwards_plane = Plane("L", 4, "C")
        rightwards_plane = Plane("R", 4, "F")

        u_body = upwards_plane.get_body()
        d_body = downwards_plane.get_body()
        l_body = leftwards_plane.get_body()
        r_body = rightwards_plane.get_body()

        self.assertEqual(len(u_body), 9)
        self.assertEqual(len(d_body), 9)
        self.assertEqual(len(l_body), 9)
        self.assertEqual(len(r_body), 9)
        

if __name__ == '__main__':
    unittest.main()