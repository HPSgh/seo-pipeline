import pandas as pd

def transform_data(response=None):
    if response is None or 'rows' not in response:
        print("No data returned from GSC yet.")
        return None
    
    records = []
    for row in response['rows']:
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
    
