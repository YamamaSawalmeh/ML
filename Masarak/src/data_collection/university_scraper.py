import requests
from bs4 import BeautifulSoup

def scrape_university_data(url):
    """
    Scrapes university data from the given URL.

    Args:
        url (str): The URL of the university website to scrape.

    Returns:
        dict: A dictionary containing scraped university data.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example scraping logic (to be customized based on actual website structure)
    university_data = {
        'name': soup.find('h1').text.strip(),
        'location': soup.find('p', class_='location').text.strip(),
        'programs': [program.text.strip() for program in soup.find_all('li', class_='program')],
        'website': url
    }
    
    return university_data

def main():
    # Example usage
    url = "https://example-university.com"
    data = scrape_university_data(url)
    print(data)

if __name__ == "__main__":
    main()