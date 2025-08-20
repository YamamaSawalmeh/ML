"""
Flask application for University Recommendation System
"""

import os
import json
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import pandas as pd
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import Config
# Use relative imports that will work both with direct import and when run as a module
try:
    # Try relative import first (when imported as a module)
    from ..ml_models.recommendation_model import UniversityRecommendationModel
    from ..ocr_module.diploma_scanner import DiplomaScanner
    from ..utils.interest_assessment import InterestAssessment
except (ImportError, ValueError):
    # Fall back to absolute imports (when run directly)
    from src.ml_models.recommendation_model import UniversityRecommendationModel
    from src.ocr_module.diploma_scanner import DiplomaScanner
    from src.utils.interest_assessment import InterestAssessment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize app
app = Flask(__name__)
app_config = Config()
app.config['SECRET_KEY'] = app_config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = app_config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = app_config.MAX_CONTENT_LENGTH
app.config['ALLOWED_EXTENSIONS'] = app_config.ALLOWED_EXTENSIONS

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize modules
try:
    # Force re-training of the model to fix the "Model not trained yet" error
    import pandas as pd
    import os
    
    # Check if model files exist
    model_path = "data/models"
    model_files_exist = os.path.exists(model_path) and any([
        f for f in os.listdir(model_path) if f.endswith('.joblib')
    ]) if os.path.exists(model_path) else False
    
    logger.info(f"Model files exist: {model_files_exist}")
    
    if model_files_exist:
        # Try to load with existing model files
        recommendation_model = UniversityRecommendationModel(use_saved_model=True)
        logger.info("Loaded existing model successfully")
    else:
        # Train a new model if files don't exist
        logger.info("Training new model as model files do not exist")
        data_path = "data/dummy/student_profiles.csv"
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            recommendation_model = UniversityRecommendationModel(use_saved_model=False)
            metrics = recommendation_model.train(data)
            recommendation_model._save_model()
            logger.info(f"Model trained and saved. Accuracy: {metrics['random_forest']['accuracy']:.4f}")
        else:
            logger.error(f"Training data not found at {data_path}")
            recommendation_model = UniversityRecommendationModel()
    
    diploma_scanner = DiplomaScanner()
     
    interest_assessment = InterestAssessment()
    logger.info("Models and modules initialized successfully")
except Exception as e:
    logger.error(f"Error initializing modules: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())


def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render the home page"""
    language = request.args.get('lang', 'en')
    return render_template('index.html', language=language)


@app.route('/upload_diploma', methods=['GET', 'POST'])
def upload_diploma():
    """Handle diploma upload and OCR processing"""
    language = request.args.get('lang', 'en')
    
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'diploma_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['diploma_file']
        
        # If the user does not select a file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Save the file
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Process the file with OCR
                result = diploma_scanner.run_ocr(filepath)
                
                # Validate and extract information
               
                
                # Store in session for next steps
                session['diploma_data'] = result
                return redirect(url_for('manual_entry', lang=language))
                # Identify missing fields
               
                
               
            
            except Exception as e:
                logger.error(f"Error processing diploma: {str(e)}")
                flash(f"Error processing diploma: {str(e)}")
                return redirect(request.url)
    
    return render_template('upload_diploma.html', language=language)


@app.route('/manual_entry', methods=['GET', 'POST'])
def manual_entry():
    """Handle manual entry of student academic data"""
    language = request.args.get('lang', 'en')
    
    if request.method == 'POST':
        try:
            # Get data from form
            form_data = request.form.to_dict()
            
            # Process academic data
            academic_data = {
                'stream': form_data.get('stream'),
                'scores': {}
            }
            
            # Extract scores
            for field, value in form_data.items():
                if field.startswith('score_') and value:
                    subject = field.replace('score_', '')
                    academic_data['scores'][subject] = float(value)
            
            # Store in session for next step
            session['academic_data'] = academic_data
            
            #print(academic_data)
            # Redirect to demographics form
            return redirect(url_for('demographics_entry', lang=language))
        
        except Exception as e:
            logger.error(f"Error processing manual entry: {str(e)}")
            flash(f"Error processing form data: {str(e)}")
            return redirect(request.url)
    
    # Get diploma data from session if available
    diploma_data = session.get('diploma_data', {})
    
    return render_template(
        'manual_entry.html',
        diploma_data=diploma_data,
        language=language
    )


@app.route('/demographics_entry', methods=['GET', 'POST'])
def demographics_entry():
    """Handle entry of student demographic information"""
    language = request.args.get('lang', 'en')
    
    if request.method == 'POST':
        try:
            # Get data from form
            form_data = request.form.to_dict()
            
            # Process demographic data
            demographic_data = {
                'first_name': form_data.get('first_name'),
                'family_name': form_data.get('family_name'),
                'gender': form_data.get('gender'),
                'age': int(form_data.get('age', 18)),
                'city': form_data.get('city'),
                'family_size': int(form_data.get('family_size', 4)),
                'family_income': float(form_data.get('family_income', 3000)),
                'income_level': form_data.get('income_level', 'medium'),
                'father_education': form_data.get('father_education', 'secondary'),
                'mother_education': form_data.get('mother_education', 'secondary')
            }
            
            # Store in session for next step
            session['demographic_data'] = demographic_data
            
            # Redirect to interest assessment
            return redirect(url_for('interest_assessment_page', lang=language))
        
        except Exception as e:
            logger.error(f"Error processing demographics entry: {str(e)}")
            flash(f"Error processing form data: {str(e)}")
            return redirect(request.url)
    
    return render_template('demographics_entry.html', language=language)


@app.route('/interest_assessment', methods=['GET', 'POST'])
def interest_assessment_page():
    """Handle interest assessment questionnaire"""
    language = request.args.get('lang', 'en')
    
    if request.method == 'POST':
        try:
            # Get responses from form
            form_data = request.form.to_dict()
            
            # Convert responses to integer values
            responses = {}
            for question_id, response in form_data.items():
                if question_id.startswith(('p', 's', 'c', 'a')) and response.isdigit():
                    responses[question_id] = int(response)
            
            # Store all responses in session for later use - make sure everything is native Python type
            session['interest_responses'] = {k: ensure_json_serializable(v) for k, v in responses.items()}
            
            # Analyze responses
            results = interest_assessment.analyze_responses(responses)
            
            # Format results
            formatted_results = interest_assessment.format_results(results, language)
            
            # Store in session for next step - ensure all values are JSON serializable
            session['interest_results'] = ensure_json_serializable(formatted_results)
            
            # Create complete student profile
            student_profile = create_student_profile(
                session.get('academic_data', {}),
                session.get('demographic_data', {}),
                formatted_results
            )
            
            # Get recommendations
            language = request.args.get('lang', 'en')
            recommendations = generate_recommendations(student_profile, language)
            session['recommendations'] = ensure_json_serializable(recommendations)
            
            # Redirect to recommendations page
            return redirect(url_for('recommendations', lang=language))
        
        except Exception as e:
            logger.error(f"Error processing interest assessment: {str(e)}")
            flash(f"Error processing assessment: {str(e)}")
            return redirect(request.url)
    
    # Get questionnaire
    questionnaire = interest_assessment.get_questionnaire(language)
    
    return render_template(
        'interest_assessment.html',
        questionnaire=questionnaire,
        language=language
    )


@app.route('/recommendations')
def recommendations():
    """Display university field recommendations"""
    language = request.args.get('lang', 'en')
    
    # Get recommendations from session
    recommendations = session.get('recommendations', {})
    
    return render_template(
        'recommendations.html',
        recommendations=recommendations,
        language=language,
        config=app_config
    )


@app.route('/api/process_diploma', methods=['POST'])
def api_process_diploma():
    """API endpoint for processing diploma"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Get file type
            file_extension = os.path.splitext(file.filename)[1].lower()[1:]
            
            # Process file bytes
            result = diploma_scanner.process_bytes(file.read(), file_extension)
            
            # Validate results
           
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"API error processing diploma: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400


@app.route('/api/analyze_interests', methods=['POST'])
def api_analyze_interests():
    """API endpoint for analyzing interest assessment responses"""
    try:
        data = request.get_json()
        
        if not data or 'responses' not in data:
            return jsonify({'error': 'No response data provided'}), 400
        
        responses = data['responses']
        language = data.get('language', 'en')
        
        # Analyze responses
        results = interest_assessment.analyze_responses(responses)
        
        # Format results
        formatted_results = interest_assessment.format_results(results, language)
        
        return jsonify(formatted_results)
        
    except Exception as e:
        logger.error(f"API error analyzing interests: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_recommendations', methods=['POST'])
def api_get_recommendations():
    """API endpoint for generating recommendations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create student profile
        student_profile = data.get('student_profile', {})
        
        # Get language preference
        language = data.get('language', 'en')
        
        # Generate recommendations
        recommendations = generate_recommendations(student_profile, language)
        
        return jsonify(recommendations)
        
    except Exception as e:
        logger.error(f"API error getting recommendations: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Helper function to ensure JSON serializable values
def ensure_json_serializable(value):
    """Convert NumPy types to native Python types"""
    import numpy as np
    if isinstance(value, (np.integer, np.int32, np.int64)):
        return int(value)
    elif isinstance(value, (np.floating, np.float32, np.float64)):
        return float(value)
    elif isinstance(value, np.bool_):
        return bool(value)
    elif isinstance(value, np.ndarray):
        return value.tolist()
    elif isinstance(value, dict):
        return {k: ensure_json_serializable(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [ensure_json_serializable(i) for i in value]
    return value


def create_student_profile(academic_data, demographic_data, interest_results):
    """
    Create a complete student profile with all required features for the model
    """
    # Start with basic profile info
    profile = {
        'academic_tawjihi_stream': academic_data.get('stream', 'scientific'),
        'personality_type': interest_results.get('personality', {}).get('type', 'analytical'),
        'academic_ability_level': 'medium',  # Default value
        'academic_overall_average': 80.0     # Default value
    }
    
    # Add demographic data with 'demo_' prefix
    for key, value in demographic_data.items():
        profile[f'demo_{key}'] = value
    
    # Ensure all required demographic fields exist
    required_demo_fields = {
        'gender': 'male',
        'age': 18,
        'city': 'Jerusalem',
        'family_size': 5,
        'family_income': 4000.0,
        'income_level': 'medium',
        'father_education': 'secondary',
        'mother_education': 'secondary'
    }
    
    for field, default_value in required_demo_fields.items():
        demo_field = f'demo_{field}'
        if demo_field not in profile:
            profile[demo_field] = default_value
    
    # Process academic scores
    if 'scores' in academic_data and academic_data['scores']:
        # Use provided scores
        for subject, score in academic_data['scores'].items():
            profile[f'score_{subject}'] = float(score)
        
        # Calculate overall average if not already set
        if 'score_overall_average' not in profile and academic_data['scores']:
            scores = [float(score) for score in academic_data['scores'].values()]
            profile['score_overall_average'] = sum(scores) / len(scores)
    else:
        # Set default scores
        default_scores = {
            'mathematics': 75.0,
            'physics': 75.0,
            'chemistry': 75.0,
            'biology': 75.0,
            'arabic': 75.0,
            'english': 75.0,
            'overall_average': 75.0
        }
        for subject, score in default_scores.items():
            profile[f'score_{subject}'] = score
    
    # Ensure all possible subject scores are included
    all_subjects = [
        'mathematics', 'physics', 'chemistry', 'biology', 'arabic', 'english',
        'accounting', 'economics', 'business_studies', 'technical_drawing', 
        'workshop_practice', 'history', 'geography', 'islamic_studies',
        'philosophy', 'agricultural_sciences', 'nutrition', 'child_development', 'textiles'
    ]
    
    for subject in all_subjects:
        if f'score_{subject}' not in profile:
            profile[f'score_{subject}'] = 0.0
    
    # Process interest responses from the session
    interest_responses = session.get('interest_responses', {})
    
    # Map the form responses to the format expected by the model
    interest_mapping = {
        'p': 'personality',
        's': 'subjects',
        'c': 'career_goals',
        'a': 'activities'
    }
    
    # Initialize all interest fields with default values
    for category in ['personality', 'subjects', 'career_goals', 'activities']:
        max_questions = 20 if category == 'personality' else 15
        if category == 'career_goals' or category == 'activities':
            max_questions = 10
            
        for i in range(max_questions):
            field_name = f'interest_{category}_{i}'
            profile[field_name] = 3  # Default neutral value
    
    # Override with actual responses from the form
    for q_id, response in interest_responses.items():
        if len(q_id) > 1:
            category_code = q_id[0]
            question_num = int(q_id[1:]) - 1  # Convert from 1-based to 0-based index
            
            if category_code in interest_mapping:
                category = interest_mapping[category_code]
                field_name = f'interest_{category}_{question_num}'
                profile[field_name] = int(response)
    
    # Make sure all values are JSON serializable
    for key, value in profile.items():
        profile[key] = ensure_json_serializable(value)
    
    return profile


def generate_recommendations(student_profile, language='en'):
    """
    Generate university field recommendations based on student profile
    
    Args:
        student_profile (dict): Student profile data
        language (str): Language code ('en' or 'ar')
        
    Returns:
        dict: Recommendations data
    """
    try:
        # Convert to DataFrame (model expects DataFrame input)
        profile_df = pd.DataFrame([student_profile])
        
        # Verify the model is initialized correctly and has necessary components
        if not hasattr(recommendation_model, 'feature_processor') or recommendation_model.feature_processor is None:
            logger.error("Model not properly initialized - feature_processor is missing")
            return {"recommendations": [], "error": "Model not trained yet. Train the model first."}
        
        # Get recommendations from model
        try:
            logger.info(f"Calling recommendation_model.predict with profile data (language: {language})")
            recommendations = recommendation_model.predict(profile_df, language)
            logger.info(f"Raw recommendations from model: {recommendations}")
            
            # Handle different formats of recommendations
            if isinstance(recommendations, dict):
                # Already in the expected format
                if 'error' in recommendations:
                    logger.error(f"Model returned error: {recommendations['error']}")
                    return {"recommendations": [], "error": recommendations['error']}
                
                # Ensure recommendations has the expected structure
                if 'recommendations' in recommendations:
                    logger.info(f"Found 'recommendations' key in dict with {len(recommendations['recommendations'])} items")
                    
                    # Fix the nested structure issue - this is the key fix
                    processed_recommendations = []
                    for rec in recommendations['recommendations']:
                        # Create a new recommendation object with the correct structure
                        processed_rec = rec.copy() if isinstance(rec, dict) else {"field": "unknown", "field_name": "Unknown"}
                        
                        # Ensure all required fields exist
                        if 'score' not in processed_rec:
                            logger.warning(f"Recommendation missing 'score' field: {processed_rec}")
                            processed_rec['score'] = 0.5  # Default score
                        
                        # Add match_strength based on score
                        if 'match_strength' not in processed_rec:
                            score = processed_rec['score']
                            if score >= 0.85:
                                processed_rec['match_strength'] = "Excellent"
                            elif score >= 0.7:
                                processed_rec['match_strength'] = "Strong"
                            elif score >= 0.55:
                                processed_rec['match_strength'] = "Good"
                            elif score >= 0.4:
                                processed_rec['match_strength'] = "Moderate"
                            else:
                                processed_rec['match_strength'] = "Fair"
                        
                        # Ensure other required fields exist
                        if 'field' not in processed_rec:
                            processed_rec['field'] = "unknown"
                        if 'field_name' not in processed_rec:
                            processed_rec['field_name'] = "Unknown"
                        if 'field_name_ar' not in processed_rec:
                            processed_rec['field_name_ar'] = "غير معروف"
                        if 'subfields' not in processed_rec:
                            processed_rec['subfields'] = []
                        if 'reasons' not in processed_rec:
                            processed_rec['reasons'] = []
                        if 'admission_probability' not in processed_rec:
                            processed_rec['admission_probability'] = 0.5
                            
                        processed_recommendations.append(processed_rec)
                    
                    # Replace the recommendations with our processed ones
                    recommendations['recommendations'] = processed_recommendations
                    logger.info(f"Processed recommendations: {recommendations}")
                    return recommendations
                else:
                    logger.error("Recommendations dict missing 'recommendations' key")
                    return {"recommendations": [], "error": "Invalid recommendation format from model"}
            elif isinstance(recommendations, list):
                # Convert to the expected format
                if len(recommendations) > 0:
                    logger.info(f"Recommendations is a list with {len(recommendations)} items")
                    
                    # Process each recommendation
                    processed_recommendations = []
                    for rec in recommendations:
                        # Create a new recommendation object with the correct structure
                        processed_rec = rec.copy() if isinstance(rec, dict) else {"field": "unknown", "field_name": "Unknown"}
                        
                        # Ensure all required fields exist
                        if 'score' not in processed_rec:
                            logger.warning(f"Recommendation missing 'score' field: {processed_rec}")
                            processed_rec['score'] = 0.5  # Default score
                        
                        # Add match_strength based on score
                        if 'match_strength' not in processed_rec:
                            score = processed_rec['score']
                            if score >= 0.85:
                                processed_rec['match_strength'] = "Excellent"
                            elif score >= 0.7:
                                processed_rec['match_strength'] = "Strong"
                            elif score >= 0.55:
                                processed_rec['match_strength'] = "Good"
                            elif score >= 0.4:
                                processed_rec['match_strength'] = "Moderate"
                            else:
                                processed_rec['match_strength'] = "Fair"
                        
                        # Ensure other required fields exist
                        if 'field' not in processed_rec:
                            processed_rec['field'] = "unknown"
                        if 'field_name' not in processed_rec:
                            processed_rec['field_name'] = "Unknown"
                        if 'field_name_ar' not in processed_rec:
                            processed_rec['field_name_ar'] = "غير معروف"
                        if 'subfields' not in processed_rec:
                            processed_rec['subfields'] = []
                        if 'reasons' not in processed_rec:
                            processed_rec['reasons'] = []
                        if 'admission_probability' not in processed_rec:
                            processed_rec['admission_probability'] = 0.5
                            
                        processed_recommendations.append(processed_rec)
                    
                    # Check if this is a nested structure and extract the inner recommendations if needed
                    if len(processed_recommendations) == 1 and 'recommendations' in processed_recommendations[0]:
                        # Extract the nested recommendations
                        inner_recommendations = processed_recommendations[0]['recommendations']
                        academic_eligibility = processed_recommendations[0].get('academic_eligibility', {})
                        all_scores = processed_recommendations[0].get('all_scores', {})
                        result = {
                            "recommendations": inner_recommendations,
                            "academic_eligibility": academic_eligibility,
                            "all_scores": all_scores
                        }
                    else:
                        result = {"recommendations": processed_recommendations}
                    
                    logger.info(f"Processed list recommendations: {result}")
                    return result
                else:
                    logger.error(f"Recommendations list is empty")
                    return {"recommendations": [], "error": "No recommendations generated"}
            else:
                logger.error(f"Unexpected recommendation type: {type(recommendations)}")
                return {"recommendations": [], "error": "Invalid recommendation format from model"}
                
        except Exception as e:
            logger.error(f"Error during model prediction: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"recommendations": [], "error": str(e)}
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {"recommendations": [], "error": str(e)}


def main():
    """Run the Flask application"""
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
