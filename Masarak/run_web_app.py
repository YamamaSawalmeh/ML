from flask import Flask

app = Flask(__name__)

# Load configuration settings
app.config.from_pyfile('config.py')

# Import routes
from web_app import app as web_app_routes

if __name__ == '__main__':
    app.run(debug=True)