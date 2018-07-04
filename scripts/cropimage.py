import os
import argparse

from doc2text import Document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--language', default='eng')
    parser.add_argument('-i', '--infile', required=True)
    parser.add_argument('-d', '--outdir', required=True)
    args = parser.parse_args()

    doc = Document.get_by_path(args.infile)


    print("Starting processing {}".format(os.path.basename(args.infile)))


    doc.crop_image(os.path.join(args.outdir, os.path.basename(args.infile)))


if __name__ == '__main__':
    main()
