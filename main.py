from auth import get_credentials
from extract import fetch_gsc_data
from transform import transform_data
from load import load_data_to_db

def main():
    try:
        print("Authenticating and getting credentials...")
        credentials = get_credentials()

        print("Extracting data from Google Search Console...")
        raw_data = fetch_gsc_data()

        print("Transforming data...")
        transformed_data = transform_data(raw_data)

        if transformed_data is None:
            print("Pipeline stopped: no data to load yet.")
            return

        print("Loading data into database...")
        load_data_to_db(transformed_data)
        print("Pipeline completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()