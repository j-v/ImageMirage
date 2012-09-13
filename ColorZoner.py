from collections import deque
from PIL import Image, ImageStat, ImageDraw
import sys
import math

GROUP_THRESH = 100

class QuadTreeNode:
	def __init__(self, image, x1, y1, x2, y2, parent=None): # all should be ints
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

		self.parent = parent

		self.ne_child = None
		self.nw_child = None
		self.se_child = None
		self.sw_child = None

		stats = ImageStat.Stat(image)
		self.mean = stats.mean
		self.var = stats.var

		self.group = None

class NodeGroup:
   def __init__(self):
      self.nodes = []
      self.mean = [0., 0., 0.]
      self.var = [0., 0., 0.]

   def add_node(self, node):
      node.group = self
      self.nodes.append(node)

   def refresh_stats(self):
      mean_accum = [0., 0., 0.]
      var_accum = [0., 0., 0.]
      pix_accum = 0

      # iterate through all nodes, do weighted summing
      for node in self.nodes:
	 pix = (node.y2-node.y1)*(node.x2-node.x1)
	 pix_accum += pix
	 for i in range(3):
	    mean_accum[i] += node.mean[i] * pix
	    var_accum[i] += node.var[i] * pix
      
      # normalization
      for i in range(3):
	 self.mean[i] = mean_accum[i] / float(pix_accum)
	 self.var[i] = var_accum[i] / float(pix_accum)



def magnitude_3d_euclid(v):
   return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def generate_quad_tree(image, thresh, minsize):
   width, height = image.size
   x1, y1, x2, y2 = 0, 0, width - 1, height - 1
   rootNode = QuadTreeNode(image,x1,y1,x2,y2)

   q = deque()
   q.append(rootNode)

   while len(q) > 0:
      node = q.popleft()
      # 
      if node.x2 - node.x1 < minsize or node.y2 - node.y1 < minsize:
	 continue
      elif magnitude_3d_euclid(node.var) < thresh: 
	 continue
      else:
	 # expand node
	 nw_image = image.crop( (node.x1, node.y1, 
	    			(node.x1+node.x2)/2, (node.y1+node.y2)/2 ) )
	 ne_image = image.crop( ((node.x1+node.x2)/2, node.y1, node.x2, (node.y1+node.y2)/2 ) )
	 se_image = image.crop( ((node.x1+node.x2)/2, (node.y1+node.y2)/2 , node.x2, node.y2 ) )
	 sw_image = image.crop( (node.x1, (node.y1+node.y2)/2 ,(node.x1+node.x2)/2, node.y2) )
	 
	 nw_image.load()
	 ne_image.load()
	 se_image.load()
	 sw_image.load()

	 node.nw_child = QuadTreeNode(nw_image, node.x1, node.y1, (node.x1+node.x2)/2, (node.y1+node.y2)/2, node)
	 node.ne_child = QuadTreeNode(ne_image, (node.x1+node.x2)/2, node.y1, node.x2, (node.y1+node.y2)/2, node)
	 node.se_child = QuadTreeNode(se_image, (node.x1+node.x2)/2, (node.y1+node.y2)/2 , node.x2, node.y2, node)
	 node.sw_child = QuadTreeNode(sw_image, node.x1, (node.y1+node.y2)/2 ,(node.x1+node.x2)/2, node.y2, node)

	 for child in [node.nw_child, node.ne_child, node.se_child, node.sw_child]:
	    q.append(child)

   return rootNode

def expand_group_w(start_node, group):
   q = deque()
   q.append(start_node)
   while len(q) > 0:
      node = q.popleft()
      if node.ne_child == None:# and node.group == None:
	 diff = [0.,0.,0.]
	 for i in range(3): diff[i] = node.mean[i] - group.mean[i]
	 if magnitude_3d_euclid(diff) < GROUP_THRESH:
	    group.add_node(node)
	    group.refresh_stats()
      else:
	 for child in [node.nw_child, node.sw_child]:
	    q.append(child)
      
def expand_group_e(start_node, group):
   q = deque()
   q.append(start_node)
   while len(q) > 0:
      node = q.popleft()
      if node.ne_child == None: # and node.group == None:
	 diff = [0.,0.,0.]
	 for i in range(3): diff[i] = node.mean[i] - group.mean[i]
	 if magnitude_3d_euclid(diff) < GROUP_THRESH:
	    group.add_node(node)
	    group.refresh_stats()
      else:
	 for child in [node.ne_child, node.se_child]:
	    q.append(child)
def expand_group_n(start_node, group):
   q = deque()
   q.append(start_node)
   while len(q) > 0:
      node = q.popleft()
      if node.ne_child == None:# and node.group == None: 
	 diff = [0.,0.,0.]
	 for i in range(3): diff[i] = node.mean[i] - group.mean[i]
	 if magnitude_3d_euclid(diff) < GROUP_THRESH:
	    group.add_node(node)
	    group.refresh_stats()
      else:
	 for child in [node.nw_child, node.ne_child]:
	    q.append(child)
def expand_group_s(start_node, group):
   #import pdb; pdb.set_trace()
   q = deque()
   q.append(start_node)
   while len(q) > 0:
      node = q.popleft()
      if node.ne_child == None:# and node.group == None:
	 diff = [0.,0.,0.]
	 for i in range(3): diff[i] = node.mean[i] - group.mean[i]
	 if magnitude_3d_euclid(diff) < GROUP_THRESH:
	    group.add_node(node)
	    group.refresh_stats()
      else:
	 for child in [node.sw_child, node.se_child]:
	    q.append(child)

'''Output a list of node groups'''
def generate_leaf_groups(root):
   groups = []
   q = deque()
   q.append(root)

   # BF Traversal
   while len(q) > 0:
      node = q.popleft()
      if node.ne_child == None:
	 if node.parent == None:
	    pass
	 else:
	    if node.group == None:
	       group = NodeGroup()
	       group.add_node(node)
	       group.refresh_stats()
	       node.group = group
	       groups.append(group)
	    parent = node.parent
	    group = node.group

	    if node == node.parent.ne_child:
	       expand_group_e(parent.nw_child, group)
	       expand_group_n(parent.se_child, group)
	    elif node == node.parent.nw_child:
	       expand_group_w(parent.ne_child, group)
	       expand_group_n(parent.sw_child, group)
	    elif node == node.parent.sw_child:
	       expand_group_s(parent.nw_child, group)
	       expand_group_w(parent.se_child, group)
	    elif node == node.parent.se_child:
	       expand_group_e(parent.sw_child, group)
	       expand_group_s(parent.ne_child, group)
	       pass
	    else:
	       raise Exception("Could not find node in it's parents' children.")
	    
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


if __name__ == '__main__':
    DEFAULT_THRESH = 1200
    DEFAULT_MINSIZE = 20
    
    def print_usage():
        print '''usage:
python ColorZoner.py <in_filename> <out_filename> [<color_threshold> [<min_region_size>]]
default color_threshold: %s
default min_region_size: %s
NOTE: file will be saved in PNG format (hint hint.. use PNG extension)''' % (DEFAULT_THRESH, DEFAULT_MINSIZE)
    
    #get arguments
    try:
        in_filename = sys.argv[1]
        out_filename = sys.argv[2]
        
        if len(sys.argv)>3:  thresh = int(sys.argv[3])
        else: thresh = DEFAULT_THRESH
         
        if len(sys.argv)>4: min_size = int(sys.argv[4])
        else: min_size = DEFAULT_MINSIZE
    except:
        print 'Error processing command line arguments!'
        print_usage()
        exit()
    
        
    img = Image.open(in_filename)
    print 'Generating quad tree on %s' % in_filename
    root = generate_quad_tree(img, thresh, min_size)
    print 'Drawing leaves...'
    out_img = draw_quadtree_leaf_colors(root, img.size)
    print 'Saving tree.png...'
    print 'Making leaf groups...'
    groups = generate_leaf_groups(root)
    print 'Drawing groups...'
    out_img = draw_group_colors(groups, img.size)
    print 'Saving image...'
    out_img.save(out_filename,'PNG')  
    print 'Saved to %s' % out_filename





   

