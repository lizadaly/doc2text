import os
import argparse

from doc2text import Document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--language', default='deu')
    parser.add_argument('-i', '--infile', required=True)
    parser.add_argument('-o', '--outfile', required=True)

    args = parser.parse_args()

    # Initialize the class.
    doc = Document(lang=args.language)

    # Read the file in. Currently accepts pdf, png, jpg, bmp, tiff.
    # If reading a PDF, doc2text will split the PDF into its component pages.
    doc.read(os.path.abspath(args.infile))
    with open(os.path.abspath(args.outfile), 'w') as outfile:
        outfile.write(doc.text)


if __name__ == '__main__':
    main()
