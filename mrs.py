#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, render_template, jsonify

# Load data
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Prepare the user-item matrix
user_item_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

# Compute item similarity
item_similarity_matrix = cosine_similarity(user_item_matrix.T)
item_similarity = pd.DataFrame(
    item_similarity_matrix,
    index=user_item_matrix.columns,
    columns=user_item_matrix.columns
)

# Movie recommendation function
def get_movie_recommendations(user_id, top_n=5):
    if user_id not in user_item_matrix.index:
        raise ValueError(f"User {user_id} not found in the dataset.")
    user_ratings = user_item_matrix.loc[user_id]

    # Compute weighted scores for all items based on similarity and user's ratings
    weighted_scores = item_similarity.dot(user_ratings).div(item_similarity.sum(axis=1))
    
    # Exclude movies the user has already rated
    unrated_movies = weighted_scores[user_ratings == 0]

    # Get top N recommended movie IDs
    recommended_movie_ids = unrated_movies.nlargest(top_n).index

    # Fetch the movie titles from the movies DataFrame
    recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]['title'].tolist()
    return recommended_movies

# Initialize Flask app
app = Flask(__name__)
import logging

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Handle recommendation requests from the frontend.
    """
    try:
        data = request.get_json()# Retrieve JSON data from the request
        app.logger.debug(f"Received data: {data}")  
        user_id = int(data["user_id"]) # Get the user ID from the request data
        app.logger.debug(f"User ID received: {user_id}")
        recommendations = get_movie_recommendations(user_id)
        return jsonify({"recommendations": recommendations})
    except ValueError as e:
        app.logger.error(f"ValueError: {e}")
        return jsonify({"error": str(e)})
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        return jsonify({"error": "An unexpected error occurred."})

if __name__ == "__main__":
    app.run(port=5000, debug=True)




# In[ ]:





# In[ ]:





# In[ ]:




