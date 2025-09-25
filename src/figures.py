#Provides functions for making visualisations using Seaborn and Matplot
#Author: Gabrielle Hornshaw

# Imports #
import os
import math
import cv2
import numpy as np
import seaborn as sbn
import matplotlib.pyplot as plt
import matplotlib.lines as lns

from utils import stack_images

def create_album_bar(albums, imsize, n_wide, imspath):
    """
    Creates an album cover bar chart by stacking images from each rating into an array,
    Then using that array as an image to draw onto the figure.
    """

    categories = [1,2,3,4,5]

    #Get counts of each (for formatting uneven stacks)
    counts = albums['Rating'].value_counts()
    counts[0] = 0
    counts[6] = 0
    n_high = math.ceil(np.max(counts.values)/n_wide)

    stacks = []

    #For each category
    for cat in categories:
        #Get image filenames
        imfiles = albums[albums['Rating'] == cat]['Img']
        inv = True if (counts[cat-1] <= counts[cat+1]) else False

        #Load and prepare the images
        images = []
        for imfile in imfiles:
            im = cv2.resize(cv2.imread(os.path.join(imspath, imfile)), (imsize, imsize))
            im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR) #Colour convert
            im[0, :, :] = 0 #Borders for better definition around plain colour images
            im[:, 0, :] = 0
            im[imsize-1, :, :] = 0
            im[:, imsize-1, :] = 0
            images.append(im)

        #Stack the images
        stacks.append(stack_images(images, imsize, n_wide, n_high, inv, vert = True))

    #Create figure
    fig, axs = plt.subplots(1, 5, figsize = (len(categories)*2, (n_high/n_wide)*2), constrained_layout = True)
    for i, (stack, ax) in enumerate(list(zip(stacks, axs))):
        ax.imshow(stack, extent = [0, n_wide**2, 0, n_high*n_wide])
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.set_xlabel(categories[i])
    axs[0].spines.left.set_visible(True)
    axs[0].set_yticks(range(0, (math.ceil(np.max(counts.values)/n_wide) + 1) * n_wide, n_wide))
    
    return fig


def create_genre_rating_bar(albums, primary = False):
    """
    Creates a rating radar chart where the axes are the highest level genre for each album
    """

    #Create dataframes of ratings counts indexed by genre
    if primary:
        #Only use primary genre (Genre1)
        counts = albums.value_counts(['Genre1','Rating']).reset_index(name='Count')
        counts_pivot = counts.pivot(index='Genre1', columns='Rating', values='Count').fillna(0)
        counts_pivot = counts_pivot.reindex(index=albums['Genre1'].value_counts().index[::-1])
    else:
        #Use all genres (Genre1,Genre2,Genre3)
        albums_long = albums.melt(
            id_vars='Rating', 
            value_vars=['Genre1', 'Genre2', 'Genre3'],
            var_name='Genre_Col', 
            value_name='GenresAll'
        )
        albums_long = albums_long.dropna(subset=['GenresAll'])
        counts = albums_long.value_counts(['GenresAll', 'Rating']).reset_index(name='Count')
        counts_pivot = counts.pivot(index='GenresAll', columns='Rating', values='Count').fillna(0)
        counts_pivot = counts_pivot.reindex(index=albums_long['GenresAll'].value_counts().index[::-1])

    #Create the figure
    ax = counts_pivot.plot(
        kind='barh', 
        figsize=(12,14),
        stacked=True,
        width=0.8,
        colormap='inferno'
    )
    ax.tick_params(top=True, labeltop=True, bottom=True, labelbottom=True)
    ax.spines.right.set_visible(False)
    ax.legend(
        bbox_to_anchor = [1, 0.95], 
        loc='upper right',
        title='Rating',
        title_fontsize='x-large',
        fontsize='x-large',
        markerscale=1.5
    )
    plt.ylabel(None)
    plt.title("Albums by Genre")
    plt.tight_layout()

    return ax