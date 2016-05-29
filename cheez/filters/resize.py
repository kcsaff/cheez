from cheez.types import ImageInfo, Namespace
from PIL import Image
import io


def thru_resize(image: ImageInfo, args: Namespace)-> ImageInfo:
    pimage = Image.open(io.BytesIO(image.bytes))
    size = (args.width, args.height)
    pimage.thumbnail(size)
    with io.BytesIO() as stream:
        pimage.save(stream, format=image.format.upper())
        image = image._replace(bytes=stream.getvalue())
    return image
