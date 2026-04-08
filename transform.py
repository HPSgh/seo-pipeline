import pandas as pd

def transform_data():
    records = []
    mock_response = {
        "rows": [
            {
                "keys": ["example query 1", "https://hpsgh.github.io/page1"],
                "clicks": 100,
                "impressions": 1000,
                "ctr": 0.1,
                "position": 5
            },
            {
                "keys": ["example query 2", "https://hpsgh.github.io/page2"],
                "clicks": 50,
                "impressions": 500,
                "ctr": 0.1,
                "position": 10
            }
        ]
    }
    for row in mock_response['rows']:
        records.append({
            "query": row['keys'][0],
            "page": row['keys'][1],
            "clicks": row['clicks'],
            "impressions": row['impressions'],
            "ctr": row['ctr'],
            "position": row['position']
        })
    df = pd.DataFrame(records)
    df = df.fillna({'clicks': 0, 'impressions': 0, 'ctr': 0.0, 'position': 0.0})
    df['clicks'] = df['clicks'].astype(int)
    df['impressions'] = df['impressions'].astype(int)
    df['ctr'] = df['ctr'].astype(float)
    df['position'] = df['position'].astype(float)
    df['ctr_percent'] = (df['ctr'] * 100).round(2)
    pd.set_option('display.max_columns', None)
    return df
    print(df)
        
if __name__ == "__main__":
    transform_data()
    
