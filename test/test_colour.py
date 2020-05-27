import unittest
import Colour


class TestColour(unittest.TestCase):
    def test_colour(self):
        # ARRANGE

        # ACT
        colour = Colour.white

        # ASSERT
        self.assertIsInstance(colour, Colour.Colour)

    def test_rgb_of_colour(self):
        # ARRANGE
        red = Colour.red

        # ACT
        r, g, b = red.rgb

        # ASSERT
        self.assertEqual(r, 1)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)

    def test_faded(self):
        # ARRANGE
        red = Colour.red

        # ACT
        output = red.faded()

        # ASSERT
        r, g, b = output.rgb
        self.assertEqual(r, 1)
        self.assertEqual(g, 0.9)
        self.assertEqual(b, 0.9)

    def test_alias(self):
        # ARRANGE
        phase1 = Colour.phase_1

        # ACT
        rgb_phase1 = phase1.rgb

        # ASSERT
        rgb_yellow = Colour.yellow.rgb
        self.assertEqual(rgb_phase1, rgb_yellow)


if __name__ == '__main__':
    unittest.main()
