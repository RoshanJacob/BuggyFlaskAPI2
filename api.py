from numpy.core.numeric import moveaxis
from storage import all_movies, liked_movies, disliked_movies, unwatched_movies
from flask import Flask, request, jsonify
from demographicFiltering import output
from contentBasedFiltering import getRecommendations
# print(all_movies[1])

app = Flask(__name__)


@app.route('/get-movies')
def get_movies():
    return jsonify({
        "data": all_movies[0],
        "status": "success"
    })


@app.route('/update-liked-movies', methods=["POST"])
def update_liked_movies():
    global all_movies
    movie = all_movies[0]
    all_movies = all_movies[1:]
    liked_movies.append(movie)

    return jsonify({
        "status": "success"
    }), 201


@app.route('/get-liked-movies')
def get_liked_movies():
    return jsonify({
        "data": liked_movies[0],
        "status": "success"
    })


@app.route('/update-unliked-movies', methods=['POST'])
def update_unliked_movies():
    global all_movies
    unliked_movie = all_movies[0]
    all_movies = all_movies[1:]
    disliked_movies.append(unliked_movie)

    return jsonify({
        "status": "success"
    }), 201


@app.route('/get-disliked-movies')
def get_unliked_movies():
    return jsonify({
        "data": disliked_movies[0],
        "status": "success"
    })


@app.route('/update-unwatched-movies', methods=['POST'])
def update_unwatched_movies():
    global all_movies
    unwatched_movie = all_movies[0]
    all_movies = all_movies[1:]
    unwatched_movies.append(unwatched_movie)

    return jsonify({
        "status": "success"
    }), 201


@app.route('/get-unwatched-movies')
def get_unwatched_movies():
    return jsonify({
        "data": unwatched_movies[0],
        "status": "success"
    })


@app.route('/popular-movies')
def get_popular_movies():
    data = []
    for movie in output:
        item = {
            'title': movie[0],
            'poster_link': movie[1],
            'release_data': movie[2],
            'duration': movie[3],
            'rating': movie[4],
            'overview': movie[5]
        }
        data.append(item)
    return jsonify({
        'data': data,
        'status': 'success'
    })


@app.route('/recommended_movies')
def get_recommended_movies():
    all_recommended = []

    import itertools

    for liked_movie in liked_movies:
        output = getRecommendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    all_recommended.sort()
    all_recommended = list(
        all_recommended for all_recommended in itertools.groupby(all_recommended))
    recommended_movies = []
    for item in all_recommended:
        movie_data = {
            'title': item[0],
            'poster_link': item[1],
            'release_data': item[2],
            'duration': item[3],
            'rating': item[4],
            'overview': item[5]
        }
        recommended_movies.append(movie_data)

    return jsonify({
        'data': recommended_movies,
        'status': 'success'
    })


if __name__ == "__main__":
    app.run()
