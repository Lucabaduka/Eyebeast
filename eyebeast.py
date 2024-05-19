import os
import html
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, abort, send_from_directory

VERSION = "1.3.0"
PATH    = os.path.dirname(__file__)
app     = Flask(__name__)

#######################################
# ---           Errors            --- #
#######################################

# 404
@app.errorhandler(404)
def error_404(e):

    title    = "404: Not Found"
    subtitle = "Region is unknown or cannot be known"
    text     = """No record was found within the database for the region you mentioned. Try searching for something else."""

    return render_template("page.html",
    title    = title,
    subtitle = subtitle,
    text     = text
    )

# 500
@app.errorhandler(500)
def error_500(e):

    title    = "500: Internal Server Error"
    subtitle = "The server's brain has exploded"
    text     = """Something about your last interaction triggered a fault in the Eyebeast software or in the server's
    configuration. If it keeps happening, feel free to report it to Refuge administration."""

    return render_template("page.html",
    title    = title,
    subtitle = subtitle,
    text     = text
    )

#######################################
# ---        Main  Routing        --- #
#######################################

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

    # Operator is arriving
    else:
        return render_template("splash.html", version = VERSION)

    # Operator probably disabled the front-end form validation
    if region.replace("_", "").isalnum() is False:
        abort(404)

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
        abort(404)

    # We assume we have results to deliver at this point
    stamps  = []
    regions = []
    wfes    = [[], []]
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
        stamp = datetime.utcfromtimestamp(value[0]).strftime('%B %d, %Y')
        stamp_entry = f"""<p class="center stamps{hide}">Entry from {stamp}</p>"""
        stamps.append(stamp_entry)

        # Load regions
        region_entry = f"""<p class="title space is-2 regions{hide}" style="margin-bottom: 0rem;"><a class="gold" href="https://www.nationstates.net/region={value[1].lower().replace(' ', '_')}" target="_blank">{value[1]}</a></p>"""
        regions.append(region_entry)

        # Load WFEs
        wrapper_entry = f"""<pre class="data-display wfes{hide}" style="font-size: 10pt;">"""
        wfe_entry = html.unescape(value[2])

        wfes[0].append(wrapper_entry)
        wfes[1].append(wfe_entry)

        # Load tags
        tag_entry = f"""<pre class="data-display tags{hide}">{value[3]}</pre>"""
        tags.append(tag_entry)

        # Load ROs
        ro_entry = f"""<pre class="data-display ros{hide}">{value[4]}</pre>"""
        ros.append(ro_entry)

        # Load flags
        if value[5] != "":
            pflag = f"""<a href="static/flags/{value[5]}" download><img alt="flag from {stamp}" src="static/flags/{value[5]}"></a>"""
            flag_entry = f"""<pre class="data-display flags{hide}">{pflag}</pre>"""
        else:
            flag_entry = f"""<pre class="data-display flags{hide}"></pre>"""
        flags.append(flag_entry)

        # Load banners
        if value[6] == "":
            banner_entry = f"""<pre class="data-display banners{hide}"></pre>"""
        elif len(value[6]) < 3:
            banner_entry = f"""<pre class="data-display banners{hide}"><p class="gold" style="font-size: 10pt;">This is a stock banner. Select it in the region's admin menu.</p><img src ="https://www.nationstates.net/images/rbanners/{value[6]}"></pre>"""
        else:
            banner_entry = f"""<pre class="data-display banners{hide}"><a href="static/banners/{value[6]}" download><img alt="banner from {stamp}" src="static/banners/{value[6]}"></a></pre>"""
        banners.append(banner_entry)

    # Disable buttons when they can't flip to new snapshots
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
    length  = len(data),
    breaks  = breaks,
    stamps  = stamps,
    regions = regions,
    wfes    = wfes,
    tags    = tags,
    ros     = ros,
    flags   = flags,
    banners = banners,
    )

    # Slep
    connect.close()

#######################################
# ---            Misc.            --- #
#######################################

# Robits
@app.route('/robots.txt')
def robits():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == "__main__":
    app.run()