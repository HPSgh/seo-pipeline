def fetch_gsc_data():
    try:
        from auth import get_credentials
        from googleapiclient.discovery import build
        creds = get_credentials()
        service = build('searchconsole', 'v1', credentials=creds)
        site_url = 'https://hpsgh.github.io/'
        request_body = {
            "startDate": "2026-01-01",
            "endDate": "2026-04-28",
            "dimensions": ["query", "page"],
            "rowLimit": 100
        }
        response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
        print("Data fetched successfully!")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    fetch_gsc_data()