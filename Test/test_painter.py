import unittest
from ColorZoner.Painter.Painter import Painter
from os import path


class TestPainter(unittest.TestCase):
    """Unit Test for ColorZoner.Painter"""

    def setUp(self):
        self.image_dir = ('Test')
        self.image_bank_dir = path.join('Test','color_bank')

    def test_painter(self):
        src_img_path = path.join(self.image_dir, 'kirk.jpg')
        dest_img_path = path.join(self.image_dir, 'kirk_painted.png')

        painter = Painter(src_img_path,
                self.image_bank_dir,
                split_thresh=1500,
                minsize = 5,
                group_thresh = 40)
        self.assertIsNotNone(painter.src_img)
        self.assertTrue(len(painter.imagebank.entries) == 32)

        painter.generate_groups()
        self.assertIsNotNone(painter.node_groups)
        self.assertTrue(len(painter.node_groups) > 0)

        painter.get_pictures_for_groups()
        self.assertIsNotNone(painter.pic_list)
        self.assertTrue(len(painter.pic_list) == len(painter.node_groups))

        painter.paint()

        print 'Saving image to %s' % dest_img_path
        painter.dest_image.save(dest_img_path, 'PNG')


if __name__ == '__main__':
    unittest.main()

