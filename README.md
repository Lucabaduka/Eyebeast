# Eyebeast: Eldritch Archival Utility ![Version 1.3.0](https://img.shields.io/badge/Version-1.3.0-0099ff)

<table align="center"><tr>
<td align="center">

<img src="https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white&style=flat" alt="HTML5"> <img src="https://img.shields.io/badge/-Bulma-00D1B2?logo=bulma&logoColor=white&style=flat" alt="CSS 3"> <img src="https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=white&style=flat" alt="JavaScript">
<br>Front End

</td><td align="center">

<img src="https://img.shields.io/badge/-Python%203-3776AB?logo=python&logoColor=white&style=flat" alt="python3"> <img src="https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white&style=flat" alt="Flask"> <img src="https://img.shields.io/badge/-SQLite%203-003B57?logo=sqlite&logoColor=white&style=flat" alt="SQLite">
<br>Back End

</td>
</tr></table>

## Overview
Eyebeast is a data archival utility designed to help recover recently lost data for a given region on [NationStates.net](https://www.nationstates.net/). Data is organised into snapshots of how a region looked at a particular point in time. Every snapshot attempts to record the following, if available:
- Proper name formatting
- Regional flag
- Regional banner
- World Factbook Entry
- Search tags
- Regional Officers

Snapshots can be taken by configuring, then operating `mining.py` on a cron job. In production, this job is scheduled to start at 01:00 Pacific Time, every Monday, typically concluding around 10:00 to 12:00 noon. After a snapshot's timestamp reaches six months of age, its record is pruned from the database and applicable flag and banner image files are removed from the server.

**The official Eyebeast website is located here:** https://eyebeast.calref.ca/

## Operator Usage
The splash page is a simple search box, where an operator may input a region name, or a region's URL. On submission, and if a region could be located in the database, the operator will be taken to a results page. The operator may flip through available snapshots with the `◀ Forward` and `Backward ▶` nav buttons. World Factbook Entries can be copied with the `Copy` button on the page, and flags or banners can be downloaded with a simple left click or device tap.

Outside the splash page, the search bar will always be at the top of the screen so the operator may move on to additional regions if necessary. On mobile, a floating anchor button will be in the bottom right corner of the screen to better navigate results pages with larger volumes of data.

## Installation and Configuration

Minimum Python version: 3.8

Simply clone the repository into the directory of your choosing, or download the repository as a zip and extract it to where it will be run.

You may wish to operate through a virtual environment and, if you're running python 3.11, you'll *definitely* want to do that. Slap one up today with `python3 -m venv path` with the `path` being wherever you want to put it. Activate the environment with `source path/bin/activate` and install the requirements with `pip install -r requirements.txt`.

The only Eyebeast file to configure is `mining.py`, which contains three variable options in its configuration area.
- `NIGHTLY` asks if the Eyebeast is running as a component of Nightly or needs to download the dump itself.
- `OPERATOR` asks for your required [user agent](https://www.nationstates.net/pages/api.html#terms), ideally your main nation name or email.
- `WEBHOOKS` allows you to place any webhooks to which you would like errors to post

Do not forget to set up a weekly cron job for `mining.py`, such as with Linux' `crontab` utility. If running locally, you can just run `eyebeast.py` in your virtual environment at this point.

Eyebeast is designed to run on `mod_wsgi` but can be set up on something less reprehensible if one is feeling adventurous. A semi-workable sample config for Apache2 includes, but is not limited to, the following:

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

## History

Eyebeast was created by [Refuge Isle](https://www.nationstates.net/nation=refuge_isle), in February 2021. It began as a private python experiment to programatically download region flags in place of the Taijitu flag recovery site, which had not worked for at least five years at that time. It was also intended to save additional data like region tags and regional officers, which The Grey Wardens' [WFE Index](https://greywardens.xyz/tools/wfe_index/) did not record. The user-interface left something to be desired, however, as one could only traverse the files by manually adjusting the URL.

Eventually, in August 2022, it [released](https://forum.calref.ca/index.php?topic=9.msg3853#msg3853) as a properly developed web app with improved storage methods, picked up an actual user interface, and gained the ability to recover region banners. In November 2022, Eyebeast received the distinction of being awarded the NS Defender tech contribution of that year.

## Required Disclosures

I am a NationStates staff member; therefore, I am required to provide a disclaimer that operators of this tool should not assume it to be legal. It remains the player's responsibility to ensure any tools they use comply with the [Script Rules](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966).