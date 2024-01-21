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
        "mongodb+srv://mongo_username:mongo_password@mongo_cluster?retryWrites=true&w=majority"
    )

    # return a friendly error if a URI error is thrown
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

try:
    db = client.edgar  # Use a database named "edgar"
    filings_collection = db["filings"]  # Use a collection named "filings"

    # Build the API request URL for Query API
    query_api_endpoint = "https://api.sec-api.io?token=api_key"
    query_api_params = {
        "query": {
            "query_string": {
                "query": "formType:\"10-K\" AND documentFormatFiles.type:\"EX-21\""
            }
        },
        "from": "0",
        "size": "100",
        "sort": [{"filedAt": {"order": "desc"}}],
    }
    query_response = requests.post(query_api_endpoint, json=query_api_params)

    # Check if the Query API call was successful
    if query_response.status_code == 200:
        query_data = query_response.json()

        # Iterate over the results and use XBRL-to-JSON Converter API
        for filing in query_data.get("filings", []):
            filing_url = filing.get("linkToFilingDetails")

            if filing_url:
                # Build the API request URL for XBRL-to-JSON Converter
                xbrl_api_endpoint = "https://api.sec-api.io/xbrl-to-json"
                xbrl_api_params = {"htm-url": filing_url, "token": api_key}
                xbrl_response = requests.get(xbrl_api_endpoint, params=xbrl_api_params)

                if xbrl_response.status_code == 200:
                    xbrl_data = xbrl_response.json()

                    # Store the data in MongoDB
                    result = filings_collection.insert_one(xbrl_data)

                    # Print the inserted document ID
                    print("Inserted document ID:", result.inserted_id)
                else:
                    print(
                        f"Failed to fetch data from XBRL-to-JSON Converter API. Status code: {xbrl_response.status_code}"
                    )

    else:
        print(
            f"Failed to fetch data from Query API. Status code: {query_response.status_code}"
        )

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the MongoDB client connection
    client.close()