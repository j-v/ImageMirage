from ColorZoner import generate_quad_tree, generate_leaf_groups, draw_quadtree_leaf_colors, draw_group_colors
import Image, ImageDraw

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

    # Test masking
    print 'Testing group.get_mask'
    paste_img = Image.new('RGB', img.size)
    from random import random
    for group in groups:
       if random() < 0.5: continue
       mask = group.get_mask()
       color_img = Image.new('RGB', mask.size)
       #draw = ImageDraw.Draw(color_img)
       color = tuple(int(i) for i in group.mean)
       #draw.rectangle([(0,0), mask.size], fill=color, outline=color)
       x1,y1,x2,y2 = group.get_bounding_box()
       paste_img.paste(color, box=(x1,y1,x2+1,y2+1), mask=mask)
    paste_img.save('mask_test.png', 'PNG')   
    print 'Saved mask_test.png'

if __name__ == '__main__':
    in_file = 'kirk.jpg'
    out_file = 'kirk_zoned.png'
    splitthresh = 1500# 1200 # Lower means fewer nodes are split, faster algo
    minsize = 20 #5 # Lower means higher detail in splitting, slower algo
    groupthresh = 40 #80 # Lower means fewer nodes are grouped back together, faster algo

    TestColorZoner(in_file, out_file, splitthresh, minsize, groupthresh)

