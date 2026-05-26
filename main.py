from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from mapreduce import run_mapreduce
from database import save_results

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Secret key from .env
app.secret_key = os.environ.get("SECRET_KEY", "fallbacksecretkey")


# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Default admin credentials
USERNAME = "admin"
PASSWORD = "admin123"

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:

            session['user'] = username

            return redirect(url_for('upload_file'))

        else:
            return "Invalid Username or Password"

    return render_template('login.html')


# Upload Route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    # Check if logged in
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        if 'logfile' not in request.files:
            return "No file selected"

        file = request.files['logfile']

        if file.filename == '':
            return "No file selected"

        filename = secure_filename(file.filename)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        results = run_mapreduce(filepath)
        save_results(filename, results)
        
        return render_template('dashboard.html', results=results)

    return render_template('upload.html')


# Logout Route
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect(url_for('login'))

@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error Occurred", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)