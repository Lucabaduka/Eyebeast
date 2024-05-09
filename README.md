# Eyebeast - Eldritch Archival Utility ![Version 1.1.1](https://img.shields.io/badge/Version-1.1.1-0099ff)
##### A utility for region-builders, defenders, and researchers to recover region data on NationStates.

### Front End
![HTML 5](https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white&style=flat) ![CSS 3](https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white&style=flat) ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=white&style=flat)

### Back End
<img src="https://img.shields.io/badge/-Python%203-3776AB?logo=python&logoColor=white&style=flat" alt="python3"> <img src="https://img.shields.io/badge/-SQLite%203-003B57?logo=sqlite&logoColor=white&style=flat" alt="SQLite"> <img src="https://img.shields.io/badge/-Flask%203-000000?logo=flask&logoColor=white&style=flat" alt="Flask">


## Overview
Eyebeast allows you to browse up to six months of data for a given region on NationStates, organised into snapshots of how the region looked at a particular point in time. In the main production application, these snapshots are taken as a component of Nightly, Calamity Refuge's main maintenance and processing routine.

Eyebeast's component of that routing (mining) runs once a week from, from midnight to 12:00 noon, Pacific time, every Wednesday. After a snapshot reaches six months of age, its applicable flags and banners are pruned from the server, and its record is removed from the database.

## Usage
The splash page is a simple search box, where an operator may input a region name, or a region's URL. On submission, the operator is taken to the main results page, which features all search results and a persistent search bar, where they may move swiftly into the next search on completion. Each results page presents all data components of a snapshot.

An operator may toggle between available snapshots with the `◀ Forward` and `Backward ▶` nav buttons. World Factbook Entries can be copied with the `Copy` button on the page, and flags or banners can be downloaded with a simple left click.

## Details
Eyebeast is a Python-based utility, with a flask framework, designed to run in a virtual environment, making casual queries to an sqlite3 database. A stock wsgi configuration file is provided.