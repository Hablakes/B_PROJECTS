import requests

from bs4 import BeautifulSoup
from difflib import SequenceMatcher


def match_similar_strings(a, b):
    return SequenceMatcher(None, a, b).ratio()


def separator_1():
    print('-' * 100)


def separator_2():
    for items in '\n', '-' * 100:
        print(items)


def separator_3():
    for items in '\n', '-' * 100, '\n':
        print(items)


test_list = []

movie_to_search = r'https://www.imdb.com/search/title/?title=' + str("The matrix")
movie_response = requests.get(movie_to_search, timeout=5)
movie_imdb_page = BeautifulSoup(movie_response.text, 'html.parser')
movie_body_text = movie_imdb_page.find('div', class_='lister list detail sub-list')
movie_title_and_id_sections = movie_body_text.find_all(class_='lister-item mode-advanced')
movie_genres_plot_and_ratings_sections = movie_body_text.find_all(class_='lister-item-content')

separator_1()

for items in movie_title_and_id_sections:
    title = items.h3.a.text

    movie_search_confidence = round(match_similar_strings(title.lower(), str('The Matrix').lower()), 2)

    if float(movie_search_confidence) >= 0.75:
        movie_title = title
        certificate = items.find('span', class_='certificate')
        genre = items.find('span', class_='genre')
        imdb_id = items.img['data-tconst']
        plot_section = items.find_all('p')
        plot = plot_section[1]
        rating = items.strong

        if movie_title:
            print('TITLE: ', movie_title, '- SEARCH CONFIDENCE: ', movie_search_confidence, '\n')
        if certificate:
            print('CERTIFICATE: ', certificate.text, '\n')
        if genre:
            print('GENRE(S): ', genre.text, '\n')
        if imdb_id:
            print('IMDB ID#: ', imdb_id, '\n')
        if plot:
            print('PLOT: ', plot.text, '\n')
        if rating:
            print('RATING: ', rating.text, '\n')
        separator_1()
