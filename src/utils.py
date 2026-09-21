# Provides utility functions for processing and visualising music rating data.
# Author: Gabrielle Hornshaw

# Imports #
import re
import urllib
import numpy as np
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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


def get_wiki(url):
    """Return an album's wikipedia html page"""

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request) as response:
        soup = BeautifulSoup(response.read(), "html.parser")
    return soup


def clean_wiki_section(section):
    """Remove numerical Wikipedia citation references from section text"""

    citation_pattern = r" \[\s*\d+(?:\s*,\s*\d+)*\s*\]"
    return re.sub(citation_pattern, "", section)


def tokenize_wiki_section(section):
    """Tokenize the wiki section text, removing low utility tokens"""

    #tokens = re.findall(r'\w+', section)
    tokens = word_tokenize(section.lower())
    stop_words = set(stopwords.words('english'))
    punc = ('.', ',', '!', '?', '~', ';', ':', '\'\'', '``', '{', '(', '[', '}', ')', ']')
    inval = ('album', 'song', 'release', 'released', '\'s', 'n\'t')
    stop_words.update(punc)
    stop_words.update(inval)
    tokens = [token for token in tokens if token not in stop_words]

    return tokens


def get_wiki_genres(soup):
    """Return the genres listed in an album's Wikipedia page"""

    for row in soup.select("table.infobox tr"):
        heading = row.find(["th", "td"])
        if heading and heading.get_text(" ", strip=True).lower() == "genres":
            genre_cell = row.find("td")
            if genre_cell is None:
                return []

            genres = [
                link.get_text(" ", strip=True).lower()
                for link in genre_cell.find_all("a")
            ]

            return list(dict.fromkeys(filter(None, genres)))

    return []


def get_wiki_sections(soup):
    """Return a dictionary containing the text from every Wikipedia article section"""

    sections = {}
    headings = soup.select("h2, h3, h4, h5, h6")
    ignore_sections = [
        "Track listing",
        "Tours", 
        "Personnel", 
        "Charts", 
        "Certifications", 
        "See also", 
        "References",
        "External links"
    ]
    ignored_level = None

    for heading in headings:
        heading_text = heading.get_text(" ", strip=True)
        heading_text = re.sub(r"\[.*?\]", "", heading_text).strip()
        heading_level = int(heading.name[1])

        if ignored_level is not None:
            if heading_level > ignored_level:
                continue
            ignored_level = None

        if heading_text in ignore_sections:
            ignored_level = heading_level
            continue

        paragraphs = []

        for element in heading.find_all_next():
            if element.name and re.fullmatch(r"h[2-6]", element.name):
                if int(element.name[1]) <= heading_level:
                    break
            elif element.name == "p":
                text = element.get_text(" ", strip=True)
                if text:
                    paragraphs.append(text)

        sections[heading_text] = clean_wiki_section(" ".join(paragraphs))

    return sections