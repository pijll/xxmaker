from Definitions import *
import unittest
import Hexag
import math


class HexagTest(unittest.TestCase):
    def test_basic_hexag(self):
        # arrange
        # act
        hexag = Hexag.Hexag(size=100)

        # assert
        self.assertIsInstance(hexag, Hexag.Hexag)
        self.size = 100
        self.unit_size = 50

    def test_horizontal_hexag(self):
        # arrange
        # act
        hexag = Hexag.Hexag(size=100, orientation=HORIZONTAL)

        # assert
        self.assertEqual(hexag.orientation, HORIZONTAL)
        self.assertEqual(hexag.unit_length, 50)
        self.assertAlmostEqual(hexag.side_length, 100/math.sqrt(3))
        self.assertAlmostEqual(hexag.width, 100)
        self.assertAlmostEqual(hexag.height, 200/math.sqrt(3))

    def test_vertical_hexag(self):
        # arrange
        # act
        hexag = Hexag.Hexag(size=100, orientation=VERTICAL)

        # assert
        self.assertEqual(hexag.orientation, VERTICAL)
        self.assertEqual(hexag.unit_length, 50)
        self.assertAlmostEqual(hexag.side_length, 100 / math.sqrt(3))
        self.assertAlmostEqual(hexag.height, 100)
        self.assertAlmostEqual(hexag.width, 200 / math.sqrt(3))

    def test_tile_edges(self):
        # arrange
        # act
        tile_edges = list(Hexag.tile_sides(HORIZONTAL))

        # assert
        self.assertEqual(len(tile_edges), 6)
        for edge in tile_edges:
            self.assertAlmostEqual(edge.x**2 + edge.y**2, 1)


if __name__ == '__main__':
    unittest.main()
