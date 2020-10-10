import random as rnd
import numpy as np
import cv2

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

from textgen.font_picker import DefaultFontPicker
from textgen.color_picker import DefaultColorPicker

class TextGeneratorOptions(object):
    def __init__(
        self,
        font_picker=DefaultFontPicker(),
        color_picker=DefaultColorPicker(),
    ):
        self.font_picker = font_picker
        self.color_picker = color_picker

def generate_text(opts, index, text, bg_color, max_height):
    font = opts.font_picker.get_font(index)
    font_size = 5
    text_width, text_height = 0, 0

    # Generate a large image to compute the text bounds
    with Image(width=max_height*4, height=max_height) as canvas:
        with Drawing() as context:
            context.font = font

            # Arbitrary range of font sizes, from a reasonable min (size 5) to max (size 100)
            # The goal is to determine the font size closest to the maximum height
            # TODO: This can be a binary search for speed
            print('Finding optimal text size...')
            for i in range(5, 100):
                context.font_size = i
                metrics = context.get_font_metrics(canvas, text)
                if metrics.text_height < max_height:
                    font_size = i
                    text_width = int(metrics.text_width)
                    text_height = int(metrics.text_height)
                else:
                    break

    # Generate the text image
    with Image(width=text_width, height=text_height, background=Color('rgba(0, 0, 0, 0)')) as canvas:
        with Drawing() as context:
            context.font = font
            context.font_size = font_size
            color = opts.color_picker.get_color(bg_color)
            context.fill_color = Color(f'rgba({color[0]}, {color[1]}, {color[2]}, 255)')
            context.text(x=0, y=text_height, body=text)
            context.text_antialias = True
            context(canvas)

            image = np.array(canvas)

    with Image(width=text_width, height=text_height, background=Color('black')) as canvas:
        with Drawing() as context:
            context.font = font
            context.font_size = font_size
            context.fill_color = Color('white')
            context.text(x=0, y=text_height, body=text)
            context.text_antialias = True
            context(canvas)

            mask = np.array(canvas)[:, :, 0]

    return image, mask
