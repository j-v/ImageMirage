# TODO make better exceptions

import ImageStat, Image
import os
import shutil
from ImageBankEntry import ImageBankEntry

open_file = open

IMAGEBANK_CSV_FILENAME = 'imagebank.csv'
IMAGEBANK_CSV_HEADER = 'filename,width,height,meanr,meang,meanb,varr,varg,varb'
IMAGEBANK_IMAGE_FORMAT = 'PNG'


class ImageBank:
    def __init__(self, directory):
        '''Should not be called directly from outside the module'''
        self.directory = directory
        self.entries = []

    def remove_image(self, filename):
        '''remove_image(str) -> None

        Removes image with given filename from bank and DELETES FROM DISK'''
        for index,entry in enumerate(self.entries):
            if entry.filename == filename:
                self.entries.pop(index)
                # delete file
                img_path = os.path.join(self.directory, filename)
                if not os.path.exists(img_path):
                    raise Exception("Image %s was found in library but no image file was found")
                os.remove(img_path)
                return

        raise Exception("Image %s was not found in library" % filename)

    def add_image(self, image, filename, stats=None):
        '''add_image(Image, str, str, ImageStat) -> None

        Takes a PIL image object, saves it to file and adds it to the bank'''

        # get stats
        if stats == None:
            stats = ImageStat.Stat(image)
        # save image to bank directory
        filepath = os.path.join(self.directory, filename)
        if os.path.exists(filepath):
            raise Exception("File %s already is present in image bank directory. Not adding." % filename)
        image.save(filepath, IMAGEBANK_IMAGE_FORMAT)

        width, height = image.size
        entry = ImageBankEntry(filename,width,height,stats.mean,stats.var)
        self.entries.append(entry)

    def add_image_file(self, file_path):
        '''add_image_file(str) -> None
        
        Takes the path to an image file, copies the image to the bank
        directory, and adds it to the bank.'''

        # check file exists
        if not os.path.isfile(file_path):
            raise Exception("File %s doesn't exist, not adding to image bank" % file_path)
        # check file doesn't already exist in image bank directory
        filename = os.path.basename(file_path)
        dest_path = os.path.join(self.directory, filename)
        if os.path.exists(dest_path):
            raise Exception("File %s already is present in image bank directory. Not adding." % filename)

        # read image
        image = Image.open(file_path)
        stats = ImageStat.Stat(image)
        width, height = image.size

        # copy file
        shutil.copyfile(file_path, dest_path)

        # add to entries
        entry = ImageBankEntry(filename, width, height, stats.mean, stats.var)
        self.entries.append(entry)

    def save(self):
        '''Update the image_bank.csv file'''
        try:
            # open file
            csv_path = os.path.join(self.directory, IMAGEBANK_CSV_FILENAME)
            print csv_path
            f = open_file(csv_path, 'w')
            # write header
            f.write(IMAGEBANK_CSV_HEADER + os.linesep)
            # write data'
            f.writelines( entry.to_csv() + os.linesep for entry in self.entries)
        except IOError:
            print 'Error opening file or writing data'
        else:
            print 'Image bank saved'
            f.close()

    def load(self):
        '''Read the image_bank.csv file'''
        try:
            f = open_file(os.path.join(self.directory, IMAGEBANK_CSV_FILENAME), 'r')
            # check header
            header = f.readline()
            if header.strip() != IMAGEBANK_CSV_HEADER:
                raise Exception("Incorrect header found in image bank file")
            # read data
            for line in f.readlines():
                entry = ImageBankEntry.parse(line)

                # check for existence of file
                if not os.path.isfile(os.path.join(self.directory, entry.filename)):
                    print 'WARNING: Image %s not found, omitting from image bank' % filename
                else:
                    self.entries.append(entry)

        except IOError:
            print 'Error opening file or reading data'
        else:
            print 'Loaded image bank'
            f.close()

def new(directory):
    '''Create a new image bank at the provided directory. The directory must 
    already exist and should be empty.'''
    if not os.path.exists(directory):
        raise Exception("Directory does not exist")
    if not os.path.isdir(directory):
        raise Exception("Path given is not a directory")
    if os.path.isfile(os.path.join(directory,IMAGEBANK_CSV_FILENAME)):
        raise Exception("Image bank at %s already exists" % directory)

    imagebank = ImageBank(directory)
    imagebank.save()

    return imagebank

def open(directory):
    '''Open an image bank at the specified directory. There must be a csv data file
    at the directory.'''
    if not os.path.exists(directory):
        raise Exception("Directory does not exist")
    if not os.path.isdir(directory):
        raise Exception("Path given is not a directory")
    csv_path = os.path.join(directory, IMAGEBANK_CSV_FILENAME)
    if not os.path.isfile(csv_path):
        raise Exception("Image bank CSV data file not found in directory %s" % directory)

    imagebank = ImageBank(directory)
    imagebank.load()

    return imagebank
