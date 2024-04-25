import unittest
from Gameproto import Board, Ships


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(10, 10)

    def test_board_initialized_correctly(self):
        self.assertEqual(self.board.rows, 10)
        self.assertEqual(self.board.columns, 10)
        self.assertEqual(len(self.board.board), 100)
        self.assertEqual(self.board.board.count("O"), 100)

class TestShips(unittest.TestCase):
    def setUp(self):
        self.ships = Ships(10, 10)

    def test_generate_ship(self):
        self.ships.generate_ship(5, "A")
        self.assertEqual(len(self.ships.ship_list), 1)
        self.assertEqual(self.ships.ship_list[0][1], 5)
        self.assertIn("A", self.ships.board)

if __name__ == "__main__":
    unittest.main()