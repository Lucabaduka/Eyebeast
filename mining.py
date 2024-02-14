import os
import time
import requests
import xml.etree.ElementTree as et
import sqlite3

VERSION     = "1.0.6"
rec         = "/var/www/nightly/rec"
path        = "/var/www/eyebeast"
flag_path   = "/var/www/eyebeast/static/flags"
banner_path = "/var/www/eyebeast/static/banners"
headers     = {"User-Agent": f"Refuge Isle, running Eyebeast, v{VERSION}"}

# Form the database if it doesn't exist
if not os.path.isfile(f"{path}/eyebeast.db"):
    connect = sqlite3.connect(f"{path}/eyebeast.db")

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

# Make these directories if they don't exist
if not os.path.isdir(flag_path):
    os.mkdir(flagpath)
if not os.path.isdir(banner_path):
    os.mkdir(banner_path)

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

# Establish connection
connect = sqlite3.connect(f"{path}/eyebeast.db")
c = connect.cursor()

# Easy add
def insert_record(record):
    with connect:
        c.execute("INSERT INTO eyebeast VALUES (:stamp, :region, :wfe, :tags, :ros, :flagname, :banner)",
                {"stamp": record.stamp, "region": record.region, "wfe": record.wfe, "tags": record.tags, "ros": record.ros, "flagname": record.flag, "banner": record.banner})

# Easy subtract
def remove_record(record):
    with connect:
        c.execute("DELETE from eyebeast WHERE stamp = :stamp AND region = :region",
                {"stamp": record.stamp, "region": record.region, "wfe": record.wfe, "tags": record.tags, "ros": record.ros, "flagname": record.flag, "banner": record.banner})

# Main
def main():

    # Initialise static variables
    stamp = int(time.time())

    tag_list = [
        "Anarchist", "Anime", "Anti-Capitalist", "Anti-Communist", "Anti-Fascist", "Anti-General Assembly", "Anti-Security Council", "Anti-World Assembly",
        "Capitalist", "Casual", "Colony", "Communist", "Conservative", "Cyberpunk", "Defender", "Democratic", "Eco-Friendly", "Egalitarian",
        "Embassy Collector", "F7er", "FT FtL", "FT FTLi", "FT STL", "Fandom", "Fantasy Tech", "Fascist", "Feminist", "Free Trade", "Frontier", "Future Tech",
        "Game Player", "General Assembly", "Generalite", "Human-Only", "Imperialist", "Independent", "Industrial", "International Federalist", "Invader",
        "Isolationist", "Issues Player", "Jump Point", "LGBT", "Liberal", "Liberated", "Libertarian", "Magical", "Map", "Mercenary", "Modern Tech", "Monarchist",
        "Multi-Species", "National Sovereigntist", "Neutral", "Non-English", "Offsite Chat", "Offsite Forums", "Outer Space", "P2TM", "Pacifist", "Parody",
        "Password", "Past Tech", "Patriarchal", "Post Apocalyptic", "Post-Modern Tech", "Puppet Storage", "Regional Government", "Religious", "Role Player",
        "Security Council", "Serious", "Silly", "Snarky", "Social", "Socialist", "Sports", "Steampunk", "Surreal", "Theocratic", "Totalitarian", "Trading Cards",
        "Video Game", "World Assembly"
        ]
    tag_regions = []

    ro_letters = ["A", "B", "C", "E", "P", "S"]
    ro_powers = ["Appearance", "Border Control", "Communications", "Embassies", "Polls", "Successor"]

    # Acquire region tag list
    print("Loading regional tags...")
    for x in tag_list:
        print(f"Loading {x}")
        insert = []

        # API call to list of regions by x (tag)
        url = f"""https://www.nationstates.net/cgi-bin/api.cgi?q=regionsbytag;tags={x.replace(" ", "_")}"""
        r = requests.get(url, headers = headers)
        with open(f"{rec}/tags.xml", "wb") as f:
            f.write(r.content)
            f.close()
        time.sleep(2)

        # Parse response and append to list of lists
        root = et.parse(f"{rec}/tags.xml").getroot()
        insert = root.find("REGIONS").text

        # Tag stopped existing
        if insert == None:
            insert = []

        # Tag working as expected
        elif "," in insert:
            insert = (root.find("REGIONS").text).split(",")

        # Tag contains one item
        else:
            pass

        tag_regions.append(insert)

    print("Tag data loaded.")

    # Parse region dump
    root = et.parse(f"{rec}/regions.xml").getroot()
    for x in root.findall("REGION"):

        try:
            flagname = ""
            ros = ""
            tags = ""

            region = x.find("NAME").text

            wfe = ""
            if x.find("FACTBOOK") != None:
                if x.find("FACTBOOK").text != None:
                    wfe = x.find("FACTBOOK").text

            banner = ""
            if x.find("BANNERURL") != None:
                if x.find("BANNERURL").text != None:
                    banner = x.find("BANNERURL").text

            flag = None
            if x.find("FLAG") != None:
                if x.find("FLAG").text != None:
                    flag = x.find("FLAG").text

            # RO proceedure
            for y in x.findall("OFFICERS"):
                for z in y.findall("OFFICER"):
                    if ros != "":
                        ros += "\n\n"

                    officer = z.find("NATION").text
                    if officer is not None:
                        office = z.find("OFFICE").text
                        permissions = z.find("AUTHORITY").text
                        powers = ""
                        for i in ro_letters:
                            if i in permissions:
                                powers += ro_powers[ro_letters.index(i)] + " • "
                        if len(powers) > 3:
                            powers = powers[:-3]

                        ros += f"""{officer} | {office}\n{powers}"""

            # Tag stuff now
            for y in tag_regions:
                if region in y:
                    tags += tag_list[tag_regions.index(y)] + "\n"
            if len(tags) > 1:
                tags = tags[:-1]

            # Flag stuff now
            if flag != None:
                extension = flag[-4:]
                flagname = f"""{stamp}-{region.lower().replace(" ", "_")}{extension}"""
                flagsave = f"""{flag_path}/{flagname}"""
                r = requests.get(flag, headers = headers)

                # File still exists
                if "Page Not Found" not in str(r.content):
                    with open(flagsave, "wb") as f:
                        f.write(r.content)
                        f.close()
                    print(f"Downloaded: {flag}")
                    time.sleep(1.3)

            # Banner stuff now
            if "/uploads/" in banner:
                extension = banner.partition(".")[2] # Maybe change if stock banners expand
                bannername = f"""{stamp}-{region.lower().replace(" ", "_")}.{extension}"""
                bannersave = f"""{banner_path}/{bannername}"""
                r = requests.get(f"""https://www.nationstates.net/{banner}""", headers = headers)

                # File still exists
                if "Page Not Found" not in str(r.content):
                    with open(bannersave, "wb") as f:
                        f.write(r.content)
                        f.close()
                    print(f"Downloaded: {bannername}")
                    time.sleep(1.3)

            else:
                bannername = banner.partition("/images/rbanners/")[2].replace(".jpg", "")  # Maybe change to {extension} if stock banners expand

            # Save the entry
            record = Byakuya(stamp, region, wfe, tags, ros, flagname, bannername)
            insert_record(record)

        except:
            continue

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
                    os.remove(f"""{flag_path}/{record.flag}""")
                except:
                    pass

            # Prune banner file
            if len(record.banner) > 3:
                try:
                    os.remove(f"""{banner_path}/{record.banner}""")
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

    # Report any errors to the CalRef discord server
    except Exception as e:
        name = "Dispatch Routine"
        payload = {
        "username": "Nightly",
        "embeds": [{
            "author": {
                "name": "Eyebeast: Failure",
                "icon_url": "https://calref.ca/post/busy.png"
            },
            "description": f"""The **Eyebeast Miner** encountered the following error:\n\n{e}""",
            "color":0xf31a71,
        }],
    }
        requests.post("https://discord.com/api/webhooks/1026162476120801422/aGvCnpBAc8mYHigxB9KWHIYw7-MPkqn4q6-jAqSS9anOkrKPM_lX6OMHWNNNtUvgDax4", json=payload)