import unittest
import Image
import os
from os import path

import ImageBank

class TestColorZoner(unittest.TestCase):
   def setUp(self):
      self.image_dir = 'test'
      print 'hello'

   def tearDown(self):
      print 'gbye'
      pass

   def test_test(self):
      print 'test'

   def test_new(self):
      bank_path = path.join('test','test_bank') 

      csv_path = path.join(bank_path,ImageBank.IMAGEBANK_CSV_FILENAME)
      if path.exists(csv_path):
	 os.remove(csv_path)
	 #TODO remove other files too? i.e. images

      # Create new empty image bank
      imagebank = ImageBank.new(bank_path)


      # The csv file should exist
      self.assertTrue(path.exists(csv_path))

      # Creating a new bank in the same location should raise an exception
      self.assertRaises(Exception, ImageBank.new, bank_path)

      # Test adding an image
      image_path = path.join(self.image_dir, 'kirk.jpg')
      imagebank.add_image_file(image_path)
      self.assertTrue( len(imagebank.entries) == 1 ) 
      # Adding it again should raise an exception
      self.assertRaises(Exception, imagebank.add_image_file, image_path)

      # Test removing an image
      imagebank.remove_image('kirk.jpg')
      self.assertTrue(len(imagebank.entries)==0)



      # Delete the bank 
      # TODO maybe there should be delete in the ImageBank API
      os.remove(csv_path)



      
