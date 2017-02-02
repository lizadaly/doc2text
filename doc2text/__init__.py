# coding=utf-8

import os
import mimetypes

import cv2
import PyPDF2 as pyPdf
from wand.image import Image

from .page import Page


acceptable_mime = ["image/bmp", "image/png", "image/tiff", "image/jpeg",
                   "image/jpg", "video/JPEG", "video/jpeg2000"]


FileNotAcceptedException = Exception(
    'The filetype is not acceptable. We accept bmp, png, tiff, jpg, jpeg, jpeg2000, and PDF.'
)


class Document(object):
    CONVERSION_RESOLUTION = 300
    COMPRESSION_QUALITY = 99

    @property
    def text(self):
        if not self.processed:
            self._process()

        return '\f'.join([(p.extract_text() or ' ') for p in self.processed_pages])

    def __init__(self, lang=None):
        self.lang = lang
        self.pages = []
        self.processed_pages = []
        self.page_content = []
        self.prepared = False
        self.processed = False
        self.error = None
        self.path = None

    def _convert(self, source, destination):
        with Image(filename=source, resolution=self.CONVERSION_RESOLUTION) as image:
            image.compression_quality = self.COMPRESSION_QUALITY
            image.save(filename=destination)

    def _process(self):
        def process_page(p):
            p.crop()
            p.deskew()
            return p

        self.processed_pages = [process_page(p) for p in self.pages]
        self.processed = True

    def read(self, path):
        self.filename = os.path.basename(path)
        self.file_basename, self.file_extension = os.path.splitext(self.filename)
        self.path = path
        self.mime_type = mimetypes.guess_type(path)
        self.file_basepath = os.path.dirname(path)

        # If the file is a pdf, split the pdf and prep the pages.
        if self.mime_type[0] == "application/pdf":
            file_temp = open(self.path, 'rb')
            pdf_reader = pyPdf.PdfFileReader(file_temp)
            self.num_pages = pdf_reader.numPages
            try:
                for i in range(self.num_pages):
                    output = pyPdf.PdfFileWriter()
                    output.addPage(pdf_reader.getPage(i))
                    path = 'temp.pdf'
                    im_path = 'temp.png'
                    with open(path, 'wb') as f:
                        output.write(f)
                    self._convert(path, im_path)
                    orig_im = cv2.imread(im_path, 0)
                    page = Page(orig_im, i, self.lang)
                    self.pages.append(page)
                    os.remove(path)
                    os.remove(im_path)
                self.prepared = True
            except Exception as e:
                self.error = e
                raise

        # If the file is an image, think of it as a 1-page pdf.
        elif self.mime_type[0] in acceptable_mime:
            self.num_pages = 1
            temp_path = os.path.normpath(os.path.join(
                self.file_basepath, self.file_basename + '_temp.png'
            ))
            self._convert(path, temp_path)
            orig_im = cv2.imread(temp_path, 0)
            os.remove(temp_path)
            page = Page(orig_im, 0)
            self.pages.append(page)

        # Otherwise, out of luck.
        else:
            print(self.mime_type[0])
            raise FileNotAcceptedException

    def process(self):
        if not self.processed:
            self._process()
