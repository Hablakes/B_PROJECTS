import requests
from bs4 import BeautifulSoup


movie_to_search = r'https://www.imdb.com/search/title/?title=' + str("The matrix")

movie_plot_search = r'https://www.imdb.com/search/title-text/?plot=' + str("The matrix")

movie_response = requests.get(movie_to_search, timeout=5)

movie_imdb_page = BeautifulSoup(movie_response.text, 'html.parser')
movie_body_text = movie_imdb_page.find('div', class_='lister list detail sub-list')

movie_body_text_sections = movie_body_text.find_all('div', class_='lister-item')

for items in movie_body_text_sections:
    test = items.find('img')
    print(test['alt'], test['data-tconst'])
