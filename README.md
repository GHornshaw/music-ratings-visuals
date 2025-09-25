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

![A bar chart for each rating category with the bars drawn with the covers of each album rated so far](https://github.com/GHornshaw/music-ratings-visuals/blob/main/visuals/album-bar-chart.png?raw=true)

This figure is a custom bar chart made by loading and resizing the album cover arts images (pulled from wikipedia pages), stacking them by rating into numpy arrays that then act as images drawn onto the axis to form a bar chart. The x axis is the rating categories (1-5) and the y axis is the number of albums (in multiples of 5 because each row in the stacked image contains 5 albums).

This figure shows that I have rated most albums 4/5 or 3/5. I have rated very few (only 6) albums 1/5 so far, likely because I am less willing to return to artists or genres that I have previously disliked.