import scripts_init
import argparse
from ColorZoner.Painter.Painter import Painter

def do_paint(src_file, dest_file, imagebank, split_thresh, minsize, group_thresh):
    painter = Painter(src_file,
                      imagebank,
                      split_thresh,
                      minsize,
                      group_thresh)

    painter.generate_groups()
    painter.get_pictures_for_groups()
    painter.paint()

    painter.dest_image.save(dest_file, 'PNG')

def main():
    DEFAULT_SPLIT_THRESH = 1200
    DEFAULT_MINSIZE = 20
    DEFATUL_GROUP_THRESH = 75

    parser = argparse.ArgumentParser(
        description='ColorZoner for your pleasure')
    parser.add_argument('in_file', metavar='IN_FILE', type=str,
                        help='The input image file')
    parser.add_argument('out_file', metavar='OUT_FILE', type=str,
                        help='The output image file, should have .png extension')
    parser.add_argument('-s', '--splitthresh', type=int,
                        default=DEFAULT_SPLIT_THRESH,
                        help="Threshold for splitting up the image into regions")
    parser.add_argument('-m', '--minsize', type=int, default=DEFAULT_MINSIZE,
                        help='Minimum dimension of squares to break the image down into')
    parser.add_argument(
        '-g', '--groupthresh', type=int, default=DEFATUL_GROUP_THRESH,
        help='Threshold for joining groups together')
    parser.add_argument('img_bank', metavar="IMG_BANK", type=str,
                        help='Path to image bank folder')

    args = parser.parse_args()

    do_paint(args.in_file, args.out_file, args.img_bank, args.splitthresh,
             args.minsize, args.groupthresh)

if __name__ == '__main__':
    main()
