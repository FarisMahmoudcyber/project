"""
mock_data.py - Fake scan data for Week 2.

Week 2 goal: design the Scan Results page and test it with mock JSON,
before the real scanner (scanner.py, Firas) and monitoring engine
(monitor.py, Rayan) exist.

This file stands in for both of them. The keys used in each dictionary
below are the shape we plan to ask Firas and Rayan to match once we
connect the real modules in Week 4-5. Using the same shape now means
the templates built this week will not need to change later - only
this file gets deleted and replaced with real data.

port dictionary:
    number  - port number, e.g. 22
    service - service name, e.g. "SSH"
    state   - "open" or "closed" (what the scanner found)
    status  - "new"       port was closed last scan, open now
              "closed"    port was open last scan, closed now
              "unchanged" same as last scan
              (this field is what monitor.py will calculate for real)
"""

# A sample scan result, used as the mock result of the "Start scan" form.
PORT_TEMPLATE = [
    {"number": 21, "service": "FTP", "state": "open", "status": "new"},
    {"number": 22, "service": "SSH", "state": "open", "status": "unchanged"},
    {"number": 80, "service": "HTTP", "state": "open", "status": "unchanged"},
    {"number": 443, "service": "HTTPS", "state": "open", "status": "unchanged"},
    {"number": 3389, "service": "RDP", "state": "closed", "status": "closed"},
]

# A handful of past scans, used by the Scan history page (/history).
# Each one can be opened on its own results page (/results/<id>).
MOCK_HISTORY = [
    {
        "id": 3,
        "target": "192.168.1.10",
        "time": "2026-09-25 14:02",
        "ports": PORT_TEMPLATE,
    },
    {
        "id": 2,
        "target": "192.168.1.10",
        "time": "2026-09-24 09:41",
        "ports": [
            {"number": 22, "service": "SSH", "state": "open", "status": "unchanged"},
            {"number": 80, "service": "HTTP", "state": "open", "status": "unchanged"},
            {"number": 443, "service": "HTTPS", "state": "open", "status": "unchanged"},
            {"number": 3389, "service": "RDP", "state": "open", "status": "unchanged"},
        ],
    },
    {
        "id": 1,
        "target": "10.0.0.5",
        "time": "2026-09-23 18:15",
        "ports": [
            {"number": 22, "service": "SSH", "state": "open", "status": "unchanged"},
            {"number": 80, "service": "HTTP", "state": "open", "status": "unchanged"},
        ],
    },
]


def summarize(ports):
    """Count ports by status and how many are open.

    Used on results.html and history.html so the page does not need
    to loop over the port list twice.
    """
    counts = {"new": 0, "closed": 0, "unchanged": 0}
    open_count = 0
    for port in ports:
        counts[port["status"]] += 1
        if port["state"] == "open":
            open_count += 1
    return {"open": open_count, **counts}
