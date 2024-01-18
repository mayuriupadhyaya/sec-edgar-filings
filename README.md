# Importing financial data from SEC EDGAR database and storing it in MongoDB.

This Python script retrieves financial data from the U.S. Securities and Exchange Commission's EDGAR database using the XBRL-to-JSON Converter API and stores it in a MongoDB database.

## Prerequisites

Before running the script, make sure you have the following:

1. **API Key**: Obtain an API key from [SEC-API](https://sec-api.io/).
2. **MongoDB Atlas Account**: Set up a MongoDB Atlas account and create a cluster.

## Environment Variables

Set the following environment variables:

- `XBRL_API_KEY`: Your SEC-API key.
- `MONGO_USERNAME`: Your MongoDB Atlas username.
- `MONGO_PASSWORD`: Your MongoDB Atlas password.
- `MONGO_CLUSTER`: Your MongoDB Atlas cluster name.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mayuriupadhyaya/sec-edgar-filings.git
    cd sec-edgar-filings
    ```

2. Install dependencies:

    ```bash
    pip install pymongo requests
    ```

## Usage

Run the script using the following command:

```bash
python 10-K-filings.py
```

## Configuration

Adjust the following parameters in the script:

- `filing_url`: Replace with the actual filing URL or accession number.
- `api_endpoint`: The API endpoint for the XBRL-to-JSON Converter.
- `api_params`: The parameters to be passed to the API.

## Contributing

Feel free to contribute by submitting issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
