import numpy as np
from PIL import Image
from itertools import product
from math import dist


def stereo_to_polar(
        stereo_in : Image.Image,
        theta_max : float,
        theta_centre : float,
        phi_centre : float) -> Image.Image:


    polar_out = Image.new(
        mode="RGB",
        size=stereo_in.size,
        color=(0, 0, 0)
    )

    # Address the pixels
    stereo_pixels = stereo_in.load()
    polar_pixels = polar_out.load()

    # Convenient constants
    origin = (int(polar_out.width/2), int(polar_out.height/2))
    twopi = 2. * np.pi

    # Iterate over output pixels
    for polar_x, polar_y in product(range(polar_out.width), range(polar_out.height)):

        # Find the polar phi value in radians
        if polar_x == origin:
            polar_phi = 0.
        else:
            polar_phi = np.atan2(polar_x - origin[0], polar_y - origin[1]) % twopi  # Keep positive

        # Find the theta value in radians. It can exceed physical values, since we
        #  are interested in exotic behaviour of the double-cover (or higher than double)
        polar_theta = dist((polar_x, polar_y), origin) * 2. * theta_max / polar_out.width

        # The stereoscopic theta reference will be equal to the polar, but:
        #  (1) First, modulo 2 pi to return to limit to a double cover
        #  (2) Next, if over 1 pi, find the conjugate (theta, phi) pair
        #     at phi -> phi + pi
        stereo_theta = (polar_theta + theta_centre) % twopi
        stereo_phi = polar_phi + phi_centre
        if stereo_theta > np.pi:
            stereo_theta = twopi - stereo_theta
            stereo_phi = (stereo_phi + np.pi) % twopi
        else:
            stereo_phi = stereo_phi % twopi

        # Find the pixel
        stereo_x = int(stereo_phi * polar_out.width / twopi)
        stereo_y = int(stereo_theta * (polar_out.height - 1) / np.pi)

        polar_pixels[polar_x, polar_y] = stereo_pixels[stereo_x, stereo_y]

        if (polar_y == 0) and (polar_x % 82 == 0):
            print(polar_x / polar_out.width)

    # Return the polar image
    return polar_out