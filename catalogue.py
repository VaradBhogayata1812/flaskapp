import os
import json
import requests
from flask import Flask, request, render_template, jsonify, redirect, url_for
import bcrypt
import pymysql

# Configure your database connection here
db_config = {
    'host': 'myflix-user-database.c6bg2uvvdgty.us-east-1.rds.amazonaws.com',
    'database': 'myflixusers',
    'user': 'admin',
    'password': 'Varad#1812'
}

# Establish the database connection
db_connection = pymysql.connect(**db_config)

# Create a cursor object
cursor = db_connection.cursor()


app = Flask(__name__)
app.debug = True

api_key = os.getenv('API_KEY')

# Function to hash a password
def hash_password(plain_text_password):
    return bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

# Function to check a password
def check_password(hashed_password, plain_text_password):
    return bcrypt.check_password_hash(hashed_password, plain_text_password)

def fetch_movies_from_api():
    api_url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print("Failed to fetch movies")
        return []
    
def fetch_featured_movies():
    # Implement logic to fetch a limited number of movies
    # For simplicity, let's fetch the first 5 popular movies
    api_url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&page=1"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['results'][:5]
    else:
        print("Failed to fetch featured movies")
        return []
    
@app.route('/')
def home_page():
    # Fetch only a few featured movies for the homepage
    featured_movies = fetch_featured_movies()
    return render_template('home.html', featured_movies=featured_movies)

@app.route('/movies')
def movies_page():
    # This page shows the full movie list and is accessible after login
    movies = fetch_movies_from_api()
    return render_template('movies_list.html', movies=movies)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        plain_text_password = request.form.get('password')

        # Create a new database connection
        db_connection = pymysql.connect(**db_config)
        cursor = db_connection.cursor()

        # Fetch the user's hashed password from the database
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        user_record = cursor.fetchone()

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()

        # Verify the password
        if user_record and check_password(user_record[0], plain_text_password):
            # Redirect to movies page after successful login
            return redirect(url_for('movies_page'))
        else:
            # Return an error message if login fails
            # Consider rendering a page with an error message instead of JSON response
            return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401
    else:
        return render_template('login.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        plain_text_password = request.form.get('password')

        # Create a new database connection
        db_connection = pymysql.connect(**db_config)
        cursor = db_connection.cursor()

        # Hash the password
        hashed_password = hash_password(plain_text_password)

        # Execute SQL command
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                       (username, hashed_password))
        db_connection.commit()

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
