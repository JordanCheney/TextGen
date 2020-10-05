import subprocess
import tempfile
import cv2
import numpy as np
from PIL import Image

pov_no_light = '''
#include "colors.inc"

camera {
    location <0.5, 0.5, -5.7>
    look_at <0.5, 0.5, 0>
}
light_source {
    <0.5, 0.5, -10>,
    color rgb<1, 1, 1>
}
cylinder {
    <0, 0, 0>, <1, 0, 0>, 5
    pigment {
        image_map {
            png "%s"
            map_type 0
        }
    }
}
'''

pov_light = '''
#include "colors.inc"

camera {
    location <0.5, 0.5, -5.7>
    look_at <0.5, 0.5, 0>
}
light_source {
    <%f, %f, -10>,
    color rgb<1, 1, 1>
}
cylinder {
    <0, 0, 0>, <1, 0, 0>, 5
    pigment {
        image_map {
            png "%s"
            map_type 0
        }
    }
    finish {
        ambient %f
        diffuse %f
        phong %f
        phong_size %d
    }
}
'''

def add_lighting(image):
    if subprocess.call(["povray", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
        raise ValueError("Could not find the povray program on your path. Install povray and try again")

    w, h = image.size
    size = max(w, h)
    square = Image.new('RGB', (size, size), (0, 0, 0))
    square.paste(image, ((size - w) // 2, (size - h) // 2))
    imgfile = tempfile.NamedTemporaryFile(suffix='.png', mode='w+')
    square.save(imgfile.name)

    with tempfile.NamedTemporaryFile(suffix='.pov', mode='w+') as povfile:
        povfile.write(pov_no_light % (imgfile.name))
        povfile.flush()

        subprocess.call(['povray', '-V', '+I' + povfile.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        povimg = cv2.imread(povfile.name[:-4] + '.png', cv2.IMREAD_COLOR)
        gray_povimg = cv2.cvtColor(povimg, cv2.COLOR_BGR2GRAY)
        _, mask_povimg = cv2.threshold(gray_povimg, 10, 255, cv2.THRESH_BINARY)

        bounds = np.nonzero(mask_povimg)
        top = bounds[0].min()
        bottom = bounds[0].max()

    with tempfile.NamedTemporaryFile(suffix='.pov', mode='w+') as povfile:
        povfile.write(pov_light % (
            0.6 * np.random.random() + 0.2, # light x-location
            0.6 * np.random.random() + 0.2, # light y-location
            imgfile.name, # imgfile
            0.2 * np.random.random() + 0.7, # ambient
            0.2 * np.random.random() + 0.7, # diffuse
            0.4 * np.random.random() + 0.5, # phong
            np.random.randint(75, high=200) # phong_size
        ))
        povfile.flush()

        subprocess.call(['povray', '-V', '+I' + povfile.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    povimg = cv2.imread(povfile.name[:-4] + '.png', cv2.IMREAD_COLOR)

    return cv2.cvtColor(povimg[top:bottom, :, :], cv2.COLOR_BGR2RGB)
