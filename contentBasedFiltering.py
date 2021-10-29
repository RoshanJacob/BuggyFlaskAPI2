from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from ast import NodeTransformer, literal_eval
import numpy as np
import pandas as pd

dataFrame2 = pd.read_csv('final.csv')
dataFrame2 = dataFrame2['metadata'].notna()

count = CountVectorizer(stop_words="english")

count_matrix = count.fit_transform(dataFrame2['metadata'])


count_matrix.toarray()

CosineMatcher = cosine_similarity(count_matrix, count_matrix)


# dataFrame2 = dataFrame2.reset_index()
indices = pd.Series(dataFrame2.index, index=dataFrame2['original_title'])


def getRecommendations(title, matcher):
    index = indices[title]
    print(index)

    sim_scores = list(enumerate(matcher[index]))
    print(sim_scores)

    sorted_simscores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    print(sorted_simscores)

    sorted_simscores = sorted_simscores[1:11]
    movie_indices = [i[0] for i in sorted_simscores]
    print(movie_indices)

    return dataFrame2[['title', 'poster_link', 'release_date', 'runtime', 'vote_average', 'overview']].iloc[movie_indices].values.tolist()
