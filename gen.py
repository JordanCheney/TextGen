from textgen import SampleIterator, TextGeneratorOptions, ImageBackgroundOptions, WhiteBackgroundOptions
from textgen.sources import FileSource

import cv2
import numpy as np

it = SampleIterator(
    FileSource('nnumbers.txt', shuffle=True),
    TextGeneratorOptions(
        blur=1
    ),
    ImageBackgroundOptions(
        image_dir='images/',
        image_file='images/image_list.csv'
    ),
    #WhiteBackgroundOptions(),
    count=-1
)

for (image, mask, text) in it:
    rgb_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
    cv2.imshow('image', rgb_image)
    cv2.imshow('mask', np.asarray(mask))
    print('label:', text)

    cv2.waitKey()
