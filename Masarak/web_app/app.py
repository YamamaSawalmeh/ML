from flask import Flask, render_template, request, redirect, url_for
from src.ocr_module.diploma_scanner import scan_diploma
from src.ml_models.recommendation_model import get_recommendations
from src.utils.interest_assessment import assess_interests
import os

app = Flask(__name__)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = os.path.join('data', 'uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_diploma', methods=['GET', 'POST'])
def upload_diploma():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            diploma_data = scan_diploma(file_path)
            return redirect(url_for('interest_assessment', diploma_data=diploma_data))
    return render_template('upload_diploma.html')

@app.route('/interest_assessment', methods=['GET', 'POST'])
def interest_assessment():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        interests = assess_interests(user_data)
        recommendations = get_recommendations(interests)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('interest_assessment.html')

@app.route('/manual_entry', methods=['GET', 'POST'])
def manual_entry():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        interests = assess_interests(user_data)
        recommendations = get_recommendations(interests)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('manual_entry.html')

@app.route('/demographics_entry', methods=['GET', 'POST'])
def demographics_entry():
    if request.method == 'POST':
        demographics_data = request.form.to_dict()
        return redirect(url_for('interest_assessment', demographics_data=demographics_data))
    return render_template('demographics_entry.html')

if __name__ == '__main__':
    app.run(debug=True)