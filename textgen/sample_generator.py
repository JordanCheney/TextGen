import os
import random as rnd

from PIL import Image, ImageFilter

from textgen.text_generator import generate_text
from textgen.white_background import generate_white_background


def generate_sample(index, text, gen_opts, generate_background):
    # Do an initial text generation with a fixed sized, this is mostly to compute the aspect ratio of the output sample
    image, mask = generate_text(index, text, 80, gen_opts)

    return generate_image_with_background(image, mask)
    background_image, text_image, pos = generate_background(image)

    background_mask = Image.new(
        "RGB", background_image.size, (0, 0, 0)
    )

    background_image.paste(text_image, pos, text_image)

    return background_image, mask
'''
class FakeTextDataGenerator(object):
    @classmethod
    def generate(
        cls,
        index,
        text,
        font,
        out_dir,
        size,
        extension,
        skewing_angle,
        random_skew,
        blur,
        random_blur,
        background_type,
        distorsion_type,
        distorsion_orientation,
        is_handwritten,
        name_format,
        width,
        alignment,
        text_color,
        orientation,
        space_width,
        character_spacing,
        margins,
        fit,
        output_mask,
        word_split,
        image_dir,
    ):
        image = None

        margin_top, margin_left, margin_bottom, margin_right = margins
        horizontal_margin = margin_left + margin_right
        vertical_margin = margin_top + margin_bottom

        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            if orientation == 1:
                raise ValueError("Vertical handwritten text is unavailable")
            image, mask = handwritten_text_generator.generate(text, text_color)
        else:
            image, mask = computer_text_generator.generate(
                text,
                font,
                text_color,
                size,
                orientation,
                space_width,
                character_spacing,
                fit,
                word_split,
            )

        #############################
        # Skew                      #
        #############################
        if random_skew:
            random_angle = rnd.randint(0 - skewing_angle, skewing_angle)

        rotated_img = image.rotate(
            skewing_angle if not random_skew else random_angle, expand=1
        )

        rotated_mask = mask.rotate(
            skewing_angle if not random_skew else random_angle, expand=1
        )

        ##################################
        # Resize image to desired format #
        ##################################

        # Horizontal text
        #if orientation == 0:
        #    new_width = int(
        #        distorted_img.size[0]
        #        * (float(size - vertical_margin) / float(distorted_img.size[1]))
        #    )
        #    rotated_img = distorted_img.resize(
        #        (new_width, size - vertical_margin), Image.ANTIALIAS
        #    )
        #    rotated_mask = distorted_mask.resize((new_width, size - vertical_margin), Image.NEAREST)
        #    background_width = width if width > 0 else new_width + horizontal_margin
        #    background_height = size
        # Vertical text
        #elif orientation == 1:
        #    new_height = int(
        #        float(distorted_img.size[1])
        #        * (float(size - horizontal_margin) / float(distorted_img.size[0]))
        #    )
        #    rotated_img = distorted_img.resize(
        #        (size - horizontal_margin, new_height), Image.ANTIALIAS
        #    )
        #    rotated_mask = distorted_mask.resize(
        #        (size - horizontal_margin, new_height), Image.NEAREST
        #    )
        #    background_width = size
        #    background_height = new_height + vertical_margin
        #else:
        #    raise ValueError("Invalid orientation")

        #############################
        # Generate background image #
        #############################
        if background_type == 0:
            background_img, paste_location = background_generator.gaussian_noise(
                image.size[0], image.size[1], margin_left, margin_top
            )
        elif background_type == 1:
            background_img, paste_location = background_generator.plain_white(
                image.size[0], image.size[1], margin_left, margin_top
            )
        elif background_type == 2:
            background_img, paste_location = background_generator.quasicrystal(
                image.size[0], image.size[1], margin_left, margin_top
            )
        else:
            background_img, paste_location = background_generator.image(
                image_dir, image.size[0], image.size[1], skewing_angle
            )
        print(paste_location, background_img.size)
        background_mask = Image.new(
            "RGB", background_img.size, (0, 0, 0)
        )

        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = rotated_img.size

        if alignment == 0:
            background_img.paste(rotated_img, (margin_left, margin_top), rotated_img)
            background_mask.paste(rotated_mask, (margin_left, margin_top))
        elif alignment == 1:
            background_img.paste(
                rotated_img, paste_location, rotated_img
            )
            background_mask.paste(
                rotated_mask, paste_location
            )
        else:
            background_img.paste(
                rotated_img,
                (background_width - new_text_width - margin_right, margin_top),
                rotated_img,
            )
            background_mask.paste(
                rotated_mask,
                (background_width - new_text_width - margin_right, margin_top),
            )

        ##################################
        # Apply gaussian blur #
        ##################################

        gaussian_filter = ImageFilter.GaussianBlur(
            radius=blur if not random_blur else rnd.randint(0, blur)
        )
        final_image = background_img.filter(gaussian_filter)
        final_mask = background_mask.filter(gaussian_filter)

        #####################################
        # Generate name for resulting image #
        #####################################
        if name_format == 0:
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))
        elif name_format == 1:
            image_name = "{}_{}.{}".format(str(index), text, extension)
            mask_name = "{}_{}_mask.png".format(str(index), text)
        elif name_format == 2:
            image_name = "{}.{}".format(str(index), extension)
            mask_name = "{}_mask.png".format(str(index))
        else:
            print("{} is not a valid name format. Using default.".format(name_format))
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))

        # Save the image
        if out_dir is not None:
            final_image.convert("RGB").save(os.path.join(out_dir, image_name))
            if output_mask == 1:
                final_mask.convert("RGB").save(os.path.join(out_dir, mask_name))
        else:
            if output_mask == 1:
                return final_image.convert("RGB"), final_mask.convert("RGB")
            return final_image.convert("RGB")
'''
