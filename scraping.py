from bs4 import BeautifulSoup
import requests
import weaviate

# The main URL you want to scrape
main_url = 'https://u.ae/en/information-and-services'

# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract data here
    data = soup.find_all('div', class_='home-service')
    return data

# Function to store data in your vector database
def store_data(data):
    # Assuming you have already connected to Weaviate (client is available)
    # and have a class called "Service" with properties like "name", "description", etc.

    for item in data:
        # Extract relevant information from the scraped data
        name = item.get("name")
        description = item.get("description")

        # Create an object (entity) in Weaviate
        weaviate_object = {
            "class": "Service",
            "properties": {
                "name": name,
                "description": description
                # Add other properties as needed
            }
        }



# Start by scraping the main page
main_data = scrape_page(main_url)
store_data(main_data)

# for the subpages
subpages = ['https://u.ae/en/information-and-services/visa-and-emirates-id', 'https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas', 'https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa']  # Add your subpage URLs here
for page in subpages:
    subpage_data = scrape_page(page)
    store_data(subpage_data)

