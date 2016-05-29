from cheez.types import ImageInfo, Namespace
from cheez.fs import read_file
from PIL import Image, ImageDraw, ImageFont
import io


MIN_FONT_SIZE = 5


def _interpret_value(value, scale):
    if isinstance(value, str):
        value = value.strip()
        if value.endswith('%'):
            value = scale * 0.01 * float(value.strip('%').strip())
    return int(float(value))


def thru_overlay_text(image: ImageInfo, args: Namespace)-> ImageInfo:
    # Prepare text
    text = args.text or ''
    if args.file:
        text += read_file(args.file)

    # Prepare image & its values
    pimage = Image.open(io.BytesIO(image.bytes)).convert('RGB')
    scale = min(pimage.size)

    margin = _interpret_value(args.margin, scale)
    padding = _interpret_value(args.padding, scale)
    allowed_width = pimage.size[0] - 2 * (margin + padding)
    allowed_height = pimage.size[1] - 2 * (margin + padding)

    font_size = _interpret_value(args.font_size, scale)
    font_name = args.font

    if font_name:
        font = ImageFont.truetype(font_name, font_size)
    else:
        font = ImageFont.load_default()
        font_size = 0

    draw = ImageDraw.Draw(pimage, 'RGBA')

    text_size = draw.textsize(text, font)
    while font_size > MIN_FONT_SIZE and \
            (text_size[0] > allowed_width or text_size[1] > allowed_height):
        font_size -= 1
        font = ImageFont.truetype(font_name, font_size)
        text_size = draw.textsize(text, font)

    box = (
        margin, margin,
        margin + padding + text_size[0] + padding,
        margin + padding + text_size[1] + padding)
    draw.rectangle(box, fill=(255, 255, 255, 128))
    draw.text((margin + padding, margin + padding), text, fill=(0, 0, 0, 255), font=font)
    with io.BytesIO() as stream:
        pimage.save(stream, format=image.format.upper())
        image = image._replace(bytes=stream.getvalue())
    return image
