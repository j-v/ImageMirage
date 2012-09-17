'''Wrapt the QuadTree and ImageBank modules to make the magic happen.'''
from ColorZoner.QuadTree import QuadTreeFunctions
from ColorZoner.ImageBank import ImageBank
from PIL import Image
from ColorZoner import Math
import os


def paint_group(src_image, dest_image, group):
    '''Uses the node group as a maskk to paint src_image onto dest_image'''
    mask = group.get_mask()
    x1, y1, x2, y2 = group.get_bounding_box()
    width, height = x2 + 1 - x1, y2 + 1 - y1
    src_width, src_height = src_image.size
    if width > src_width:
        print 'bad width'
        # hope this doesn't happen for now
        # TODO should use tiling
        return
    elif width < src_width:
        # crop src_image horizontally
        # src_image = src_image.crop((0,0,width,src_height))
        src_width = width
    if height > src_height:
        print 'bad height'
        # hope this doesn't happen for now
        # TODO use tiling?
        return
    elif height < src_height:
        # crop src_image vertically
        # src_image = src_image.crop((0,0,src_width,height))
        src_height = height

    old_width, old_height = src_image.size
    if src_width != old_width or src_height != old_height:
        box = (0, 0, src_width, src_height)
        src_image = src_image.crop(box)
        mask = mask.crop(box)

    dest_image.paste(src_image,
            box=(x1, y1, x1 + src_width, y1 + src_height),
            mask = mask)


class Painter(object):
    """Painter class wraps QuadTree and ImageBank"""
    def __init__(self, src_img_path, imagebank_path,
                 split_thresh=1200, minsize=10, group_thresh=75):
        self.src_img_path = src_img_path
        self.imagebank_path = imagebank_path
        self.split_thresh = split_thresh
        self.minsize = minsize
        self.group_thresh = group_thresh

        # load the source image
        self.src_img = Image.open(src_img_path)
        # Initialize destination image
        self.dest_image = Image.new('RGB', self.src_img.size)

        # load the image bank
        self.imagebank = ImageBank.open(imagebank_path)

        self.node_groups = None
        self.pic_list = None

    def generate_groups(self):
        print 'Painter: generating quad tree...'
        self.quadtree = QuadTreeFunctions.generate_quad_tree(
            self.src_img, self.group_thresh, self.minsize)
        print 'Painter: generating node groups...'
        self.node_groups = QuadTreeFunctions.generate_leaf_groups(
            self.quadtree,
            self.group_thresh)

    def get_pictures_for_groups(self):
        print 'Painter: getting pictures for groups'
        ''' Builds a list a list of filenames, in the same order as the groups,
        corresponding to best fit for color '''

        if self.node_groups is None:
            raise Exception(
                "Groups must be generated before calling get_pictures_for_groups"
            )

        self.pic_list = []

        # if image_bank has no entries
        if len(self.imagebank.entries) == 0:
            raise Exception(
                "Image bank must contain at least one entry")  # TODO

        for group in self.node_groups:
            best_file = None
            best_dist = float('inf')
            for entry in self.imagebank.entries:
                dist = Math.distance_3d_euclid(group.mean, entry.mean)
                if dist < best_dist:
                    best_file = entry.filename
                    best_dist = dist
            self.pic_list.append(best_file)

    def paint(self):
        print 'Painter: painting'
        if self.pic_list == None:
            raise Exception("pic list must be generated before calling Painter.paint")
        for group, pic in zip(self.node_groups, self.pic_list):
            pic_path = os.path.join(self.imagebank.directory, pic)
            pic = Image.open(pic_path)
            paint_group(pic, self.dest_image, group)


