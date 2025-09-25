# Provides utility functions for processing and visualising music rating data.
# Author: Gabrielle Hornshaw

# Imports #
import numpy as np

def chunks(lst, n):
    """
    Yields successive n-sized chunks from list.
    """

    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def stack_images(images, imsize, n_wide, n_high, inv = False, vert = True):
    """
    Stacks images into a single numpy array.
    """

    if vert == False:
        print("Not yet implemented: Horizontal image stack")
        exit()

    #Create sets of images (rows) and a base stacked array
    imsets = [images[i:i + n_wide] for i in range(0, len(images), n_wide)]
    stack = np.ones((n_high * imsize, n_wide * imsize, 3), dtype = np.uint8) * 255

    #Insert the images into the base stacked array
    for i in range(len(imsets)):
        for j in range(len(imsets[i])):
            if inv:
                stack[(n_high-i-1)*imsize:(n_high-i)*imsize, (n_wide-j-1)*imsize:(n_wide-j)*imsize, :] = imsets[i][j]
            else:
                stack[(n_high-i-1)*imsize:(n_high-i)*imsize, j*imsize:(j+1)*imsize, :] = imsets[i][j]
    
    return stack