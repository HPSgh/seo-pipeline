import sqlite3
import pandas as pd

def run_reports(db_name="gsc_data.db"):    
    conn = sqlite3.connect(db_name)

    print("\n=== Report 1: All Data ===")
    df_all = pd.read_sql_query(
        "SELECT * FROM gsc_data",
        conn
    )
    print(df_all)

    print("\n=== Report 2: Top Queries by Impressions ===")
    df_top_queries = pd.read_sql_query(
        """
        SELECT query, impressions, clicks, ctr_percent, position 
        FROM gsc_data 
        ORDER BY impressions DESC
        """,
        conn
    )
    print(df_top_queries)

    print("\n=== Report 3: Page Summary ===")
    df_page_summary = pd.read_sql_query(
        """
        SELECT page, SUM(clicks) as total_clicks, 
               SUM(impressions) as total_impressions,
               ROUND(AVG(position), 2) as avg_position
        FROM gsc_data 
        GROUP BY page
        """,
        conn
    )
    print(df_page_summary)
    conn.close()

    return df_all, df_top_queries, df_page_summary

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    run_reports()