#Provides functions for making visualisations using Seaborn and Matplot
#Author: Gabrielle Hornshaw

# Imports #
import os
import math
import cv2
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sbn
import matplotlib as mpl
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

    plt.suptitle("Number of Albums by Rating", fontsize=16, horizontalalignment='center')
    
    return fig


def create_genre_rating_bar(albums, primary = False):
    """
    Creates a horizontal bar chart showing the number of ratings per genre,
    Coloured by rating
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
    plt.title("Number of Ratings by Genre", fontsize=16)
    plt.tight_layout()

    return ax


def create_artist_origin_map(albums, filepath):
    """
    Create a world map heatmap showing the number of rated artists from each country
    """

    #Load and process the geometry dataframe
    geo_df = gpd.read_file(os.path.join(filepath, "geo_shapefile", "ne_10m_admin_0_countries.shp"))[['ADMIN', 'ADM0_A3', 'geometry']]
    geo_df.columns = ['country','country_code','geometry']
    geo_df = geo_df.drop(geo_df.loc[geo_df['country'] == 'Antarctica'].index)

    #Select artists and countries, drop duplicates
    countries = albums[['Artist','Country']].drop_duplicates()['Country']
    #Reformat some common ones to how they are written in geo_df
    countries = countries.replace(['England','Wales','Scotland'], 'United Kingdom')
    countries = countries.replace('USA', 'United States of America')
    countries = countries.drop(countries.loc[countries == 'Multiple'].index)
    #Count instances of each origin country in ratings
    geo_counts = countries.value_counts()
    merged_df = pd.merge(left=geo_df, right=geo_counts, how='left', left_on='country', right_on='Country').fillna(0)

    #Create custom colormap - dark grey for values of 0, heatmap for the rest
    ocmap = sbn.color_palette("viridis", as_cmap=True)
    cmap = np.insert(ocmap(np.linspace(0, 1, geo_counts[0])), 0, mpl.colors.to_rgba('dimgrey'), axis=0)
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", cmap)

    #Create the figure
    fig, ax = plt.subplots(1, figsize=(16, 6))
    ax.axis('off')
    merged_df.plot(column='count', ax=ax, edgecolor='0.0', linewidth=0.1, cmap=cmap)
    plt.title("Number of Rated Artists by Country of Origin", color='white', fontsize=16)
    fig.set_facecolor("black")

    #Create the colorbar legend
    sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=0, vmax=geo_counts[0]), cmap=ocmap)
    sm._A = []
    cbax = fig.add_axes([0.15, 0.1, 0.01, 0.4])
    cb = fig.colorbar(sm, cax=cbax)
    cb.outline.set_visible(False)
    cbax.yaxis.label.set_color('white')
    cbax.tick_params(axis='y', colors='white')

    plt.tight_layout()

    return fig