import unittest
from graphics.cairo import Draw


class LoadImageTest(unittest.TestCase):
    def test_loadimage(self):
        # arrange
        canvas = Draw.Canvas((0,0), 500, 500)

        # act
        retvalue = Draw.load_image(canvas, 'test/X.png', (250, 250), 200, 200)

        # assert
        self.assertTrue(retvalue)
        self.assertEqual('Public domain image', canvas.credits_info['test/X.png'].strip())

    def test_loadimage_unavailable(self):
        # arrange
        canvas = Draw.Canvas((0,0), 500, 500)

        # act
        retvalue = Draw.load_image(canvas, 'test/Doesnotexist.png', (250, 250), 200, 200)

        # assert
        self.assertFalse(retvalue)

    def test_loadimage_nocredits(self):
        # arrange
        canvas = Draw.Canvas((0,0), 500, 500)

        # act
        with self.assertRaisesRegex(Exception, 'No credits file found.*'):
            Draw.load_image(canvas, 'test/NoCredits.png', (250, 250), 200, 200)

        # assert
        pass


if __name__ == '__main__':
    unittest.main()
