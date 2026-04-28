import sqlite3
import pandas as pd
import webbrowser
import json
import os

def generate_dashboard(db_name="gsc_data.db"):
    try:
        conn = sqlite3.connect(db_name)

        df_summary = pd.read_sql_query("""
            SELECT
                SUM(clicks) as total_clicks,
                SUM(impressions) as total_impressions,
                ROUND(AVG(position), 2) as avg_position,
                COUNT(DISTINCT query) as total_queries
            FROM gsc_data
        """, conn)

        df_queries = pd.read_sql_query("""
            SELECT query, clicks, impressions, ctr_percent, ROUND(position, 2) as position
            FROM gsc_data
            ORDER BY impressions DESC
        """, conn)

        df_pages = pd.read_sql_query("""
            SELECT page,
                   SUM(clicks) as total_clicks,
                   SUM(impressions) as total_impressions,
                   ROUND(AVG(position), 2) as avg_position
            FROM gsc_data
            GROUP BY page
            ORDER BY total_impressions DESC
        """, conn)

        conn.close()

        summary = df_summary.to_dict(orient='records')[0]
        queries_data = df_queries.to_dict(orient='records')
        pages_data = df_pages.to_dict(orient='records')

        query_labels = json.dumps([r['query'] for r in queries_data])
        query_impressions = json.dumps([r['impressions'] for r in queries_data])
        query_clicks = json.dumps([r['clicks'] for r in queries_data])

        def query_rows(data):
            rows = ""
            for r in data:
                rows += f"""
                <tr>
                    <td class="col-query">{r['query']}</td>
                    <td>{int(r['clicks'])}</td>
                    <td>{int(r['impressions'])}</td>
                    <td>{r['ctr_percent']}%</td>
                    <td>{r['position']}</td>
                </tr>"""
            return rows

        def page_rows(data):
            rows = ""
            for r in data:
                rows += f"""
                <tr>
                    <td class="col-query">{r['page']}</td>
                    <td>{int(r['total_clicks'])}</td>
                    <td>{int(r['total_impressions'])}</td>
                    <td>{r['avg_position']}</td>
                </tr>"""
            return rows

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO Analytics Dashboard</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

  :root {{
    --bg-base: #0e0f11;
    --bg-surface: #16181c;
    --bg-raised: #1e2127;
    --bg-hover: #252830;
    --border: rgba(255,255,255,0.07);
    --border-strong: rgba(255,255,255,0.13);
    --text-primary: #e8eaf0;
    --text-secondary: #8b8f9a;
    --text-muted: #555a66;
    --accent-teal: #00c2a8;
    --accent-blue: #4d8ef0;
    --accent-amber: #f0a23c;
    --accent-red: #e05c5c;
    --font-sans: 'IBM Plex Sans', sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: var(--bg-base);
    color: var(--text-primary);
    font-family: var(--font-sans);
    font-size: 14px;
    line-height: 1.6;
    min-height: 100vh;
  }}

  .topbar {{
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border);
    padding: 0 32px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .topbar-brand {{
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 500;
    color: var(--accent-teal);
    letter-spacing: 0.04em;
  }}

  .topbar-meta {{
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
  }}

  .main {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 32px 24px;
  }}

  .section-label {{
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 16px;
  }}

  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 36px;
  }}

  .stat-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px 20px 16px;
  }}

  .stat-label {{
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
  }}

  .stat-value {{
    font-family: var(--font-mono);
    font-size: 28px;
    font-weight: 500;
    color: var(--text-primary);
    line-height: 1;
  }}

  .stat-value.teal {{ color: var(--accent-teal); }}
  .stat-value.blue {{ color: var(--accent-blue); }}
  .stat-value.amber {{ color: var(--accent-amber); }}

  .card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 24px;
  }}

  .card-header {{
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .card-title {{
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
  }}

  .chart-wrap {{
    padding: 20px;
    position: relative;
    height: 240px;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
  }}

  thead tr {{
    background: var(--bg-raised);
  }}

  th {{
    padding: 10px 16px;
    text-align: left;
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }}

  td {{
    padding: 11px 16px;
    font-size: 13px;
    border-bottom: 1px solid var(--border);
    color: var(--text-secondary);
    vertical-align: middle;
  }}

  td.col-query {{
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-primary);
    max-width: 300px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}

  tbody tr:last-child td {{ border-bottom: none; }}
  tbody tr:hover td {{ background: var(--bg-hover); }}

  .badge {{
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 4px;
    background: rgba(0,194,168,0.1);
    color: var(--accent-teal);
    border: 1px solid rgba(0,194,168,0.2);
  }}

  .footer {{
    text-align: center;
    padding: 32px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
  }}
</style>
</head>
<body>

<div class="topbar">
  <span class="topbar-brand">seo-pipeline / dashboard</span>
  <span class="topbar-meta">hpsgh.github.io &mdash; live data</span>
</div>

<div class="main">

  <p class="section-label">Overview</p>
  <div class="stat-grid">
    <div class="stat-card">
      <div class="stat-label">Total Impressions</div>
      <div class="stat-value teal">{int(summary['total_impressions'])}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Total Clicks</div>
      <div class="stat-value blue">{int(summary['total_clicks'])}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Avg Position</div>
      <div class="stat-value amber">{summary['avg_position']}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Unique Queries</div>
      <div class="stat-value">{int(summary['total_queries'])}</div>
    </div>
  </div>

  <div class="card">
    <div class="card-header">
      <span class="card-title">Impressions by query</span>
      <span class="badge">last 90 days</span>
    </div>
    <div class="chart-wrap">
      <canvas id="queryChart" role="img" aria-label="Bar chart showing impressions per search query"></canvas>
    </div>
  </div>

  <div class="card">
    <div class="card-header">
      <span class="card-title">Query breakdown</span>
    </div>
    <table>
      <thead>
        <tr>
          <th>Query</th>
          <th>Clicks</th>
          <th>Impressions</th>
          <th>CTR</th>
          <th>Position</th>
        </tr>
      </thead>
      <tbody>
        {query_rows(queries_data)}
      </tbody>
    </table>
  </div>

  <div class="card">
    <div class="card-header">
      <span class="card-title">Pages</span>
    </div>
    <table>
      <thead>
        <tr>
          <th>Page</th>
          <th>Clicks</th>
          <th>Impressions</th>
          <th>Avg Position</th>
        </tr>
      </thead>
      <tbody>
        {page_rows(pages_data)}
      </tbody>
    </table>
  </div>

</div>

<div class="footer">generated by seo-pipeline &mdash; python main.py &amp;&amp; python dashboard.py</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
  const labels = {query_labels};
  const impressions = {query_impressions};
  const clicks = {query_clicks};

  new Chart(document.getElementById('queryChart'), {{
    type: 'bar',
    data: {{
      labels: labels,
      datasets: [
        {{
          label: 'Impressions',
          data: impressions,
          backgroundColor: 'rgba(0, 194, 168, 0.2)',
          borderColor: 'rgba(0, 194, 168, 0.8)',
          borderWidth: 1.5,
          borderRadius: 4,
        }},
        {{
          label: 'Clicks',
          data: clicks,
          backgroundColor: 'rgba(77, 142, 240, 0.2)',
          borderColor: 'rgba(77, 142, 240, 0.8)',
          borderWidth: 1.5,
          borderRadius: 4,
        }}
      ]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{ display: false }},
      }},
      scales: {{
        x: {{
          ticks: {{ color: '#555a66', font: {{ family: 'IBM Plex Mono', size: 11 }} }},
          grid: {{ color: 'rgba(255,255,255,0.04)' }},
          border: {{ color: 'rgba(255,255,255,0.07)' }}
        }},
        y: {{
          ticks: {{ color: '#555a66', font: {{ family: 'IBM Plex Mono', size: 11 }}, stepSize: 1 }},
          grid: {{ color: 'rgba(255,255,255,0.04)' }},
          border: {{ color: 'rgba(255,255,255,0.07)' }}
        }}
      }}
    }}
  }});
</script>
</body>
</html>"""

        with open("dashboard.html", "w", encoding="utf-8") as f:
            f.write(html)

        print("Dashboard generated: dashboard.html")
        webbrowser.open('file:///' + os.path.abspath("dashboard.html").replace("\\", "/"))

    except FileNotFoundError:
        print("Error: gsc_data.db not found. Run main.py first.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_dashboard()