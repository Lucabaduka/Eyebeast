import os
import sqlite3
import html
from datetime import datetime
from flask import Flask, render_template, request

version = "1.1.2"

app = Flask(__name__)

PATH = os.path.dirname(__file__)

# Errors
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# Main
@app.route("/", methods = ["POST", "GET"])
def gazer():


    # Pull the URL
    url_params = request.args
    region = url_params.get("region", None)

    # Direct request
    if region != None:
        region = region.lower().strip().replace(" ", "_")

    # Normal Eyebeast request
    elif request.form:
        name = request.form
        region = name['region'].replace("https://www.nationstates.net/region=", "").strip().lower()
        region = region.replace(" ", "_")

    # We have no idea what is happening
    else:
        return render_template("main.html")

    # The search data is garbage
    if region.replace("_", "").isalnum() is False:
        return render_template("404.html")

    # Connect to the database and search for the input
    data = []
    connect = sqlite3.connect(f"{PATH}/eyebeast.db")
    c = connect.cursor()
    c.execute("""SELECT * FROM eyebeast WHERE LOWER(REPLACE(region, ' ', '_')) = ? order by stamp desc;""", (region,))

    # Process results
    for x in c.fetchall():
        data.append(list(x))

    # The entry was not found
    if len(data) == 0:
        return render_template("404.html")

    # We assume we have results to deliver at this point
    stamps  = []
    regions = []
    wfes    = []
    tags    = []
    ros     = []
    flags   = []
    banners = []

    for count, value in enumerate(data):

        # Initialise hidden
        if count == 0:
            hide = ""
        else:
            hide = " inactive"

        # Load timestamps
        entry = ""
        entry = datetime.utcfromtimestamp(value[0]).strftime('%B %d, %Y')
        pstamp = f"""<p class="center stamps{hide}">Entry from {entry}</p>"""
        stamps.append(pstamp)

        # Load regions
        entry = ""
        entry = f"""<p class="title space is-2 regions{hide}" style="margin-bottom: 0rem;"><a class="gold" href="https://www.nationstates.net/region={value[1].lower().replace(' ', '_')}" target="_blank">{value[1]}</a></p>"""
        regions.append(entry)

        # Load WFEs
        entry = ""
        pwfe = html.unescape(value[2])
        entry = f"""<pre class="data-display wfes{hide}" style="font-size: 10pt;">{pwfe}</pre>"""
        wfes.append(entry)

        # Load tags
        entry = ""
        entry = f"""<pre class="data-display tags{hide}">{value[3]}</pre>"""
        tags.append(entry)

        # Load ROs
        entry = ""
        entry = f"""<pre class="data-display ros{hide}">{value[4]}</pre>"""
        ros.append(entry)

        # Load flags
        entry = ""
        if value[5] != "":
            pflag = f"""<a href="static/flags/{value[5]}" download><img src ="static/flags/{value[5]}"></a>"""
            entry = f"""<pre class="data-display flags{hide}">{pflag}</pre>"""
        else:
            entry = """<pre class="data-display flags"></pre>"""
        flags.append(entry)

        # Format banners
        entry = ""
        if value[6] == "":
            entry = f"""<pre class="data-display banners{hide}"></pre>"""
        elif len(value[6]) < 3:
            entry = f"""<pre class="data-display banners{hide}"><p class="gold" style="font-size: 10pt;">This is a stock banner. Select it in the region's admin menu.</p><img src ="https://www.nationstates.net/images/rbanners/{value[6]}"></pre>"""
        else:
            entry = f"""<pre class="data-display banners{hide}"><a href="static/banners/{value[6]}" download><img src ="static/banners/{value[6]}"></a></pre>"""
        banners.append(entry)

    # Initialise break buttons
    breaks = []

    if len(data) == 1:
        breaks.append("disabled")
    else:
        breaks.append("")

    if value[2] == "":
        breaks.append("disabled")
    else:
        breaks.append("")

    # Send the response
    return render_template("gazer.html",
    length    = len(data),
    breaks    = breaks,
    stamps    = stamps,
    regions   = regions,
    wfes      = wfes,
    tags      = tags,
    ros       = ros,
    flags     = flags,
    banners   = banners,
    )

    # Slep
    connect.close()

if __name__ == "__main__":
    app.run()