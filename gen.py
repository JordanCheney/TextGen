from textgen import SampleIterator, TextGeneratorOptions, ImageBackgroundOptions, WhiteBackgroundOptions
from textgen.sources import FileSource

from lightgen.light_generator import add_lighting

import cv2
import numpy as np
import tempfile

it = SampleIterator(
    FileSource('nnumbers.txt', shuffle=True),
    TextGeneratorOptions(),
    ImageBackgroundOptions(
        image_dir='images/',
        image_file='images/image_list.csv'
    ),
    #WhiteBackgroundOptions(),
    count=-1
)

index = 0
for (image, mask, text) in it:
    bgr_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
    lit_image = add_lighting(image)

    cv2.imshow('image', bgr_image)
    cv2.imshow('mask', mask)
    cv2.imshow('lit', cv2.cvtColor(lit_image, cv2.COLOR_BGR2RGB))
    cv2.waitKey()
    cv2.imwrite(f'samples/{text}_{index}.png', bgr_image)
    cv2.imwrite(f'samples/{text}_{index}_lit.png', cv2.cvtColor(lit_image, cv2.COLOR_BGR2RGB))

    index += 1
    if index == 200:
        break
