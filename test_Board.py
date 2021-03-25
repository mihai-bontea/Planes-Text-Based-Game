import unittest
from Board import Board

class TestBoard(unittest.TestCase):

    def test_initialize(self):
        board = Board()
        data = board.data
        for i in range(0, 8):
            for j in range(0, 8):
                self.assertEqual(data[i][j], 0)

    def test_hit_air(self):
        board = Board()
        for i in range(0, 8):
            for j in range(0, 8):
                board.hit_air(i, j)
        
        for i in range(0, 8):
            for j in range(0, 8):
                self.assertEqual(board.data[i][j], 3)

    def test_hit_hull(self):
        board = Board()
        for i in range(0, 8):
            for j in range(0, 8):
                board.hit_hull(i, j)
        
        for i in range(0, 8):
            for j in range(0, 8):
                self.assertEqual(board.data[i][j], 4)

    def test_hit_cockpit(self):
        board = Board()
        for i in range(0, 8):
            for j in range(0, 8):
                board.hit_cockpit(i, j)
        
        for i in range(0, 8):
            for j in range(0, 8):
                self.assertEqual(board.data[i][j], 5)


if __name__ == '__main__':
    unittest.main()