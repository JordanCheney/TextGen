import os
import random

class FileSource(object):
    def __init__(
        self,
        filename,
        shuffle=False
    ):
        self.filename = filename
        with open(self.filename) as f:
            self.strings = f.read().split()

        if shuffle:
            random.shuffle(self.strings)

        self.generated_count = 0

    def next(self):
        self.generated_count += 1
        if self.generated_count == len(self.strings):
            self.generated_count = 0

        return self.strings[self.generated_count]
