from PIL import Image, ImageDraw, ImageFilter
import shapely
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon
import random
import json
import os
import cv2
import numpy as np

class ImageBackgroundOptions(object):
    def __init__(
        self,
        image_dir,
        image_file,
        num_centers=20,
        skew_angles=range(-20, 20, 5)
    ):
        self.image_dir = image_dir
        self.image_file = image_file
        self.num_centers = num_centers
        self.skew_angles = skew_angles

        self.background_images = []
        with open(self.image_file) as f:
            f.readline()
            for line in f:
                cols = line.strip().split(',')
                attrs = json.loads(','.join(cols[5:-1]).replace('""', '"').strip('"'))
                img = Image.open(os.path.join(self.image_dir, cols[0]))
                pts = list(zip(map(int, attrs['all_points_x']), map(int, attrs['all_points_y'])))

                self.background_images.append((img, pts))


def project_axes(center, theta, width, height):
    x_line = LineString([Point(center.x - width, center.y), Point(center.x + width, center.y)])
    y_line = LineString([Point(center.x, center.y - height), Point(center.x, center.y + height)])

    x_line = shapely.affinity.rotate(x_line, theta, center)
    y_line = shapely.affinity.rotate(y_line, theta, center)

    return x_line, y_line

def pset_center(point_set):
    p1, p2 = point_set.coords[:2]
    return Point((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

def make_box(center, width, height, theta):
    xoff = width / 2
    yoff = height / 2
    box = Polygon([
        Point(center.x - xoff, center.y - yoff),
        Point(center.x + xoff, center.y - yoff),
        Point(center.x + xoff, center.y + yoff),
        Point(center.x - xoff, center.y + yoff)
    ])

    return shapely.affinity.rotate(box, theta, center)

def check_box(poly, box):
    for pt in box.exterior.coords:
        if not poly.contains(Point(pt)):
            return False

    return True

def generate_image_background(opts, index, generate_text):
    # This function finds the largest rectangle contained within a polygon
    # It is based on this blog post: https://d3plus.org/blog/behind-the-scenes/2014/07/08/largest-rect/

    # Generate text at a fixed size, this is defines a valid aspect ratio for the text, which we will use
    # when finding our box
    print('Generating inital text...')
    text_image, _ = generate_text((255, 255, 255), 80)
    aspect_ratio = text_image.size[1] / text_image.size[0]

    img, pts = opts.background_images[index % len(opts.background_images)]

    # Compute the average background color of the polygon
    print('Getting background color...')
    poly_mask = np.zeros((img.size[1], img.size[0]), dtype=np.uint8)
    cv2.fillConvexPoly(poly_mask, np.array(pts, np.int32), 255)
    np_poly_mask = np.where(poly_mask == 255)
    bg_color = (
        np.mean(np.asarray(img)[:, :, 0][np_poly_mask]),
        np.mean(np.asarray(img)[:, :, 1][np_poly_mask]),
        np.mean(np.asarray(img)[:, :, 2][np_poly_mask])
    )

    poly = Polygon(shell=pts)
    poly_left, poly_top, poly_right, poly_bottom = poly.bounds

    print('Computing centers...')
    centers = []
    while len(centers) < opts.num_centers:
        new_center = Point(random.randint(poly_left, poly_right), random.randint(poly_top, poly_bottom))
        if poly.contains(new_center):
            centers.append(new_center)

    background_image = img.copy()
    draw = ImageDraw.Draw(background_image)
    draw.polygon(pts, outline=(255, 0, 0))

    background_mask = Image.new("RGB", background_image.size, (0, 0, 0))

    print('Finding best fit rectangle...')
    rect_params = None
    best_rect = Polygon([])
    for theta in opts.skew_angles:
        for center in centers:
            # Step 1 is to update our center point. This is done by projecting a line in the x and y directions after rotating
            # the coordinate plane by the skew angle. The line will intersect with the polygon at 2 points. The new centers
            # will be the midpoints of the x and y lines

            # Create x and y lines from our chosen center and skew angle. The lines should run to infinity in both directions
            # but that can't be coded. Instead we run them the image width in both directions which is equivalent
            x_line, y_line = project_axes(center, theta, img.size[0], img.size[1])

            # Compute the new centers. The rational is that these are more central to the polygon and should be better
            # centroids for our rectangle
            try:
                new_centers = [pset_center(poly.intersection(x_line)), pset_center(poly.intersection(y_line))]
            except: # On occasion, annotations aren't perfectly convex and a line can pass through 3 sides of a polygon. For now we just skip that
                continue

            # Iterate over our centers and try different widths at our fixed aspect ratio
            for center in new_centers:
                x_line, y_line = project_axes(center, theta, img.size[0], img.size[1])

                try:
                    width = LineString(poly.intersection(x_line).coords).length
                except:
                    continue

                # Now iterate over rectangle projected along the x and y lines, the width will reduce by 10% until we find
                # a rectangle that fits
                for width_factor in range(100, 10, -10):
                    rect_width = int(width_factor / 100 * width)
                    rect_height = int(rect_width * aspect_ratio)

                    box = make_box(center, rect_width, rect_height, theta)
                    if check_box(poly, box) and best_rect.area < box.area:
                        rect_params = (center, rect_width, rect_height, theta)
                        best_rect = box
                        break

    # Regenerate the text image using the rect width
    print('Regenerating text...')
    center, text_width, text_height, theta = rect_params
    text_image, text_mask = generate_text(bg_color, text_height)
    if text_image is None or text_mask is None:
        return None, None

    print('Merging sample...')
    rotated_image = text_image.rotate(-1 * theta, expand=1)
    rotated_mask = text_mask.rotate(-1 * theta, expand=1)

    tl = (int(center.x - (rotated_image.size[0] / 2)), int(center.y - (rotated_image.size[1] / 2)))

    background_image.paste(rotated_image, tl, rotated_image)
    background_mask.paste(rotated_mask, tl)

    draw.polygon(list(best_rect.exterior.coords), outline=(0, 255, 0))
    return background_image, background_mask
