from PIL import Image

class WhiteBackgroundOptions(object):
    def __init__(
        self,
        margins=(5, 5, 5, 5),
        height=250
    ):
        self.margins = margins
        self.left_margin, self.top_margin, self.right_margin, self.bottom_margin = self.margins
        self.height = height


def generate_white_background(opts, index, generate_text):
    """
        Create text on a plain white background
    """

    text_image, text_mask = generate_text(opts.height)

    width = text_image.size[0] + opts.left_margin + opts.right_margin
    height = text_image.size[1] + opts.top_margin + opts.bottom_margin

    background_image = Image.new("L", (width, height), 255).convert("RGBA")
    background_mask = Image.new("RGB", background_image.size, (0, 0, 0))

    paste_pos = (opts.left_margin, opts.top_margin)
    background_image.paste(text_image, paste_pos, text_image)
    background_mask.paste(text_mask, paste_pos)

    return background_image, background_mask
