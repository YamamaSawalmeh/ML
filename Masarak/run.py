import sys
from src.data_collection.university_scraper import scrape_universities
from src.data_processing.data_generator import generate_data
from src.ml_models.recommendation_model import train_model
from src.ocr_module.diploma_scanner import scan_diploma

def main():
    # Step 1: Scrape university data
    print("Scraping university data...")
    university_data = scrape_universities()
    
    # Step 2: Generate data based on user input or scraped data
    print("Generating data...")
    generated_data = generate_data(university_data)
    
    # Step 3: Train the recommendation model
    print("Training recommendation model...")
    model = train_model(generated_data)
    
    # Step 4: Scan diploma for user information
    print("Scanning diploma...")
    diploma_info = scan_diploma()
    
    # Output results
    print("Process completed successfully.")
    print("Diploma Info:", diploma_info)
    print("Model trained and ready for use.")

if __name__ == "__main__":
    main()