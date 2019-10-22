import requests

from bs4 import BeautifulSoup
from difflib import SequenceMatcher


def match_similar_strings(a, b):
    return SequenceMatcher(None, a, b).ratio()


test_list = []

movie_to_search = r'https://www.imdb.com/search/title/?title=' + str("The matrix")

movie_plot_search = r'https://www.imdb.com/search/title-text/?plot=' + str("The matrix")

movie_response = requests.get(movie_to_search, timeout=5)

movie_imdb_page = BeautifulSoup(movie_response.text, 'html.parser')
movie_body_text = movie_imdb_page.find('div', class_='lister list detail sub-list')

movie_body_text_sections = movie_body_text.find_all('div', class_='lister-item')

for items in movie_body_text_sections:
    test = items.find('img')
    title = test['alt']
    imdb_id = test['data-tconst']

    movie_confidence_percentage = round(match_similar_strings('The Matrix'.lower(),
                                                              title.lower()), 2)

    if float(movie_confidence_percentage) >= 0.75:
        movie_title = title

        test_list.append([movie_title, imdb_id])

print(test_list[0])
