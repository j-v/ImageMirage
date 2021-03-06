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
        print 'Checking for overlapping groups'
        overlapping = False
        for i in range(len(groups)):
            for j in range(i+1, len(groups)):

                for n1 in groups[i].nodes:
                    for n2 in groups[j].nodes:
                        if n1.y2 <= n2.y1 or \
                                n1.y1 >= n2.y2 or \
                                n1.x2 <= n2.x1 or \
                                n1.x1 >= n2.x2:
                                    continue
                        overlapping = True
                        print 'Found overlap in groups %d and %d: (%d,%d,%d,%d)(%d,%d,%d,%d)' % (
                                i, j, n1.x1, n1.y1, n1.x2, n1.y2, n2.x1, n2.y1, n2.x2, n2.y2)

        self.assertFalse(overlapping)


if __name__ == '__main__':
    unittest.main()
