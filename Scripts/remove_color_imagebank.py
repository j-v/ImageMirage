# Include the following line at the beginning of any script in this directory
from scripts_init import proj_dir

from ColorZoner.ImageBank import ImageBank
import os
from os import path


def main():
    img_bank_dir = path.join(proj_dir, 'Test', 'color_bank')

    imagebank = ImageBank.open(img_bank_dir)

    # remove all image files
    for entry in imagebank.entries:
        img_path = path.join(img_bank_dir, entry.filename)
        os.remove(img_path)
        print 'Deleted %s' % entry.filename

    # remove csv file
    os.remove(path.join(img_bank_dir, ImageBank.IMAGEBANK_CSV_FILENAME))
    print 'Deleted CSV file'


if __name__ == '__main__':
    main()
