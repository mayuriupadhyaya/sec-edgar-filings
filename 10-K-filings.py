import pymongo
import requests
import sys
import os

# Load environment variables
api_key = os.getenv("XBRL_API_KEY")
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_cluster = os.getenv("MONGO_CLUSTER")

# Replace the placeholder data with your Atlas connection string. Be sure it includes
# a valid username and password! Note that in a production environment,
# you should not store your password in plain-text here.

# Check if any of the required environment variables are missing
if not (api_key and mongo_username and mongo_password and mongo_cluster):
    print("Please set the environment variables: XBRL_API_KEY, MONGO_USERNAME, MONGO_PASSWORD, MONGO_CLUSTER")
    sys.exit(1)

try:
  client = pymongo.MongoClient(
  "mongodb+srv://<mongo_username>:<mongo_password>@<mongo_cluster>?retryWrites=true&w=majority")
  
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

try:
    db = client.edgar  # Use a database named "edgar"
    filings_collection = db["filings"]  # Use a collection named "filings"

    # Replace with the actual filing URL or accession number
    filing_url = "https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm"
    # Example using accession number: filing_accession = "0001564590-21-004599"

    # Build the API request URL
    api_endpoint = "https://api.sec-api.io/xbrl-to-json"
    api_params = {"htm-url": filing_url, "token": api_key}
    response = requests.get(api_endpoint, params=api_params)

    # Check if the API call was successful
    if response.status_code == 200:
        data = response.json()

        # Store the data in MongoDB
        result = filings_collection.insert_one(data)

        # Print the inserted document ID
        print("Inserted document ID:", result.inserted_id)

    else:
        print(f"Failed to fetch data from XBRL-to-JSON Converter API. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the MongoDB client connection
    client.close()
