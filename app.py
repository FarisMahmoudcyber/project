"""
app.py - Web interface (Flask) for the Port Management & Monitoring System.

Week 1: built the skeleton of the website
  - created the Flask app
  - set up the routes (the "addresses" of each page)
  - built the basic HTML templates
  - created a clean project structure

Week 2 goal: design the scan results page and test it with mock data
  - added a Scan results page (/results) that shows a table of ports
  - the New scan form now "runs" a fake scan (mock_data.py) and shows
    the results, so the page can be reviewed before scanner.py exists
  - Scan history now lists a few fake past scans and links to their
    results page

Later weeks will plug in the other modules:
  scanner.py  (Firas)  -> runs the Nmap scan, replaces mock_data.py
  database.py (Rayan)  -> saves and loads scan history
  monitor.py  (Rayan)  -> compares scans and finds New / Closed ports
"""

import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for

from mock_data import MOCK_HISTORY, PORT_TEMPLATE, summarize

app = Flask(__name__)

# flask needs a secret key to use flash() messages safely.
# Read it from the environment; the fallback is for local development only.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")


# ---------------------------------------------------------------------------
# Data shared with the templates
# ---------------------------------------------------------------------------

# Menu items: (route function name, text shown in the menu)
NAV_ITEMS = [
    ("index", "Dashboard"),
    ("scan", "New scan"),
    ("history", "Scan history"),
    ("alerts", "Alerts"),
    ("about", "About"),
]

# The Scan results page is reached from "New scan" or "Scan history",
# not from the side menu, but it should still highlight "New scan"
# while the visitor is looking at a result.
RESULTS_ENDPOINTS = {"results", "result_detail"}

# Well-known ports shown on the home page.
# "risky" = dangerous when it is open to the whole network by mistake.
COMMON_PORTS = [
    {"number": 21, "service": "FTP", "risky": True},
    {"number": 22, "service": "SSH", "risky": False},
    {"number": 23, "service": "Telnet", "risky": True},
    {"number": 25, "service": "SMTP", "risky": False},
    {"number": 53, "service": "DNS", "risky": False},
    {"number": 80, "service": "HTTP", "risky": False},
    {"number": 443, "service": "HTTPS", "risky": False},
    {"number": 3389, "service": "RDP", "risky": True},
]

# Team modules and their status (taken from the project plan).
MODULES = [
    {"name": "Scanner", "file": "scanner.py", "owner": "Firas", "status": "In progress"},
    {"name": "Database", "file": "database.py", "owner": "Rayan", "status": "In progress"},
    {"name": "Web interface", "file": "app.py", "owner": "Fares", "status": "In progress"},
]


@app.context_processor
def inject_globals():
    """Make these values available in every template automatically."""
    active = "scan" if request.endpoint in RESULTS_ENDPOINTS else request.endpoint
    return {"nav_items": NAV_ITEMS, "active_page": active}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Home page / dashboard."""
    return render_template("index.html", ports=COMMON_PORTS, modules=MODULES)


@app.route("/scan", methods=["GET", "POST"])
def scan():
    """Scan page. GET shows the form, POST receives the target.

    Week 1: the form only checked that something was typed.
    Week 2: a POST now builds a *mock* result (mock_data.PORT_TEMPLATE)
            stamped with the typed target and the current time, and
            sends the visitor to the results page to review it.
    Week 4: this block will call scanner.py instead of using mock data.
    """
    if request.method == "POST":
        target = request.form.get("target", "").strip()
        if not target:
            flash("Enter an IP address or a range before starting a scan.", "error")
            return redirect(url_for("scan"))

        # Mock scan: real scanning is not connected yet (Week 4).
        session["last_scan"] = {
            "target": target,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ports": PORT_TEMPLATE,
        }
        flash(
            f"Showing a simulated result for {target}. "
            "The real scanner connects in Week 4.",
            "info",
        )
        return redirect(url_for("results"))
    return render_template("scan.html")


@app.route("/results")
def results():
    """Scan results page for the scan just launched from /scan.

    If no scan was launched yet in this browser session, a sample
    result is shown instead, so this page can be opened and reviewed
    on its own.
    """
    scan_data = session.get("last_scan")
    is_sample = scan_data is None
    if is_sample:
        scan_data = MOCK_HISTORY[0]
    return render_template(
        "results.html",
        scan=scan_data,
        summary=summarize(scan_data["ports"]),
        is_sample=is_sample,
    )


@app.route("/results/<int:scan_id>")
def result_detail(scan_id):
    """Results page for one specific scan from Scan history (mock data)."""
    scan_data = next((s for s in MOCK_HISTORY if s["id"] == scan_id), None)
    if scan_data is None:
        return render_template("404.html"), 404
    return render_template(
        "results.html",
        scan=scan_data,
        summary=summarize(scan_data["ports"]),
        is_sample=True,
    )


@app.route("/history")
def history():
    """List of past scans.

    Week 1: empty.
    Week 2: a few mock scans (mock_data.MOCK_HISTORY), each linking to
            its own results page.
    Week 4: real data, read from database.py.
    """
    scans = [{**s, "summary": summarize(s["ports"])} for s in MOCK_HISTORY]
    return render_template("history.html", scans=scans)


@app.route("/alerts")
def alerts():
    """Alerts about New and Closed ports. Built for real in Week 5."""
    alert_list = []  # will come from monitor.py
    return render_template("alerts.html", alerts=alert_list)


@app.route("/about")
def about():
    """Short description of the project and the tools used."""
    return render_template("about.html", modules=MODULES)


@app.errorhandler(404)
def page_not_found(error):
    """Friendly page when the address does not exist."""
    return render_template("404.html"), 404


# ---------------------------------------------------------------------------
# Run the development server:  python app.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # debug=True is handy while building (auto-reload + error details),
    # but turn it OFF before the final demo: the debugger can run code.
    app.run(host="127.0.0.1", port=5000, debug=True)
