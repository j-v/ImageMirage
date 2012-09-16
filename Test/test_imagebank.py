import unittest
import Image
import os
from os import path

from ColorZoner.ImageBank import ImageBank


class TestColorZoner(unittest.TestCase):
    def setUp(self):
        self.image_dir = 'test'
        self.bank_path = path.join('test', 'test_bank')
        self.csv_path = path.join(
            self.bank_path, ImageBank.IMAGEBANK_CSV_FILENAME)

    def tearDown(self):
        pass

    def test_create(self):

        if path.exists(self.csv_path):
            os.remove(self.csv_path)
            # remove all other files in folder too
            for filename in os.listdir(self.bank_path):
                os.remove(path.join(
                    self.bank_path, filename))  # DELETES A FILE PERMANENTLY

        # Create new empty image bank
        imagebank = ImageBank.new(self.bank_path)

        # The csv file should exist
        self.assertTrue(path.exists(self.csv_path))

        # Creating a new bank in the same location should raise an exception
        self.assertRaises(Exception, ImageBank.new, self.bank_path)

        # Test adding an image
        image_path = path.join(self.image_dir, 'kirk.jpg')
        imagebank.add_image_file(image_path)
        self.assertTrue(len(imagebank.entries) == 1)
        e = imagebank.entries[0]
        print e
        # Adding it again should raise an exception
        self.assertRaises(Exception, imagebank.add_image_file, image_path)

        # Add a duplicate of the image using a different filename
        image = Image.open(image_path)
        imagebank.add_image(image, 'kirk_duplicate.png')
        self.assertTrue(len(imagebank.entries) == 2)
        # self.assertTrue( str(imagebank.entries[0])==str(imagebank.entries[1]))
        print imagebank.entries[1]

        imagebank.save()

    def test_load_and_destroy(self):
        imagebank = ImageBank.open(self.bank_path)

        self.assertTrue(len(imagebank.entries) == 2)

        for e in imagebank.entries:
            print e

        # Test removing the images
        imagebank.remove_image('kirk.jpg')
        imagebank.remove_image('kirk_duplicate.png')
        self.assertTrue(len(imagebank.entries) == 0)

        # Delete the bank
        # TODO maybe there should be delete in the ImageBank API
        os.remove(self.csv_path)
