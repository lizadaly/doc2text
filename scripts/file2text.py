import os
import argparse

from doc2text import Document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--language', default=None)
    parser.add_argument('-f', '--file', required=True)

    args = parser.parse_args()

    # Initialize the class.
    doc = Document(lang=args.language)

    # Read the file in. Currently accepts pdf, png, jpg, bmp, tiff.
    # If reading a PDF, doc2text will split the PDF into its component pages.
    doc.read(os.path.abspath(args.file))

    # Crop the pages down to estimated text regions, deskew, and optimize for OCR.
    doc.process()

    # Extract text from the pages.
    doc.extract_text()
    print(doc.get_text())


if __name__ == '__main__':
    main()
