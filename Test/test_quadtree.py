import unittest
from ColorZoner.QuadTree.QuadTreeFunctions import (
    generate_quad_tree, generate_leaf_groups,
    draw_quadtree_leaf_colors, draw_group_colors)
import Image
from os import path


class TestQuadTree(unittest.TestCase):
    def setUp(self):
        self.image_dir = 'test'

    def test_everything(self):  # TODO change this name, organize better..
        in_file = path.join(self.image_dir, 'kirk.jpg')
        out_file = path.join(self.image_dir, 'kirk_out.png')
        leaf_file = path.join(self.image_dir, 'kirk_leaves.png')
        mask_file = path.join(self.image_dir, 'kirk_mask.png')

        splitthresh = 1500  # 1200 # Lower means fewer nodes are split, faster algo
        minsize = 5  # Lower means higher detail in splitting, slower algo
        groupthresh = 40  # 80 # Lower means fewer nodes are grouped back together, faster algo

        img = Image.open(in_file)
        print 'Generating quad tree on %s' % in_file
        root = generate_quad_tree(img, splitthresh, minsize)
        print 'Drawing leaves...'
        out_img = draw_quadtree_leaf_colors(root, img.size)
        print 'Saving leaf image to %s...' % leaf_file
        out_img.save(leaf_file, 'PNG')
        print 'Making leaf groups...'
        groups = generate_leaf_groups(root, groupthresh)
        print 'Drawing groups...'
        out_img = draw_group_colors(groups, img.size)
        print 'Saving image...'
        out_img.save(out_file, 'PNG')
        print 'Saved to %s' % out_file

        # Test masking
        print 'Testing group.get_mask'
        paste_img = Image.new('RGB', img.size)
        for group in groups:
            mask = group.get_mask()
            #color_img = Image.new('RGB', mask.size)
            #draw = ImageDraw.Draw(color_img)
            color = tuple(int(i) for i in group.mean)
            #draw.rectangle([(0,0), mask.size], fill=color, outline=color)
            x1, y1, x2, y2 = group.get_bounding_box()
            paste_img.paste(color, box=(x1, y1, x2 + 1, y2 + 1), mask=mask)
        paste_img.save(mask_file, 'PNG')
        print 'Saved %s' % mask_file

    @unittest.skip("Incorrect implementation") #TODO
    def test_groups_dont_intersect(self):
        in_file = path.join(self.image_dir, 'kirk.jpg')

        splitthresh = 1500  # 1200 # Lower means fewer nodes are split, faster algo
        minsize = 5  # Lower means higher detail in splitting, slower algo
        groupthresh = 40  # 80 # Lower means fewer nodes are grouped back together, faster algo

        img = Image.open(in_file)
        print 'Generating quad tree on %s' % in_file
        root = generate_quad_tree(img, splitthresh, minsize)
        print 'Making leaf groups...'
        groups = generate_leaf_groups(root, groupthresh)

        # check groups for overlapping
        overlapping = False
        for i in range(len(groups)):
            g1 = groups[i]
            b1x1, b1y1, b1x2, b1y2 = g1.get_bounding_box()
            for j in range(i+1, len(groups)):
                b2x1, b2y1, b2x2, b2y2 = groups[j].get_bounding_box()
                if b1y2 < b2y1 or \
                        b1y1 > b2y2 or \
                        b1x2 < b2x1 or \
                        b1x1 > b2x2:
                            continue
                overlapping = True
                print 'Group %d and group %d overlap' % (i, j)
                print 'box %d: %d %d %d %d' % (i, b1x1, b1y1, b1x2, b1y2)
                print 'box %d: %d %d %d %d' % (j, b2x1, b2y1, b2x2, b2y2)

        self.assertFalse(overlapping)


if __name__ == '__main__':
    unittest.main()
