from weaviate import Client
import weaviate
import weaviate.classes as wvc
import os
import requests
import json
 

class VectorDatabase:
    def __init__(self):
        self.client = Client("http://localhost:8080")
    
    def index_data(self, data):
        # Code to index data in Weaviate
        pass
    
    def query(self, prompt):
        # Code to query Weaviate with the prompt
        search_results = self.client.query.get('Article', ['content']).with_near_text({'concepts': [prompt]}).do()
        return search_results

url = "https://my-sandbox-21z4t676.weaviate.network"
weaviate_key = "u3NS3dy7eAmjy1o3ZGZ2TelgRuW8PM1q3ovA"


client = weaviate.connect_to_wcs(
    cluster_url=os.getenv(url),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv(weaviate_key)),
    headers={
        "X-OpenAI-Api-Key": os.environ["sk-proj-cfWWcTPGJ2jrxcejQltgT3BlbkFJnOtyUkYYNoMoqIhJiqbD"]
    }
)

try:
    # Replace with your code
    pass
finally:
    # Close the client gracefully
    client.close()
    