from cheez.types import ImageInfo, Namespace
from PIL import Image
import io


def to_display(image: ImageInfo, args: Namespace):
    print(len(image.bytes))
    print(image.title)
    prepared_image = Image.open(io.BytesIO(image.bytes))
    prepared_image.show(title=image.title)
