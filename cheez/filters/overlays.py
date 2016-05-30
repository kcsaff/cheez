from cheez.types import ImageInfo, Namespace
from cheez.fs import read_file
from PIL import Image, ImageDraw, ImageFont
import io
import random
import glob
import os.path
import os


MIN_FONT_SIZE = 5


def _interpret_value(value, scale):
    if isinstance(value, str):
        value = value.strip()
        if value.endswith('%'):
            value = scale * 0.01 * float(value.strip('%').strip())
    return int(float(value))


def _process_font_name(font_name):
    if not font_name:
        pass
    elif '*' in font_name:  # Interpret as a glob
        font_name = random.choice(glob.glob(font_name))
    elif os.path.isdir(font_name):  # Choose random font from directory
        font_name = random.choice(
            [x for x in (os.path.join(font_name, x) for x in os.listdir(font_name))
             if os.path.isfile(x)]
        )
    return font_name


def _size_font(draw, text, font_name, margin=0, padding=0, font_size=12):
    allowed_width = draw.image.size[0] - 2 * (margin + padding)
    allowed_height = draw.image.size[1] - 2 * (margin + padding)
    if font_name:
        font = ImageFont.truetype(font_name, font_size)
    else:
        font = ImageFont.load_default()
        font_size = 0

    text_size = draw.textsize(text, font)
    while font_size > MIN_FONT_SIZE and \
            (text_size[0] > allowed_width or text_size[1] > allowed_height):
        font_size -= 1
        font = ImageFont.truetype(font_name, font_size)
        text_size = draw.textsize(text, font)
    return font


def _overlay_text_on_image(
        draw, text, font, margin=0, padding=0,
        fgcolor=(0, 0, 0, 255), bgcolor=(255, 255, 255, 128)
):
    text_size = draw.textsize(text, font)

    box = (
        margin, margin,
        margin + padding + text_size[0] + padding,
        margin + padding + text_size[1] + padding)
    draw.rectangle(box, fill=bgcolor)
    draw.text((margin + padding, margin + padding), text, fill=fgcolor, font=font)


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

    font_size = _interpret_value(args.font_size, scale)
    font_name = _process_font_name(args.font)

    draw = ImageDraw.Draw(pimage, 'RGBA')
    font = _size_font(draw, text, font_name, margin=margin, padding=padding, font_size=font_size)
    _overlay_text_on_image(draw, text, font, margin=margin, padding=padding)

    with io.BytesIO() as stream:
        pimage.save(stream, format=image.format.upper())
        image = image._replace(bytes=stream.getvalue())
    return image
