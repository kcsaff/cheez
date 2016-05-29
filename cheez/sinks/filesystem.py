import imghdr
import sys

from cheez.types import ImageInfo, Namespace

def to_filesystem(image: ImageInfo, args: Namespace):
    filename = (args.filename or 'out').strip()
    if filename == '-':
        sys.stdout.write(image.bytes)
    else:
        if '.' not in filename:
            header = imghdr.what(None, h=image.bytes)
            filename = '{}.{}'.format(filename, header)

        with open(filename, 'wb') as f:
            f.write(image.bytes)
    return filename
