# Masarak Web Application

## Overview
Masaraq is a machine learning-based university recommendation system designed to assist users in finding suitable universities based on their qualifications and interests. The web application is built using Flask and provides a user-friendly interface for data input and displaying recommendations.

## Project Structure
The project is organized into several directories and files, each serving a specific purpose:

- **run.py**: Main entry point for the machine learning recommendation system.
- **run_web_app.py**: Main entry point for launching the Flask web application.
- **config.py**: Configuration settings for paths, parameters, and constants.
- **requirements.txt**: Lists dependencies required for the project.

### Data Directory
- **data/uploads**: Stores uploaded files such as diplomas or user data.
- **data/models**: Contains trained machine learning models.
- **data/generated**: Stores generated data like recommendations or processed outputs.
- **data/raw**: Contains raw data collected from various sources.
- **data/processed**: Stores processed data that has been cleaned and transformed.

### Source Code Directory
- **src/ocr_module**: Contains the OCR module for scanning diplomas.
- **src/ml_models**: Contains machine learning models for recommendations.
- **src/utils**: Contains utility functions and classes.
- **src/data_processing**: Contains scripts for data processing.
- **src/data_collection**: Contains scripts for collecting data from external sources.

### Web Application Directory
- **web_app**: Contains all files related to the web application.
  - **templates**: HTML templates for rendering web pages.
  - **static**: Static files such as CSS and JavaScript.
  
## Getting Started
To get started with the Masaraq project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`.
3. Configure any necessary settings in `config.py`.
4. Run the web application using `run_web_app.py`.

## Usage
Users can upload their diplomas, enter their demographics, and assess their interests through the web interface. The system will then provide personalized university recommendations based on the input data.

## Contributing
Contributions to the Masaraq project are welcome. Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.