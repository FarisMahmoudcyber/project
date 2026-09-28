# Port Management & Monitoring System - Web Interface

Owner: Fares. Status: Week 2 complete (Week 1 skeleton + Week 2 scan results page).

## Run it

```bash
# 1. (once) create a virtual environment
python -m venv venv

# 2. activate it
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / macOS

# 3. (once) install Flask
pip install -r requirements.txt

# 4. start the website
python app.py
```

Open http://127.0.0.1:5000 in your browser. Stop the server with `Ctrl + C`.

## Project structure

```
port-monitor/
├── app.py               Flask app + routes
├── mock_data.py          Week 2: fake scan data (stands in for scanner.py/monitor.py)
├── requirements.txt      Python packages needed
├── README.md             this file
├── .gitignore            files Git should ignore
├── templates/             HTML pages (Jinja2)
│   ├── base.html          shared layout: menu, page frame, messages
│   ├── index.html         dashboard / home
│   ├── scan.html          new scan form
│   ├── results.html       Week 2: scan results page (ports table)
│   ├── history.html       scan history table, links to results
│   ├── alerts.html        New / Closed / Unchanged alerts
│   ├── about.html         project info
│   └── 404.html           page not found
└── static/
    └── css/style.css      all styling
```

Coming from teammates (same folder): `scanner.py` (Firas), `database.py` and `monitor.py` (Rayan).
`mock_data.py` will be deleted once those are connected in Week 4-5.

## Routes

| URL               | Methods   | Page                              |
|--------------------|-----------|------------------------------------|
| `/`                | GET       | Dashboard                          |
| `/scan`            | GET, POST | New scan form                      |
| `/results`         | GET       | Results of the scan just submitted (or a sample) |
| `/results/<id>`    | GET       | Results of one scan from history   |
| `/history`         | GET       | Scan history (mock data, Week 2)   |
| `/alerts`          | GET       | Alerts                             |
| `/about`           | GET       | About                              |

## How the mock scan works (Week 2)

Submitting the form on `/scan` does not run a real scan yet. It builds a
result from `mock_data.PORT_TEMPLATE`, stamps it with the typed target and
the current time, stores it in the browser session, and redirects to
`/results`. `/history` lists a few fixed sample scans from
`mock_data.MOCK_HISTORY`; clicking "View" opens `/results/<id>` for that
scan. This lets the whole results/history flow be reviewed and tested
before `scanner.py` and `database.py` exist.

## Git (suggested)

```bash
git checkout -b feature/web-interface
git add .
git commit -m "Week 2: scan results page with mock data"
git push -u origin feature/web-interface
```

## Before the final demo

- Set `debug=False` in `app.py` (the debug mode can run code in the browser).
- Set a real `SECRET_KEY` environment variable.
- Delete `mock_data.py` and the mock-data code paths once scanner.py/database.py are connected.
