import os

class DefaultFontPicker(object):
    def __init__(self, fonts=[]):
        """
        A font picker that selects from a font list. Selection is iterative.
        If the font list is empty a default list is loaded and used
        """
        self.fonts = fonts
        if len(self.fonts) == 0:
            self.fonts = [
                os.path.join(os.path.dirname(__file__), "fonts", font)
                for font in os.listdir(
                    os.path.join(os.path.dirname(__file__), "fonts")
                )
            ]

    def get_font(self, index):
        return self.fonts[index % len(self.fonts)]
