from ColorZoner import generate_quad_tree, generate_leaf_groups, draw_quadtree_leaf_colors, draw_group_colors
import Image

def TestColorZoner(in_file, out_file, splitthresh, minsize, groupthresh):

    img = Image.open(in_file)
    print 'Generating quad tree on %s' % in_file
    root = generate_quad_tree(img, splitthresh, minsize)
    print 'Drawing leaves...'
    out_img = draw_quadtree_leaf_colors(root, img.size)
    print 'Saving tree.png...'
    out_img.save('tree.png','PNG')
    print 'Making leaf groups...'
    groups = generate_leaf_groups(root, groupthresh)
    print 'Drawing groups...'
    out_img = draw_group_colors(groups, img.size)
    print 'Saving image...'
    out_img.save(out_file,'PNG')  
    print 'Saved to %s' % out_file
 
if __name__ == '__main__':
    in_file = 'kirk.jpg'
    out_file = 'kirk_zoned.png'
    splitthresh = 1200
    minsize = 5
    groupthresh = 80

    TestColorZoner(in_file, out_file, splitthresh, minsize, groupthresh)

