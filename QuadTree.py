import ImageStat

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

