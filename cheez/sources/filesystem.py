import sys

from cheez.types import ImageInfo, Namespace


def from_filesystem(args: Namespace)-> ImageInfo:
    filename = args.filename
    filename = filename.strip()
    if filename == '-':
        image_bytes = sys.stdin.read()
    else:
        with open(filename, 'rb') as f:
            image_bytes = f.read()
    return ImageInfo(filename=filename, bytes=image_bytes)
