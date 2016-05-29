import imghdr
import requests
from urllib.parse import urlparse

from cheez.types import ImageInfo

class Masseuse(object):
    def massage(self, image: ImageInfo)-> ImageInfo:
        for filter in (self.load, self.fetch, self.name):
            image = filter(image)
        return image

    def fetch(self, image):
        if image.url and not image.bytes:
            data = requests.get(image.url).content
            image = image._replace(bytes=data)
        if image.url and not image.filename:
            filename = urlparse(image.url).path.split('/')[-1]
            image = image._replace(filename=filename)
        return image

    def load(self, image):
        if image.filename and not image.bytes:
            data = open(image.filename, 'rb').read()
            image = image._replace(bytes=data)
        return image

    def name(self, image):
        if image.bytes and not image.filename:
            ext = imghdr.what(None, h=image.bytes)
            if ext:
                image = image._replace(filename='image.{}'.format(ext))
        if image.filename and not image.title:
            image = image._replace(title=image.filename)
        if image.title and not image.description:
            image = image._replace(description=image.title)
        return image
