from AnilistPython import Anilist
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
import numpy as np
import csv


def setup():
    genres = ['sports', 'supernatural', 'comedy', 'ecchi', 'sci-fi', 'psychological', 'mahou shoujo', 'horror', 'drama',
              'thriller', 'action', 'mystery', 'hentai', 'music', 'fantasy', 'adventure', 'mecha', 'slice of life', 'romance']
    genre_ids = {}

    for i in range(len(genres)):
        genre_ids.update({genres[i]: i})

    genres_list = dict()
    with open('anime-db.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for key, value in row.items():
                if value == '':
                    continue
                int_value = int(value)
                if int_value in genres_list:
                    genres_list[int_value].append(key)
                else:
                    genres_list.update({int_value: [key]})

    ultimate_binary_list = []
    anime_id_at = []

    for anime_id, genre_list in genres_list.items():
        binary_list = [0] * len(genres)
        for genre in genre_list:
            binary_list[genre_ids[genre]] = 1
        anime_id_at.append(anime_id)
        ultimate_binary_list.append(np.array(binary_list))

    return genre_ids, anime_id_at, ultimate_binary_list


def get_recommendation(user_input: str, genre_ids: dict, anime_id_at: list, ultimate_binary_list: list) -> list[str]:
    anilist = Anilist()

    try:
        user_anime = anilist.get_anime(user_input)["genres"]
    # return empty list if cannot find user anime
    except IndexError:
        return []

    for i in range(len(user_anime)):
        user_anime[i] = user_anime[i].lower()

    usr_list = [0] * 19
    for genre in user_anime:
        usr_list[genre_ids[genre]] = 1

    sim_jaccard = []

    x = np.array(usr_list)
    # x = user or item vector
    # articles = vectors corresponding to every article

    for a in ultimate_binary_list:
        # if all vectors have binary values
        sim_jaccard.append(jaccard_score(x, a))

    result = []
    for i in range(len(sim_jaccard)):
        result.append((sim_jaccard[i], anime_id_at[i]))
    result.sort(reverse=True)

    recommend_list = []

    for i in range(4):
        anime = anilist.get_anime_with_id(result[i][1])
        anime_name = anime["name_english"]
        if (anime_name == None):
            anime_name = anime["name_romaji"]

        recommend_list.append(
            {"name": anime_name, "image": anime['cover_image'], "rating": anime['average_score']})

    return recommend_list


if __name__ == "__main__":
    genre_ids, anime_id_at, ultimate_binary_list = setup()
