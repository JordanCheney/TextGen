import os
import random
import functools

from textgen.text_generator import generate_text
from textgen.image_background import ImageBackgroundOptions, generate_image_background
from textgen.white_background import WhiteBackgroundOptions, generate_white_background

class SampleIterator:
    def __init__(
        self,
        source,
        gen_opts,
        background_opts,
        count
   ):
        self.source = source
        self.gen_opts = gen_opts
        self.background_opts = background_opts
        self.count = count

        if type(self.background_opts) is ImageBackgroundOptions:
            self.background_f = functools.partial(generate_image_background, self.background_opts)
        elif type(self.background_opts) is WhiteBackgroundOptions:
            self.background_f = functools.partial(generate_white_background, self.background_opts)
        else:
            raise ValueError("Unknown background options")

        self.generated_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.generated_count == self.count:
            raise StopIteration
        self.generated_count += 1

        text = self.source.next()
        text_f = functools.partial(generate_text, self.gen_opts, self.generated_count, text)

        image, mask = self.background_f(self.generated_count, text_f)
        if image is None or mask is None:
            print('Error! Skipping sample!')
            return self.next() # Go to the next sample

        return image, mask, text
