import sqlite3
import pandas as pd
from transform import transform_data

def load_data_to_db(df, db_name="gsc_data.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("gsc_data", conn, if_exists="replace", index=False)
    print(f"Data loaded into {db_name} successfully!")
    conn.close()

def query_db(db_name="gsc_data.db"):
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query("""
        SELECT page, 
           SUM(clicks) as total_clicks,
           SUM(impressions) as total_impressions,
           ROUND(AVG(position), 2) as avg_position
        FROM gsc_data
        GROUP BY page
        ORDER BY total_clicks DESC
    """, conn)
    
    conn.close()
    print(df)

if __name__ == "__main__":
    df = transform_data()
    load_data_to_db(df)
    query_db()