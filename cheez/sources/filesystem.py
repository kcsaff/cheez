import sys

from cheez.types import ImageInfo, Namespace
from cheez.fs import read_file


def from_filesystem(args: Namespace)-> ImageInfo:
    filename = args.filename.strip()
    image_bytes = read_file(filename, 'rb')
    return ImageInfo(filename=filename, bytes=image_bytes)
