class ImageBankEntry:
   def __init__(self, filename, width, height, mean, var):
      '''Should not be called directly from outside this module'''
      self.filename = filename
      self.width = width
      self.height = height
      self.mean = mean
      self.var = var

   def to_csv(self):
	return ','.join([ self.filename,
	                  str(self.width),
	                  str(self.height),
	                  str(self.mean[0]),
	                  str(self.mean[1]),
	                  str(self.mean[2]),
	                  str(self.var[0]),
	                  str(self.var[1]),
	                  str(self.var[2])
			  ])
   @classmethod 
   def parse(cls, parsestr ):
      vals = parsestr.strip().split(',')
      filename = vals[0]
      height = int(vals[1])
      width = int(vals[2])
      mean = [float(m) for m in vals[3:6]]
      var = [float(v) for v in vals[6:9]]
      
      return cls(filename,width,height,mean,var)
      

   def __str__(self):
      return 'ImageBankEntry data: ' + self.to_csv()

