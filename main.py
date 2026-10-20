import numpy as np
from PIL import Image
from transforms import stereo_to_polar

stereo_img = Image.open("lo res earth.jpg")

print("Original resolution:", stereo_img.size)

polar_img = stereo_to_polar(
    stereo_img,
    6. * np.pi,
    0., 0.)

stereo_img.save("stereo.jpg")
polar_img.save("polar.jpg")
