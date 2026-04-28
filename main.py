from auth import get_credentials
from extract import fetch_gsc_data
from transform import transform_data
from load import load_data_to_db

def main():
    try:
        # Step 1: Authenticate and get credentials
        print("Authenticating and getting credentials...")
        credentials = get_credentials()

        # Step 2: Extract data from Google Search Console
        print("Extracting data from Google Search Console...")
        raw_data = fetch_gsc_data()

        # Step 3: Transform the data
        print("Transforming data...")
        transformed_data = transform_data()

        # Step 4: Load the data into a database
        print("Loading data into database...")
        load_data_to_db(transformed_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()