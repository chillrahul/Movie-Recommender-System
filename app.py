from flask import Flask, request, render_template
import pickle
import pandas as pd
import requests

# Load precomputed data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))  # Dict mapping movie titles to metadata
similarity = pickle.load(open('similarity.pkl', 'rb'))  # Precomputed similarity matrix
new_df = pd.DataFrame.from_dict(movies_dict)
# Convert new_df to a list for easier slicing
movies = new_df['title'].tolist()
all_titles = new_df['title'].tolist() # TODO

app = Flask(__name__)

@app.route('/')
def home():
    # Display the first 5 movies
    movie_list = movies[:5]  # Fetch top 5 movies
    return render_template('index.html', movies=movie_list, recommendations=[], all_titles=all_titles)


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input
    movie_name = request.form.get('movie')
    if movie_name not in movies:
        error = "Movie not found! Please try a different name."
        return render_template('index.html', movies=movies[:5], recommendations=[], error=error, all_titles=all_titles)

    # Fetch recommendations
    movie_index = new_df[new_df['title'] == movie_name].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    print(distances[1:6])
    recommendations = []
    for i in distances[1: 6]:
        recommended_movie = new_df.iloc[i[0]]
        movie_id = recommended_movie['movie_id']
        poster_string = fetch_poster(movie_id)
        name_temp = recommended_movie['title']
        recommendations.append((movie_id, name_temp, poster_string))

    # recommendations = [movies[idx] for idx, _ in recommended_indices]


    return render_template('index.html', movies=movies[:5], recommendations=recommendations, all_titles=all_titles)

if __name__ == '__main__':
    app.run(debug=True)
