# 🎓 Masarak (مسارك) – AI University Major Recommendation System

**Machine Learning final project – An-Najah National University (2025)**

Masarak helps Palestinian high-school (Tawjihi) graduates choose a university major. A student uploads their Tawjihi certificate (or enters grades manually), answers a 37-question interest assessment, and an ensemble of ML models recommends the best-fit majors, filtered by academic eligibility and explained in Arabic or English.

📄 **Full report:** [`docs/report.pdf`](docs/report.pdf)

## How it works

```
 Tawjihi certificate ──► OCR (EasyOCR / Tesseract / Gemini) ──┐
 or manual grade entry ───────────────────────────────────────┤
                                                               ├─► feature engineering ─► ML ensemble ─► eligibility filter ─► ranked majors + reasons
 37-question interest assessment ─────────────────────────────┘
```

1. **Data preparation** – cleans the student dataset and encodes the questionnaire answers (`src/data_processing/data_preparation.py`)
2. **Feature engineering** – academic, eligibility and interest features, including weighted MCQ options (`feature_engineering.py`)
3. **Model training** – Random Forest, Gradient Boosting and Logistic Regression, combined in a weighted ensemble (`src/ml_models/model_training.py`)
4. **Recommendation** – ranks majors, keeps only the ones the student is eligible for based on Tawjihi branch and grades, and generates an explanation for each one (`recommendation_ranked.py`, `recommendation_with_explanations.py`)
5. **Web app** – bilingual Flask interface (`src/web_app/`)

## Results (test set)

| Model | Accuracy | F1 (weighted) | Top-3 accuracy | Top-5 accuracy |
|-------|---------:|--------------:|---------------:|---------------:|
| Gradient Boosting | **73.4%** | **72.9%** | 80.9% | 85.9% |
| Random Forest | 72.0% | 70.0% | 81.7% | **86.2%** |
| Ensemble | 67.0% | 65.2% | **81.9%** | 85.3% |
| Logistic Regression | 58.8% | 58.0% | 76.3% | 83.5% |

Feature importances are in `src/outputs/` (`gb_feature_importances.csv`, `rf_feature_importances.csv`).

## Dataset

`src/data/raw/students_data.csv` – **synthetic** dataset of 6,300 Tawjihi students (branch, averages and 37 questionnaire answers) generated for this project.

## Tech stack

Python · scikit-learn · pandas · NumPy · Flask · Flask-Babel · EasyOCR · Tesseract · OpenCV · Google Gemini API · PyArabic

## Project structure

```
├── run.py                       # start the web app
├── config.py                    # settings and reference data
├── src/
│   ├── data/raw/                # synthetic student dataset, questions, university data
│   ├── data/processed/          # program metadata, questionnaire config, MCQ weights
│   ├── data_processing/         # data_preparation.py, feature_engineering.py
│   ├── ml_models/               # model_training.py, recommendation_*.py
│   ├── ocr_module/              # diploma_scanner.py
│   ├── utils/                   # interest_assessment.py
│   ├── outputs/                 # evaluation results and feature importances
│   └── web_app/                 # Flask app, templates, static files
└── docs/                        # report.pdf, RUN_STEPS.docx
```

## Run

```bash
pip install -r requirements.txt

# 1) build the dataset and train the models (creates src/models/*.pkl)
cd src/data_processing && python data_preparation.py && python feature_engineering.py && cd ../..
cd src/ml_models && python model_training.py && cd ../..

# 2) start the web app
export GEMINI_API_KEY=your-key      # optional, for certificate OCR (Windows: set GEMINI_API_KEY=...)
python run.py                        # http://localhost:5000
```

The trained models are not included because they are too large for GitHub (~1.6 GB); step 1 recreates them.

## Team

Machine Learning course – Group 2
