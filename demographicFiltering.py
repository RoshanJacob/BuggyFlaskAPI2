# Demographic Filtering
import pandas as pd
import numpy as np

dataFrame2 = pd.read_csv('final.csv')

C = dataFrame2['vote_average'].mean()
# print(C)


M = dataFrame2['vote_count'].quantile(0.9)
# print(M)

top_movies = dataFrame2.copy().loc[dataFrame2['vote_count'] >= M]
# print(top_movies.shape)


def weighted_rating(x, M=M, C=C):
    V = x['vote_count']
    R = x['vote_average']

    return (V / (V + M) * R) + (M / (M + V) * C)


top_movies['score'] = top_movies.apply(weighted_rating, axis=1)
sorted_movies = top_movies.sort_values('score', ascending=False)

output = sorted_movies[['title_x', 'poster_link', 'release_date',
                        'runtime', 'vote_average', 'overview']].head(20).values.tolist()
