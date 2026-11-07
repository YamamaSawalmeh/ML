# 🎓 Masarak (مسارك) – AI University & Major Recommendation System

Masarak helps high-school graduates choose the right university and major. The student uploads a photo of their Tawjihi certificate (or enters grades manually), completes a short interest assessment, and a machine-learning model recommends the best-fit universities and majors.

## Features

- **Diploma OCR** – reads grades straight from a photo of the certificate (EasyOCR / Tesseract + OpenCV, with Arabic support)
- **Interest assessment** – a questionnaire that profiles the student's interests
- **ML recommendations** – scikit-learn model trained on university data
- **University data collection** – scraper for programs and admission requirements
- **Bilingual web app** – Flask + Flask-Babel (Arabic / English) with a REST API

## Tech stack

Python · Flask · scikit-learn · pandas · NumPy · EasyOCR · Tesseract · OpenCV · PyArabic · Google Gemini API

## Project structure

```
Masarak/
├── run.py              # ML pipeline: scrape → generate data → train → scan diploma
├── run_web_app.py      # start the web app
├── src/
│   ├── data_collection/  university_scraper.py
│   ├── data_processing/  data_generator.py
│   ├── ml_models/        recommendation_model.py
│   ├── ocr_module/       diploma_scanner.py
│   └── utils/            interest_assessment.py
└── web_app/            # Flask app, templates, static files
```

## Run

```bash
cd Masarak
pip install -r requirements.txt
python run_web_app.py
```

Main routes: `/upload_diploma`, `/manual_entry`, `/interest_assessment`, `/recommendations`, plus JSON APIs under `/api/`.

> **Gemini API key:** set it as an environment variable before running – `export GEMINI_API_KEY=your-key` (or `set GEMINI_API_KEY=your-key` on Windows).
