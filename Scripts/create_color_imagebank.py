# Include the following line at the beginning of any script in this directory
from scripts_init import proj_dir

import os
from os import path
from ColorZoner.ImageBank import ImageBank


def main():
    img_dir = path.join(proj_dir, 'Images', 'colors')
    img_bank_dir = path.join(proj_dir, 'Test', 'color_bank')
    imagebank = ImageBank.new(img_bank_dir)

    # add all images from img_dir to image bank
    files = os.listdir(img_dir)
    for f in files:
        f_path = os.path.join(img_dir, f)
        imagebank.add_image_file(f_path)
        print "Added %s" % f

    imagebank.save()
    print "Image bank saved."


if __name__ == '__main__':
    main()
