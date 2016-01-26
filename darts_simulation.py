# Analysis of Darts strategies
#
# Author: Erik Rodner, 2016
#
# In the following, we analyze for which position on a dart
# board a player should aim at. The position depends on the
# aiming error of the player and we plot maps showing the expected score
# for different player skill levels.
#
# The following script was partly created during a lecture.

import numpy as np
import matplotlib.pylab as plt
import math
from scipy.misc import imsave
from mpltools import show_value_under_cursor


def get_dart_measurements(height = 500, width = 500, border = 100):
    # Some standard Dart measurements from wikipedia
    # The radius of the whole board
    mm_radius = 170.0
    # The radius to the outer border of the triple fields
    mm_triple_outer_radius = 107.0
    # The radius difference for double and triple fields
    mm_special_size = 8.0
    # The radius of the double bull with 50 points
    mm_double_bull_radius = 12.7/2
    # The radius of the bull with 25 points
    mm_bull_radius = 31.8/2

    # Converting the measurements to pixels
    m = {}
    m['radius'] = (height-border)/2
    m['scale'] = m['radius'] / mm_radius
    m['triple_outer_radius'] = mm_triple_outer_radius * m['scale']
    m['special_size'] = mm_special_size * m['scale']
    m['double_bull_radius'] = mm_double_bull_radius * m['scale']
    m['bull_radius'] = mm_bull_radius * m['scale']
    m['mx'] = width/2.0
    m['my'] = height/2.0

    return m


def get_darts_points(y, x, m):
    """ Return the score on a dart board drawn in an image """
    # The sectors of the Dart board
    points = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16,
            8, 11, 14, 9, 12, 5]
    num_main_fields = len(points)

   # Simple cases
    dy = (y-m['my'])
    dx = (x-m['mx'])
    distance_from_center = np.sqrt(dx**2 + dy**2)
    # Outside
    if distance_from_center>m['radius']:
        return 0.0
    # Double bull
    if distance_from_center<m['double_bull_radius']:
        return 50.0
    # Bull
    if distance_from_center<m['bull_radius']:
        return 25.0

    # Compute the angle relative to the beginning
    # of sector 20
    sector_angle = 2*math.pi / num_main_fields
    angle = math.atan2(-dy, dx)
    if angle<0:
        angle+=2*math.pi
    angle = (2*math.pi - angle) + math.pi/2.0 + sector_angle/2.0
    if angle>2*math.pi:
        angle -= 2*math.pi

    # Compute the sector index
    sector = int(angle/sector_angle)
    p = points[sector]
    # Check for triple or double fields
    if m['triple_outer_radius'] - m['special_size'] <= distance_from_center <= m['triple_outer_radius']:
        p *= 3
    if m['radius'] - m['special_size'] <= distance_from_center <= m['radius']:
        p *= 2

    # Return the points
    return p

def darts_image_create(height = 500, width = 500, border = 100):
    """ Create an image with a centered Dart board and its scores. """
    img = np.zeros([height, width])
    m = get_dart_measurements(height, width, border)
    for y in range(height):
        for x in range(width):
            img[y, x] = get_darts_points(y, x, m)

    return img, m

#
# Displaying a standard Dart score image
#
img, m = darts_image_create(1024, 1024, 200)
plt.figure()
plt.imshow(img, cmap=plt.get_cmap('rainbow'))
show_value_under_cursor(img)
plt.colorbar()
plt.show()

#
# Compute the expected score by convolving the image
# with different Gaussian filters
#
from scipy.ndimage.filters import gaussian_filter
# An accuracy_radius of 10mm means that in 95% of all cases the
# player is able to hit the dart board within a circle of radius 10mm around
# the position he was aiming at.
for index, accuracy_radius in enumerate([10, 25, 35, 50, 65, 80, 100, 120, 200]):
    plt.subplot(3,3,index+1)
    sigma = accuracy_radius / 2.0 * m['scale']
    print ("Analysis of a player with accuracy radius: {}mm".format(accuracy_radius))
    probs = gaussian_filter(img, sigma)
    y, x =  np.unravel_index(np.argmax(probs), probs.shape)
    plt.plot(x, y, 'wo', markersize=10, linewidth=50)
    print ("Aim for {}".format( get_darts_points(y, x, m) ))
    show_value_under_cursor(probs)
    plt.imshow(probs)
    plt.title('p(error <= {}mm)=0.95'.format(accuracy_radius))
    plt.colorbar()
plt.show()

