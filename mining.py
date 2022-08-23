import os
import time
import requests
import xml.etree.ElementTree as et
import sqlite3

rec = "/var/www/nightly/rec"
path = "/var/www/eyebeast"
flag_path = "/var/www/eyebeast/static/flags"
banner_path = "/var/www/eyebeast/static/banners"

# Initial database creation
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

if not os.path.isdir(flag_path):
    os.mkdir(flagpath)
if not os.path.isdir(banner_path):
    os.mkdir(banner_path)

# Do you know the difference between you and I? It's a class
class Byakuya:
    """Helps put things in their place"""

    def __init__(self, stamp, region, wfe, tags, ros, flag, banner):
        self.stamp = stamp
        self.region = region
        self.wfe = wfe
        self.tags = tags
        self.ros = ros
        self.flag = flag
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

def main():
    # Initialise static variables
    stamp = int(time.time())

    tag_list = [
        "Anarchist", "Anime", "Anti-Capitalist", "Anti-Communist", "Anti-Fascist", "Anti-General Assembly", "Anti-Security Council", "Anti-World Assembly",
        "Capitalist", "Casual", "Communist", "Conservative", "Cyberpunk", "Defender", "Democratic", "Eco-Friendly", "Egalitarian", "F7er", "FT FtL", 
        "FT FTLi", "FT STL", "Fandom", "Fantasy Tech", "Fascist", "Feminist", "Free Trade", "Future Tech", "Game Player", "General Assembly", 
        "Generalite", "Human-Only", "Imperialist", "Independent", "Industrial", "International Federalist", "Invader", "Isolationist", "Issues Player",
        "Jump Point", "LGBT", "Liberal", "Liberated", "Libertarian", "Magical", "Map", "Mercenary", "Modern Tech", "Monarchist", "Multi-Species", 
        "National Sovereigntist", "Neutral", "Non-English", "Offsite Chat", "Offsite Forums", "Outer Space", "P2TM", "Pacifist", "Parody", "Past Tech", 
        "Patriarchal", "Post Apocalyptic", "Post-Modern Tech", "Puppet Storage", "Recruiter Friendly", "Regional Government", "Religious", "Role Player",
        "Security Council", "Serious", "Silly", "Snarky", "Social", "Socialist", "Sports", "Steampunk", "Surreal", "Theocratic", "Totalitarian",
        "Trading Cards", "Video Game", "World Assembly"
        ]
    tag_regions = []

    ro_letters = ["A", "B", "C", "E", "P"]
    ro_powers = ["Appearance", "Border Control", "Communications", "Embassies", "Polls"]

    # Acquire region tag list
    print("Loading regional tags...")
    for x in tag_list:
        print(f"Loading {x}")
        insert = []

        # API call to list of regions by x (tag)
        url = f"https://www.nationstates.net/cgi-bin/api.cgi?q=regionsbytag;tags={x.replace(' ', '_')}"
        r = requests.get(url, headers = {'User-Agent': 'Refuge Isle, running Nightly'})
        with open(f"{rec}/tags.xml", "wb") as f:
            f.write(r.content)
            f.close()
        time.sleep(2)

        # Parse response and append to list of lists
        root = et.parse(f"{rec}/tags.xml").getroot()
        insert = (root.find("REGIONS").text).split(",")
        tag_regions.append(insert)

    print("Tag data loaded.")

    # Parse region dump
    root = et.parse(f"{rec}/regions.xml").getroot()
    for x in root.findall("REGION"):

        try:
            flag = None
            flagname = ""
            ros = ""
            tags = ""
            banner = x.find("BANNER").text
            region = x.find("NAME").text
            flag = x.find("FLAG").text
            wfe = x.find("FACTBOOK").text

            # WFE proceedure
            if wfe == None:
                wfe = ""

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
                flagname = f"{stamp}-{region.lower().replace(' ', '_')}{extension}"
                flagsave = f"{flag_path}/{flagname}"
                r = requests.get(flag, headers = {'User-Agent': 'Refuge Isle, running Nightly'})

                # File still exists
                if "Page Not Found" not in str(r.content):
                    with open(flagsave, "wb") as f:
                        f.write(r.content)
                        f.close()
                    print(f"Downloaded: {flag}")
                    time.sleep(1.5)

            # Banner stuff now
            if banner == "0":
                bannername = ""
            else:
                if "r" not in banner:
                    bannername = f"{stamp}-{region.lower().replace(' ', '_')}.jpg"
                    bannersave = f"{banner_path}/{bannername}"
                    r = requests.get(f"https://www.nationstates.net/images/rbanners/uploads/{region.lower().replace(' ', '_')}__{banner}.jpg", headers = {'User-Agent': 'Refuge Isle, running Nightly'})

                    # File still exists
                    if "Page Not Found" not in str(r.content):
                        with open(bannersave, "wb") as f:
                            f.write(r.content)
                            f.close()
                        print(f"Downloaded: {bannername}")
                        time.sleep(1.5)

                else:
                    bannername = banner

            # Save the entry
            record = Byakuya(stamp, region, wfe, tags, ros, flagname, bannername)
            insert_record(record)

        except:
            continue

    # Vanquishing module
    prune = stamp - 15552000 # six months
    c.execute(f"SELECT * FROM eyebeast WHERE stamp < {prune}")

    for x in c.fetchall():
        try:

            # Acquire record
            record = Byakuya(x[0], x[1], x[2], x[3], x[4], x[5], x[6])

            # Prune flag file
            if record.flag != "":
                os.remove(f"{flag_path}/{record.flag}")

            # Prune banner file
            if "r" not in record.banner and record.banner != "" and record.banner != "0":
                os.remove(f"{banner_path}/{record.banner}")

            # Delete from database
            remove_record(record)

        except:
            continue

    # Close database
    connect.close()

if __name__ == "__main__":
    main()
