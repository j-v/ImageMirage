# Include the following line at the beginning of any script in this directory
from scripts_init import proj_dir

import argparse
import os
from os import path
from ColorZoner.ImageBank import ImageBank

# Creates an image bank given a folder of pictures
# Pictures are copied to ImageBanks directory
# It assumes the input folder only contains image files

def main():
    parser = argparse.ArgumentParser(
        description='Image bank creator')
    parser.add_argument('input_image_folder', type=str, 
        help='Folder containing images to insert into new library')
    parser.add_argument('library_name', type=str,
        help='Name of the new image library to create')

    args = parser.parse_args()

    img_dir = path.join(proj_dir, 'Images', args.input_image_folder)
    if not path.isdir(img_dir):
        # error
        print "error:", img_dir, "is not a directory"
        return 1

    img_bank_dir = path.join(proj_dir, 'ImageBanks', args.library_name)
    print img_bank_dir
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
