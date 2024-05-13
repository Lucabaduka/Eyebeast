# Eyebeast: Eldritch Archival Utility ![Version 1.2.0](https://img.shields.io/badge/Version-1.2.0-0099ff)

<table align="center"><tr>
<td align="center">

<img src="https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white&style=flat" alt="HTML5"> <img src="https://img.shields.io/badge/-Bulma-00D1B2?logo=bulma&logoColor=white&style=flat" alt="CSS 3"> <img src="https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=white&style=flat" alt="JavaScript">
<br>Front End

</td><td align="center">

<img src="https://img.shields.io/badge/-Python%203-3776AB?logo=python&logoColor=white&style=flat" alt="python3"> <img src="https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white&style=flat" alt="Flask"> <img src="https://img.shields.io/badge/-SQLite%203-003B57?logo=sqlite&logoColor=white&style=flat" alt="SQLite">
<br>Back End

</td>
</tr></table>

### Overview
Eyebeast is a data archival utility designed to help recover recently lost data for a given region on NationStates. Data is organised into snapshots of how the region looked at a particular point in time. Every snapshot attempts to record the following, if available:
- Proper name formatting
- Regional flag
- Regional banner
- World Factbook Entry
- Search tags
- Regional Officers

Snapshots can be taken by configuring, then operating `mining.py` on a cron job. In production, this job is scheduled to start at 01:00 Pacific Time, every Monday, typically concluding around 10:00 to 12:00 noon. After a snapshot's timestamp reaches six months of age, its record is pruned from the database and applicable flag and banner image files are removed from the server.

**Live:** https://eyebeast.calref.ca/

### Operator Usage
The splash page is a simple search box, where an operator may input a region name, or a region's URL. On submission, and if a region could be located in the database, the operator will be taken to a results page. An operator may toggle between available snapshots with the `◀ Forward` and `Backward ▶` nav buttons. World Factbook Entries can be copied with the `Copy` button on the page, and flags or banners can be downloaded with a simple click or device tap.

Outside the splash page, the search bar will always be at the top of the screen so an operator may move onto additional regions if necessary. On mobile, a floating anchor button will be in the bottom right corner of the screen to better navigate results pages with larger volumes of data.