from argparse import Namespace
from collections import namedtuple

ImageInfo = namedtuple('ImageInfo', ('bytes', 'title', 'description', 'url', 'filename', 'format'))
ImageInfo.__new__.__defaults__ = (None,) * len(ImageInfo._fields)
