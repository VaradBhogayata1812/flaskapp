import os
import json
import requests
from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True

api_key = os.getenv('API_KEY')

def fetch_movies_from_api():
    api_url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print("Failed to fetch movies")
        return []

@app.route('/')
def home_page():
    movies = fetch_movies_from_api()
    return render_template('movies_list.html', movies=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
