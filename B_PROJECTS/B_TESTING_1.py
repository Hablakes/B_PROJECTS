from difflib import SequenceMatcher

import imdb


def match_similar_strings(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_imdb_show(show_name):
    ia = imdb.IMDb()
    search_confidence_percentage = 0

    tv_imdb = ia.search_movie(show_name)

    possible_tv_show_matches_list = []

    for found_tv_plots in tv_imdb:
        if found_tv_plots['kind'] != 'tv series':
            continue

        search_confidence_percentage = match_similar_strings(show_name.lower(),
                                                             found_tv_plots['title'].lower())

        possible_tv_show_matches = \
            (found_tv_plots['title'], found_tv_plots.movieID, search_confidence_percentage)
        possible_tv_show_matches_list.append(possible_tv_show_matches)

    possible_tv_show_matches_list.sort(key=lambda x: x[2], reverse=True)

    if possible_tv_show_matches_list:
        tv_id = possible_tv_show_matches_list[0][1]
        tv_info_set = ia.get_movie(tv_id)
        return search_confidence_percentage, tv_info_set


print(find_imdb_show('jhfjkahsdjkldhsljkfhasd'))
print(find_imdb_show('The Expanse'))
