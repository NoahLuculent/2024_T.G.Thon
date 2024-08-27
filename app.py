from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.tgthon  # Replace 'mydatabase' with your database name
collection = db.time_letter  # Replace 'mycollection' with your collection name

@app.route('/')
def index():
    return render_template('create.html')

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form['email']
        password = request.form['password']

        # Create a document to insert inot MongoDB
        data = {
            'email': email,
            'password': password,
            'created_at': datetime.utcnow()
        }

        # Insert data inot MongoDB 
        collection.insert_one(data)

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)