#!/usr/bin/env python3
"""Site check: every page is reachable from the nav and tracked by Vercel Web Analytics.

Fails (exit 1) when:
  - a top-level *.html page lacks the Vercel Analytics snippet (the page would be invisible in the dashboard)
  - a page is neither in the NAV list in app.js nor in OFF_NAV below (it would be unreachable)
  - a NAV entry points at a file that does not exist
  - a page that should render the masthead is missing <header id="masthead"> or app.js

Runs on every push (.github/workflows/site-check.yml). Add a page to NAV in app.js (one list
drives both the desktop masthead and the phone tab bar) or, if it is deliberately off-nav,
to OFF_NAV here with the reason.

  python3 scripts/check_site.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF_NAV = {
    "team.html": "reached from team links on rankings and the recap",
    "feed.html": "parked for the offseason, still resolves",
    "scoreboard.html": "parked for the offseason, still resolves",
    "setup.html": "commissioner setup, linked from the demo banner",
}
ANALYTICS = "/_vercel/insights/script.js"


def main():
    app = open(os.path.join(ROOT, "app.js"), encoding="utf-8").read()
    block = re.search(r"const NAV = \[(.*?)\n  \];", app, re.S)
    nav = re.findall(r'\["([\w.-]+\.html)"', block.group(1)) if block else []
    problems = []
    if not nav:
        problems.append("app.js: could not find the NAV list")
    pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
    for page in pages:
        html = open(os.path.join(ROOT, page), encoding="utf-8").read()
        if ANALYTICS not in html:
            problems.append(f"{page}: no Vercel Analytics snippet (copy the two <script> lines from trades.html)")
        if page not in nav and page not in OFF_NAV:
            problems.append(f"{page}: not in NAV (app.js) and not listed in OFF_NAV")
        if page in nav and ('id="masthead"' not in html or "app.js" not in html):
            problems.append(f"{page}: in NAV but has no masthead or does not load app.js")
    for href in nav:
        if href not in pages:
            problems.append(f"NAV points at {href}, which does not exist")
    print(f"{len(pages)} pages, {len(nav)} in the nav, {len(OFF_NAV)} off-nav by design")
    for p in problems:
        print("FAIL", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
