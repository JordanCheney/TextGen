from PIL import ImageColor
import random

class DefaultColorPicker(object):
    def __init__(
        self,
        hue=list(range(0, 360, 5)),
        saturation=list(range(0, 100, 5)),
        lightness=list(range(0, 100, 5)),
        min_contrast=7
    ):
        self.hue = hue
        self.saturation = saturation
        self.lightness = lightness
        self.min_contrast = min_contrast

    @staticmethod
    def rgb2l(rgb):
        def convert_channel(c):
            c = c / 255
            if c < 0.03928:
                return c / 12.92

            return pow((c + 0.055) / 1.055, 2.4)

        r, g, b = [convert_channel(c) for c in rgb]

        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def get_color(self, bg_color):
        l1 = DefaultColorPicker.rgb2l(bg_color)

        random.shuffle(self.hue)
        random.shuffle(self.saturation)
        random.shuffle(self.lightness)

        best_color = None
        best_contrast = 0
        for h in self.hue:
            for s in self.saturation:
                for l in self.lightness:
                    color = ImageColor.getrgb(f'hsl({h},{s}%,{l}%)')
                    l2 = DefaultColorPicker.rgb2l(color)

                    if l1 > l2:
                        contrast = (l1 + 0.05) / (l2 + 0.05)
                    else:
                        contrast = (l2 + 0.05) / (l1 + 0.05)

                    if contrast > self.min_contrast:
                        return color

                    if contrast > best_contrast:
                        best_contrast = contrast
                        best_color = color

        print('No color above contrast threshold! Best contrast:', contrast)
        return best_color
