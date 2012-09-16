from collections import deque
from PIL import Image, ImageStat, ImageDraw
import math
import argparse

from QuadTree import QuadTreeNode, NodeGroup

'''
Calculate 3d euclidian magnitude of the vector v
arg v: indexable of length 3 
'''
#TODO fix dox
def magnitude_3d_euclid(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def distance_3d_euclid(v1,v2):
    return magnitude_3d_euclid(tuple(v2[i]-v1[i] for i in range(3)))

''' 
Split an image into a quad tree, splitting conditionally based on variance in color
at each node.
Results in a tree, whose leaves can be used to draw a kind of pixelized version of 
the original.
arg image
arg thresh - Variance threshold for conditional node expansion 
arg minsize - Minimum size of node, blockin node expansion
'''
#TODO fix dox
def generate_quad_tree(image, thresh, minsize):
    width, height = image.size
    x1, y1, x2, y2 = 0, 0, width - 1, height - 1
    rootNode = QuadTreeNode(image,x1,y1,x2,y2)

    q = deque()
    q.append(rootNode)

    while len(q) > 0:
        node = q.popleft()
        # Check minsize condition
        if node.x2 - node.x1 < minsize or node.y2 - node.y1 < minsize:
            continue
        # Check thresh condition
        elif magnitude_3d_euclid(node.var) < thresh: 
            continue
        else:
            # expand node
            nw_image = image.crop( (
                      node.x1, node.y1, 
                      (node.x1+node.x2)/2, (node.y1+node.y2)/2 ) )
            ne_image = image.crop( (
                      (node.x1+node.x2)/2, node.y1, 
                      node.x2, (node.y1+node.y2)/2 ) )
            se_image = image.crop( 
                     ((node.x1+node.x2)/2, (node.y1+node.y2)/2 , 
                      node.x2, node.y2 ) )
            sw_image = image.crop( (node.x1, (node.y1+node.y2)/2 
                      ,(node.x1+node.x2)/2, node.y2) )
            
            nw_image.load()
            ne_image.load()
            se_image.load()
            sw_image.load()

            node.nw_child = QuadTreeNode(nw_image, node.x1, 
                                 node.y1, (node.x1+node.x2)/2, (node.y1+node.y2)/2, node)
            node.ne_child = QuadTreeNode(ne_image, (node.x1+node.x2)/2, 
                                 node.y1, node.x2, (node.y1+node.y2)/2, node)
            node.se_child = QuadTreeNode(se_image, (node.x1+node.x2)/2, 
                                 (node.y1+node.y2)/2 , node.x2, node.y2, node)
            node.sw_child = QuadTreeNode(sw_image, node.x1, 
                                 (node.y1+node.y2)/2 ,(node.x1+node.x2)/2, node.y2, node)

            for child in [node.nw_child, node.ne_child, node.se_child, node.sw_child]:
                q.append(child)

    return rootNode

def expand_group(ref_node, root, group_thresh):
    '''Helper function for generate_leaf_groups'''

    q = deque()
    q.append(root)
    group = ref_node.group # must not be None

    while len(q) > 0:
        node = q.popleft()
        if node == ref_node or node.group != None:
            continue
        # check for "collision"
        if node.y2 < ref_node.y1 - 1 or \
            node.y1 > ref_node.y2 + 1 or \
            node.x2 < ref_node.x1 - 1 or \
            node.x1 > ref_node.x2 + 1:
                continue
        if node.ne_child == None:
            # node touches the ref_node, check if it should be part of the group
            mean_diff = [0., 0., 0.]
            for i in range(3):
                mean_diff[i] = group.mean[i] - node.mean[i]

            if magnitude_3d_euclid(mean_diff) < group_thresh:
                group.add_node(node)
                group.refresh_stats()
        else:
            for child in [node.nw_child, node.ne_child, node.se_child, node.sw_child]:
                q.append(child)

def generate_leaf_groups(root, group_thresh):
    '''Output a list of node groups'''
    groups = []
    q = deque()
    q.append(root)

    # BF Traversal
    while len(q) > 0:
        node = q.popleft()
        if node.ne_child == None:
            if node.parent == None:
                pass # root node
            else:
                if node.group == None:
                    group = NodeGroup();
                    group.add_node(node)
                    group.refresh_stats()
                    groups.append(group)
                    node.group = group
                
                expand_group(node, root, group_thresh)
        else:
            for child in [node.nw_child, node.ne_child, node.se_child, node.sw_child]:
                q.append(child)
    
    return groups

def draw_quadtree_leaf_colors(root, size):
    image = Image.new('RGB', size)
    draw = ImageDraw.Draw(image)

    q = deque()
    q.append(root)

    while len(q) > 0:
        node = q.popleft()
        if node.ne_child == None: # if one child is None then they should all be None
            color = tuple(int(i) for i in node.mean)
            draw.rectangle([(node.x1, node.y1), (node.x2, node.y2)],
                                    outline=color,
                                    fill=color)
        else:
            for child in [node.nw_child, node.ne_child, node.se_child, node.sw_child]:
                q.append(child)

    return image

def draw_group_colors(groups, size):
    image = Image.new('RGB', size)
    draw = ImageDraw.Draw(image)

    for group in groups:
        color = tuple(int(i) for i in group.mean)
        for node in group.nodes:
            draw.rectangle([(node.x1, node.y1), (node.x2, node.y2)],
                                    outline=color,
                                    fill=color)
 
    return image

def get_pictures_for_groups(groups, image_bank):
    '''get_pictures_for_groups(list(NodeGroup)) -> list(str)

    returns a list of filenames, in the same order as the groups, 
    corresponding to best fit for color'''

    pic_list = []

    # if image_bank has no entries
    if len(image_bank.entries) == 0:
        raise Exception("Image bank must contain at least one entry") # TODO

    for group in groups:
        best_file = None
        best_dist = float('inf')
        for entry in image_bank.entries:
            dist = distance_3d_euclid(group.mean, entry.mean)
            if dist < best_dist:
                best_file = entry.filename
                best_dist = dist
        pic_list.append(best_file)

    return pic_list


def paint_group(src_image, dest_image, group):
    '''Uses the node group as a maskk to paint src_image onto dest_image'''
    mask = group.get_mask()
    x1,y1,x2,y2 = group.get_bounding_box()
    dest_image.paste(src_image, box=(x1,y1,x2+1,y2+1), mask = mask)


if __name__ == '__main__':
     DEFAULT_SPLIT_THRESH = 1200
     DEFAULT_MINSIZE = 20
     DEFATUL_GROUP_THRESH = 75

     parser = argparse.ArgumentParser(description='ColorZoner for your pleasure')
     parser.add_argument('in_file', metavar='IN_FILE', type=str,
             help='The input image file')
     parser.add_argument('out_file', metavar='OUT_FILE', type=str,
             help='The output image file, should have .png extension')
     parser.add_argument('-s', '--splitthresh', type=int, 
             default=DEFAULT_SPLIT_THRESH,
             help="Threshold for splitting up the image into regions")
     parser.add_argument('-m', '--minsize', type=int, default=DEFAULT_MINSIZE,
             help='Minimum dimension of squares to break the image down into')
     parser.add_argument('-g', '--groupthresh', type=int, default=DEFATUL_GROUP_THRESH,
             help='Threshold for joining groups together')

     args = parser.parse_args()


     img = Image.open(args.in_file)
     print 'Generating quad tree on %s' % args.in_file
     root = generate_quad_tree(img, args.splitthresh, args.minsize)
     print 'Drawing leaves...'
     out_img = draw_quadtree_leaf_colors(root, img.size)
     print 'Saving tree.png...'
     out_img.save('tree.png','PNG')
     print 'Making leaf groups...'
     groups = generate_leaf_groups(root, args.groupthresh)
     print 'Drawing groups...'
     out_img = draw_group_colors(groups, img.size)
     print 'Saving image...'
     out_img.save(args.out_file,'PNG')  
     print 'Saved to %s' % args.out_file

