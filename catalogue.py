import os
import json
import requests
from flask import Flask, request, render_template, jsonify
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

# Function to hash a password
def hash_password(plain_text_password):
    return bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

# Function to check a password
def check_password(hashed_password, plain_text_password):
    return bcrypt.check_password_hash(hashed_password, plain_text_password)

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

        return jsonify({'status': 'success', 'username': username}), 201
    else:
        return render_template('register.html')

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
            return jsonify({'status': 'success', 'message': 'Login successful'})
        else:
            return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
