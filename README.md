# Eyebeast: Eldritch Archival Utility ![Version 1.3.2](https://img.shields.io/badge/Version-1.3.2-0099ff)

<table align="center"><tr><td align="center">
<img src="https://img.shields.io/badge/-Bulma-00D1B2?logo=bulma&logoColor=white&style=flat" alt="CSS 3"> <img src="https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=white&style=flat" alt="JavaScript">
<br>
<img src="https://img.shields.io/badge/-Python%203-3776AB?logo=python&logoColor=white&style=flat" alt="python3"> <img src="https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white&style=flat" alt="Flask"> <img src="https://img.shields.io/badge/-SQLite%203-003B57?logo=sqlite&logoColor=white&style=flat" alt="SQLite"></td></tr></table>

## Overview
Eyebeast is a data archival utility designed to help recover recently lost data for a given region on [NationStates.net](https://www.nationstates.net/). Data is organised into snapshots of how a region looked at a particular point in time, and retained in the database for six months. Every snapshot attempts to record the following, if available:
- Proper name formatting
- Regional flag
- Regional banner
- World Factbook Entry
- Search tags
- Regional Officers

**The official Eyebeast website is located here:** https://eyebeast.calref.ca/

## Operator Usage
The splash page is a simple search box, where an operator may input a region name, or a region's URL. On submission, the operator will be taken to a results page if results could be found, or a 404 page if they couldn't. In the results, the operator may flip through available snapshots with the `◀ Forward` and `Backward ▶` nav buttons. World Factbook Entries can be copied with the `Copy` button on the page, and flags or banners can be downloaded with a simple left click or device tap.

Outside of the splash page, the search bar will always be at the top of the screen so the operator may move on to additional regions if necessary. On mobile, a floating anchor button will be in the bottom right corner of the screen to better navigate results pages with larger volumes of data.

## Installation and Configuration

Minimum Python version: 3.8

1. Clone the repository into the directory of your choosing, or download the repository and upload/extract it to where it will be run.

2. Like all Python programs, you should run this through a virtual environment. Slap one up today with `python3 -m venv path` where `path` is wherever you want to put your virtual environment.

3. Activate the environment with `source path/bin/activate` and `cd` to wherever you cloned/uploaded eyebeast in step 1. Then install the requirements with `pip install -r requirements.txt`.

4. `mining.py`, is configurable by way of three variable options in its configuration area. Adjust as necessary:
   - `NIGHTLY` asks if the Eyebeast is running as a component of Nightly or needs to download the dump itself.
   - `OPERATOR` asks for your required [user agent](https://www.nationstates.net/pages/api.html#terms), ideally your main nation name or email.
   - `WEBHOOKS` allows you to place any webhooks to which you would like errors to post.

5. Set up a weekly cron job for `mining.py`, such as with Linux' `crontab` utility.

6. If running locally, you can just run `eyebeast.py` in your virtual environment at this point, whenever you need to access it. If hosting, set the path of `wsgi.py` in line 2 to the path of wherever you cloned/uploaded Eyebeast in step 1 and read below.

---

Eyebeast is designed to run on [`mod_wsgi`](https://modwsgi.readthedocs.io/en/master/) but can be set up on something less reprehensible if one is feeling adventurous. A sample config for Apache2 includes, but is not limited to, the following:

```
WSGIDaemonProcess eyebeast python-home=/your/venv/path/
WSGIProcessGroup eyebeast

<VirtualHost example.org:80>
   ServerName example.org
   ServerAdmin beans@example.org

   WSGIScriptAlias / /your/eyebeast/path/wsgi.py process-group=eyebeast
   <Directory /your/eyebeast/path>
      Order allow,deny
      Allow from all
   </Directory>
</VirtualHost>
```

## Notes, Disclosures, Etc.

I am a NationStates staff member; therefore, I am required to provide a disclaimer that operators of this tool should not assume it to be legal. It remains the player's responsibility to ensure any tools they use comply with the [Script Rules](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966).

Eyebeast uses a Bulma v0.9.4 CSS framework in a minified file compiled from `beholder.css`, Eyebeasts theme colours, and [CalRef's local copy](https://calref.ca/bulma.css) of Bulma 0.9.4.

There is a `DEBUG` variable in `mining.py` that, when set to `True`, will cause it to die on every mining error and post them to `error.log`. By default, this is set to `False` because I assume the probability of NationStates feeding me corrupted data is orders of magnitude greater than the probability of Eyebeast bugging on its own. In normal operation, the miner should keep making mining attempts instead of dying on a random region four hours in, but if making substantial changes, it's good to test with this turned on, or when running the miner for atypical reasons.

### History

Eyebeast was created in February 2021. It began as a private python experiment to programatically download region flags in place of the Taijitu flag recovery site, which had not worked for at least five years at that time. It was also intended to save additional data like region tags and regional officers, which The Grey Wardens' [WFE Index](https://greywardens.xyz/tools/wfe_index/) did not record. A user-interface did not exist, as one could only traverse the files by manually adjusting the URL, but it could restore flag data at least.

In August 2022, it was [remade](https://forum.calref.ca/index.php?topic=9.msg3853#msg3853) as a properly developed web app with improved storage methods, picked up an actual user interface, and gained the ability to recover region banners. In November 2022, Eyebeast received the distinction of being voted the NS Defender tech contribution of that year.
