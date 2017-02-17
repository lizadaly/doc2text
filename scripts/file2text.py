import os
import argparse

from doc2text import Document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--language', default='deu')
    parser.add_argument('-i', '--infile', required=True)
    parser.add_argument('-o', '--outfile', required=True)

    args = parser.parse_args()

    doc = Document.get_by_path(args.infile)
    with open(os.path.abspath(args.outfile), 'w') as outfile:
        outfile.write(doc.get_text(args.language))


if __name__ == '__main__':
    main()
