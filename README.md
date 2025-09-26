# music-ratings-visuals
Visualising my music taste after listening to 200+ albums.

This is a project to demonstrate some data processing and visualisation skills, and hopefully when there's enough data, to provide me with some insights into the patterns of my music taste.

Current number of albums included: **207**

## The project:

Since 2022 I have made it a mission to listen to as many albums as possible and rate them so as to eventually be able to analyse my music taste from many data points and possibly model predictions. The rules are:

1) The album must be listened to at least twice, 1+ week apart.
2) The album must be listened to in different circumstances (e.g. walking, doing the dishes)
3) The album must be listened to all the way through uninterupted, in its intended order.
4) As much attention as possible must be paid to the music (no distractions).

Each album is rated on an ordered categorical scale from 1-5, based on two possible interpretations:

| Rating    | If I was made to listen again: | Would I reccommend it?         |
| --------- | ------------------------------ | ------------------------------ |
| 1         | Turn it off immediately        | No, I hate it                  |
| 2         | Disappointed or bored          | No, it's not a must-listen     |
| 3         | Feeling ok about it            | Maybe under some circumstances |
| 4         | Really liking it               | Yes, very worth a listen       |
| 5         | Very happy, love it            | Yes, it's flawless             |

## Visualisations

![A bar chart for each rating category with the bars drawn with the covers of each album rated so far.](https://github.com/GHornshaw/music-ratings-visuals/blob/main/visuals/album-bar-chart.png?raw=true)

This custom bar chart shows the number of albums per rating. It was made by combining album cover art images into five different numpy arrays, grouped by their rating, which then acted as images to be drawn onto the axis to form a bar chart. The function allows for different bar widths (number of albums across), and changing it automatically updates the y-axis scale (currently, each row is five albums). Incomplete top rows are populated from the side which has more albums to give it a more rounded look.

This figure shows that I have rated most albums 4/5 and given a rating of 1/5 to the least albums (only 6). This is a fairly standard bell curve leaning towards higher ratings, which is predictable as I would be more likely to return to artists or genres that I have previously rated highly and avoid those I strongly dislike.

![A horizontal stacked bar chart showing the number of albums of each genre rated, coloured by the ratings given.](https://github.com/GHornshaw/music-ratings-visuals/blob/main/visuals/genre_rating_bar.png?raw=true)

This horizontal stacked bar chart shows the number of albums rated for each genre, coloured by the ratings given. Unsurprisingly, the most common genres have been rock and pop. Some notable genres without many entries are disco, reggae, and punk - I should listen to more of them. Interestingly, most of the genres have quite an even spread of ratings, but some stand out as much more liked - thrash metal, alt pop, and grunge, for instance. On the flip side, I don't seem to be a fan of art rock, ambient, or jazz music.

![A geographical heat map showing the number of different artists rated for each country of origin.](https://github.com/GHornshaw/music-ratings-visuals/blob/main/visuals/origin_country_map.png?raw=true)

This geographic heat map shows the number of individual artists (not albums) I have rated per country of origin. It's not looking very interesting currently as most artists have been from the US and the UK. In order to allow better visiblity of countries I have listened to *any* music from over countries I haven't, I created a custom color-map that starts with a dark grey for 0, before jumping to the lowest heat map colour at 1.

## Upcoming

I am planning to include a visualisation of average album/song lengths against my ratings to identify if there is any pacing I tend to like or dislike more, but I will first have to populate the spreadsheet with album lengths.

I am also planning to plot my ratings over time, coloured by genre, to identify if there have been (or will be) any changes to my taste since starting. In order to do this I will have to include date of entry in the spreadsheet and back-fill it (difficult).