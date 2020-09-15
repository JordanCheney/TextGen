import random as rnd
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter

from textgen.font_picker import DefaultFontPicker
from textgen.color_picker import DefaultColorPicker

class TextGeneratorOptions(object):
    def __init__(
        self,
        font_picker=DefaultFontPicker(),
        color_picker=DefaultColorPicker(),
        blur=0,
        character_spacing=0,
    ):
        self.font_picker = font_picker
        self.color_picker = color_picker

        if type(blur) is tuple:
            self.blur = ImageFilter.GaussianBlur(radius=int(random.normalvariate(self.blur[0], self.blur[1])))
        elif blur > 0:
            self.blur = ImageFilter.GaussianBlur(radius=blur)
        else:
            self.blur = None

        self.character_spacing = character_spacing

def generate_text(opts, index, text, bg_color, max_height):
    font = opts.font_picker.get_font(index)

    # Arbitrary range of font sizes, from a reasonable min (size 5) to max (size 100)
    # The goal is to determine the font size closest to the maximum height
    # TODO: This can be a binary search for speed
    print('Finding optimal text size...')
    font_size = 5
    for i in range(5, 100):
        image_font = ImageFont.truetype(font=font, size=i)
        height = image_font.getsize(" ")[1]
        if height < max_height:
            font_size = i
        else:
            break

    image_font = ImageFont.truetype(font=font, size=font_size)

    piece_widths = [
        image_font.getsize(p)[0] for p in text
    ]

    text_width = sum(piece_widths) + (opts.character_spacing * (len(text) - 1))
    text_height = max([image_font.getsize(p)[1] for p in text])

    text_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    text_mask = Image.new("RGB", (text_width, text_height), (0, 0, 0))

    text_image_draw = ImageDraw.Draw(text_image)
    text_mask_draw = ImageDraw.Draw(text_mask, mode="RGB")
    text_mask_draw.fontmode = "1"

    print('Selecting color...')
    color = opts.color_picker.get_color(bg_color)
    if color is None:
        return None, None

    print('Drawing characters...')
    for i, p in enumerate(text):
        text_image_draw.text(
            (sum(piece_widths[0:i]) + i * opts.character_spacing, 0),
            p,
            fill=color,
            font=image_font,
        )
        text_mask_draw.text(
            (sum(piece_widths[0:i]) + i * opts.character_spacing, 0),
            p,
            fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
            font=image_font,
        )

    text_image = text_image.crop(text_image.getbbox())
    text_mask = text_mask.crop(text_image.getbbox())

    if opts.blur is not None:
        text_image = text_image.filter(opts.blur)
        text_mask = text_mask.filter(opts.blur)

    return text_image, text_mask
