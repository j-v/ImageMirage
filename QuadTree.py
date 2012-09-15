import Image, ImageStat
import sys

class QuadTreeNode:

   def __init__(self, image, x1, y1, x2, y2, parent=None): # all should be ints
      # TODO check for valid input
      self.x1 = x1
      self.y1 = y1
      self.x2 = x2
      self.y2 = y2

      self.parent = parent

      self.ne_child = None
      self.nw_child = None
      self.se_child = None
      self.sw_child = None

      nodestats = ImageStat.Stat(image)
      self.mean = nodestats.mean
      self.var = nodestats.var

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

   def get_bounding_box(self):
      # Get bounding box
      x2, y2 = (0,0)
      x1, y1 = (sys.maxint, sys.maxint)

      for node in self.nodes:
	 if node.x1 < x1: x1 = node.x1
	 if node.y1 < y1: y1 = node.y1
	 if node.x2 > x2: x2 = node.x2
	 if node.y2 > y2: y2 = node.y2

      return (x1,y1,x2,y2)
      
   def get_mask(self):
      '''Create a mask image. Image will be as large as the blob's bounding box,
      with each corresponding pixel either 0 or 255'''
      x1, y1, x2, y2 = self.get_bounding_box()

      # Initialize mask image
      width = x2-x1+1
      height = y2-y1+1
      mask = Image.new('1', (width,height))

      # Set pixels corresponding to nodes in group to 255
      for node in self.nodes:
	 node_width = node.x2 - node.x1
	 node_height = node.y2 - node.y1
	 for x in xrange(node_width):
	    for y in xrange(node_height):
	       mask.putpixel( (x+node.x1-x1, y+node.y1-y1), 255)

      return mask

