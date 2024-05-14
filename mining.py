import os
import time
import requests
import xml.etree.ElementTree as et
import sqlite3
import zlib

#######################################
# ---        Configuration        --- #
#######################################

NIGHTLY   = True                      # Should be True if run on CalRef servers, should be False if not.
OPERATOR  = "Default"                 # Should be the operator's main nation or email address.
WEBHOOKS  = [                         # Should be a list of Discord webhook URL strings to receive a copy of the report.
    
]

#######################################
# --- Do not edit below this line --- #
#######################################

VERSION     = "1.2.0"
PATH        = os.path.dirname(__file__)
HEADERS     = {"User-Agent": f"{OPERATOR}, running Eyebeast, v{VERSION}"}
connect     = sqlite3.connect(f"{PATH}/eyebeast.db")
c           = connect.cursor()

# Do you know the difference between you and I? It's a class
class Byakuya:
    """Helps put things in their place"""

    def __init__(self, stamp, region, wfe, tags, ros, flag, banner):
        self.stamp  = stamp
        self.region = region
        self.wfe    = wfe
        self.tags   = tags
        self.ros    = ros
        self.flag   = flag
        self.banner = banner

# API Call
# Called every time we make a request to NationStates
def api_call(url):
    r = requests.get(url, headers = HEADERS)
    time.sleep(1.2)
    return r.text

# Clean Up
# Called to clean up data dump files when not in use and prevent repeat data
def clean_up(record_path):
    for roots, dirs, files in os.walk(record_path):
        for x in files:
            cleanup = os.path.join(roots, x)
            os.remove(cleanup)

# Dump Handle
# Called if Nightly doesn't handle getting the NS Data dump
def dump_handle(record_path):

    # Wipe down the table
    clean_up(record_path)

    # Acquire data dump
    print("Acquiring data dump. . .")
    url = "https://www.nationstates.net/pages/regions.xml.gz"
    r = requests.get(url, headers = HEADERS)
    with open(f"{record_path}/regions.xml.gz", "wb") as f:
        f.write(r.content)
        f.close()

    # Extract XML file from gunzip via chunking
    print("Extracting. . .")
    CHUNKSIZE = 1024
    with open(f"{record_path}/regions.xml", "wb") as extracted:
        d = zlib.decompressobj(16+zlib.MAX_WBITS)
        f = open(f"{record_path}/regions.xml.gz","rb")
        buffer=f.read(CHUNKSIZE)
        while buffer:
            out = d.decompress(buffer)
            extracted.write(out)
            buffer=f.read(CHUNKSIZE)
        out = d.flush()
        extracted.close()

# Insert New
# Called when adding entries to the database
def insert_record(record):
    with connect:
        c.execute("INSERT INTO eyebeast VALUES (:stamp, :region, :wfe, :tags, :ros, :flagname, :banner)",
                {"stamp": record.stamp, "region": record.region, "wfe": record.wfe, "tags": record.tags, "ros": record.ros, "flagname": record.flag, "banner": record.banner})

# Delete Old
# Called when removing entries from the database
def remove_record(record):
    with connect:
        c.execute("DELETE from eyebeast WHERE stamp = :stamp AND region = :region",
                {"stamp": record.stamp, "region": record.region, "wfe": record.wfe, "tags": record.tags, "ros": record.ros, "flagname": record.flag, "banner": record.banner})

# Self-right
# Called to create missing files and directories, returns record path
def self_righting():

    # Form the database if it doesn't exist
    if not os.path.isfile(f"{PATH}/eyebeast.db"):
        connect = sqlite3.connect(f"{PATH}/eyebeast.db")

        c = connect.cursor()
        c.execute("""CREATE TABLE eyebeast (
                stamp integer,
                region text,
                wfe text,
                tags text,
                ros text,
                flag text,
                banner text
                )""")

        connect.commit()
        connect.close()

    if NIGHTLY:
        record_path = "/var/www/nightly/rec"
    else:
        if not os.path.isdir(f"{PATH}/rec"):
            os.mkdir(f"{PATH}/rec")

        record_path = f"{PATH}/rec"
        dump_handle(record_path)

    return record_path

# Main
def main():

    # Initialise static variables
    stamp = int(time.time())

    # At some point, it would be nice to replace this list with an API call, but no such API shard exists at present
    tag_list = [
        "Anarchist", "Anime", "Anti-Capitalist", "Anti-Communist", "Anti-Fascist", "Anti-General Assembly", "Anti-Security Council",
        "Anti-World Assembly", "Capitalist", "Casual", "Colony", "Communist", "Conservative", "Cyberpunk", "Defender", "Democratic",
        "Eco-Friendly", "Egalitarian", "Embassy Collector", "F7er", "FT FtL", "FT FTLi", "FT STL", "Fandom", "Fantasy Tech",
        "Fascist", "Feminist", "Free Trade", "Frontier", "Future Tech", "Game Player", "General Assembly", "Generalite",
        "Human-Only", "Imperialist", "Independent", "Industrial", "International Federalist", "Invader", "Isolationist",
        "Issues Player", "Jump Point", "LGBT", "Liberal", "Liberated", "Libertarian", "Magical", "Map", "Mercenary", "Modern Tech",
        "Monarchist", "Multi-Species", "National Sovereigntist", "Neutral", "Non-English", "Offsite Chat", "Offsite Forums",
        "Outer Space", "P2TM", "Pacifist", "Parody", "Password", "Past Tech", "Patriarchal", "Post Apocalyptic", "Post-Modern Tech",
        "Puppet Storage", "Regional Government", "Religious", "Role Player", "Security Council", "Serious", "Silly", "Snarky",
        "Social", "Socialist", "Sports", "Steampunk", "Surreal", "Theocratic", "Totalitarian", "Trading Cards", "Video Game",
        "World Assembly"
        ]
    tag_regions = []

    ros_dict = {
        "A": "Appearance",
        "B": "Border Control",
        "C": "Communications",
        "E": "Embassies",
        "P": "Polls",
        "S": "Successor",
        "X": "Executive",
        "W": "World Assembly"
        }

    # Acquire region tag list
    print("Loading regional tags...")
    for x in tag_list:
        print(f"Loading {x}")

        try:
            # API call to list of regions by x (tag)
            data = api_call(f"""https://www.nationstates.net/cgi-bin/api.cgi?q=regionsbytag;tags={x.replace(" ", "_")}""")

            # Parse response and append to list of lists
            root = et.fromstring(data)
            insert = root.find("REGIONS")

            # Tag stopped existing
            if insert == None:
                insert = []

            # Tag working as expected
            elif "," in root.find("REGIONS").text:
                insert = root.find("REGIONS").text.split(",")

            # Tag contains one item
            else:
                insert = root.find("REGIONS").text

            tag_regions.append(insert)

        # likely invoked if NationStates ever deletes a tag without notice
        except:

            # In which case we will just move on
            continue

    print("Tag data loaded.")

    # Parse region dump
    record_path = self_righting()
    root = et.parse(f"{record_path}/regions.xml").getroot()
    for x in root.findall("REGION"):

        # We basically wrap everything in try-excepts because of the high
        # probability of NationStates delivering bullshit data at some point
        try:
            region = x.find("NAME").text

            wfe = ""
            if x.find("FACTBOOK") != None:
                wfe = x.find("FACTBOOK").text

            banner = ""
            if x.find("BANNERURL") != None:
                banner = x.find("BANNERURL").text

            flag = None
            if x.find("FLAG") != None:
                flag = x.find("FLAG").text

            # RO procedure
            ros = ""
            for y in x.findall("OFFICERS"):
                for z in y.findall("OFFICER"):
                    if ros != "":
                        ros += "\n\n"

                    if z.find("NATION") != None:
                        officer = z.find("NATION").text
                        office = z.find("OFFICE").text
                        permissions = z.find("AUTHORITY").text
                        powers = ""
                        for i in ros_dict:
                            if i in permissions:
                                powers += ros_dict[i] + " • "
                        if len(powers) > 3:
                            powers = powers[:-3]

                        ros += f"""{officer} | {office}\n{powers}"""

            # Tag stuff now
            tags = ""
            for y in tag_regions:
                if region in y:
                    tags += tag_list[tag_regions.index(y)] + "\n"
            if len(tags) > 1:
                tags = tags[:-1]

            # Flag stuff now
            flagname = ""
            if flag != None:
                extension = flag[-4:]
                flagname = f"""{stamp}-{region.lower().replace(" ", "_")}{extension}"""
                flagsave = f"""{PATH}/static/flags/{flagname}"""
                r = requests.get(flag, headers = HEADERS)

                # File still exists
                if r.status_code == 200:
                    with open(flagsave, "wb") as f:
                        f.write(r.content)
                        f.close()
                    print(f"Downloaded: {flag}")
                    time.sleep(1.2)

            # Banner stuff now
            if "/uploads/" in banner:
                extension = banner.partition(".")[2] # Maybe change if stock banners expand
                bannername = f"""{stamp}-{region.lower().replace(" ", "_")}.{extension}"""
                bannersave = f"""{PATH}/static/banners/{bannername}"""
                r = requests.get(f"""https://www.nationstates.net/{banner}""", headers = HEADERS)

                # File still exists
                if r.status_code == 200:
                    with open(bannersave, "wb") as f:
                        f.write(r.content)
                        f.close()
                    print(f"Downloaded: {bannername}")
                    time.sleep(1.2)

            else:
                bannername = banner.partition("/images/rbanners/")[2].replace(".jpg", "")  # Maybe change to {extension} if stock banners expand

            # Save the entry
            record = Byakuya(stamp, region, wfe, tags, ros, flagname, bannername)
            insert_record(record)

        except:
            continue

    # Wipe down the table again
    clean_up(record_path)

    # Vanquishing module
    prune = stamp - 15552000 # six months
    c.execute(f"""SELECT * FROM eyebeast WHERE stamp < {prune}""")

    for x in c.fetchall():
        try:

            # Acquire record
            record = Byakuya(x[0], x[1], x[2], x[3], x[4], x[5], x[6])

            # Delete from database
            remove_record(record)

            # Prune flag file
            if record.flag != "":
                try:
                    os.remove(f"""{PATH}/static/flags/{record.flag}""")
                except:
                    pass

            # Prune banner file
            if len(record.banner) > 3:
                try:
                    os.remove(f"""{PATH}/static/banners/{record.banner}""")
                except:
                    pass

        except:
            continue

    # Close database
    connect.close()

if __name__ == "__main__":

    # Run mining program
    try:
        main()

    # Report any errors to discord webhooks
    except Exception as e:
        payload = {
        "embeds": [
            {
            "description": f"""{e}""",
            "color": 0xf31a71,
            "author": {
                "name": "The Eyebeast Miner encountered an error:",
                "icon_url": "https://calref.ca/post/busy.png"
            }
            }
        ],
        }

        for x in WEBHOOKS:
            requests.post(x, json=payload)