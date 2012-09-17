import os
from os import path
from scripts_init import proj_dir
from ColorZoner.ImageBank import ImageBank


def main():
    img_dir = path.join(proj_dir, 'Images', 'colors')
    img_bank_dir = path.join(proj_dir, 'ImageBanks', 'colors')
    imagebank = ImageBank.new(img_bank_dir)

    # add all images from img_dir to image bank
    files = os.listdir(img_dir)
    for f in files:
        f_path = os.path.join(img_dir, f)
        print f_path
        imagebank.add_image_file(f_path)

    # print out entries
    for e in imagebank.entries:
        print e

    imagebank.save()


if __name__ == '__main__':

    main()
