import sqlite3
import html
from datetime import datetime
from flask import Flask, render_template, request

version = 1.0

app = Flask(__name__)

# Errors
@app.errorhandler(404)  
def not_found(e):
      return render_template("404.html")

# Main
@app.route("/", methods = ["POST", "GET"])
def gazer():

    # Reject the user if they travelled here directly
    if request.method != "POST":
        return render_template("main.html")
    
    # Process the search input
    name = request.form
    region = name['region'].replace("https://www.nationstates.net/region=", "").strip().lower()
    region = region.replace(" ", "_")

    # Trashy RCE thwarting
    junk = ["<script>", "</script>", "<div>", "</div>", "<pre>", "</pre>", "<p>", "</p>", 
            "<a ", "</a>", "href=", "src=", "<body>", "</body>", "<style>", "</style>"]
    for x in junk:
        region.replace(x, "")

    # The search data is garbage
    if region.replace("_", "").isalnum() is False:
        return render_template("404.html")

    # Connect to the database and search for the input
    data = []
    connect = sqlite3.connect("/var/www/eyebeast/eyebeast.db")
    c = connect.cursor()
    c.execute(f"SELECT * FROM eyebeast WHERE LOWER(REPLACE(region, ' ', '_')) = ? order by stamp desc;", (region,))

    # Process results
    for x in c.fetchall():
        data.append(list(x))

    # The entry was not found
    if len(data) == 0:
        return render_template("404.html")

    # We assume we have results to deliver at this point
    stamps = []
    regions = []
    wfes = []
    tags = []
    ros = []
    flags = []
    banners = []
    counter = 1

    for x in data:

        # Initialise hidden
        if counter == 1:
            hide = ""
        else:
            hide = " inactive"

        # Load timestamps
        entry = ""
        entry = datetime.utcfromtimestamp(x[0]).strftime('%B %d, %Y')
        pstamp = f"""<p class="center stamps{hide}">Entry from {entry}</p>
                                """
        stamps.append(pstamp)

        # Load regions
        entry = ""
        entry = f"""<p class="title space is-2 regions{hide}" style="margin-bottom: 0rem;">{x[1]}</p>
                                """
        regions.append(entry)

        # Load WFEs
        entry = ""
        pwfe = html.unescape(x[2])
        entry = f"""<pre class="data-display wfes{hide}" style="font-size: 10pt;">{pwfe}</pre>
                                    """
        wfes.append(entry)

        # Load tags
        entry = ""
        entry = f"""<pre class="data-display tags{hide}">{x[3]}</pre>
                                    """
        tags.append(entry)

        # Load ROs
        entry = ""
        entry = f"""<pre class="data-display ros{hide}">{x[4]}</pre>
                                    """
        ros.append(entry)

        # Load flags
        entry = ""
        if x[5] != "":
            pflag = f"""<a href="static/flags/{x[5]}" download><img src ="static/flags/{x[5]}"></a>"""
            entry = f"""<pre class="data-display flags{hide}">{pflag}</pre>
                                    """
        else:
            entry = ""
        flags.append(entry)

        # Format banners
        entry = ""
        if x[6] == "":
            entry = f"""<pre class="data-display banners{hide}"></pre>"""
        elif len(x[6]) < 3:
            entry = f"""<pre class="data-display banners{hide}"><p class="gold" style="font-size: 10pt;">This is a stock banner. Select it in the region's admin menu.</p><img src ="https://www.nationstates.net/images/rbanners/{x[6]}"></pre>"""
        else:
            entry = f"""<pre class="data-display banners{hide}"><a href="static/banners/{x[6]}" download><img src ="static/banners/{x[6]}"></a></pre>"""
        banners.append(entry)

        # Next
        counter += 1

    # Initialise break buttons
    breaks = []

    if len(data) == 1:
        breaks.append("disabled")
    else:
        breaks.append("")
    
    if x[2] == "":
        breaks.append("disabled")
    else:
        breaks.append("")

    # Send the response
    return render_template("gazer.html", 
    length = len(data),
    breaks=breaks,
    stamps=stamps,
    regions=regions,
    wfes=wfes,
    tags=tags,
    ros=ros,
    flags=flags,
    banners=banners,
    )

    # Slep
    connect.close()

if __name__ == "__main__":
    app.run()