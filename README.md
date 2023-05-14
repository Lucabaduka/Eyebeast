# Eyebeast - Eldritch Archival Utility
##### A utility for region-builders, defenders, and researchers to recover region data on NationStates.
![Eyebeast v1.0.6](https://img.shields.io/badge/Eyebeast-v1.0.6-0099ff) ![Flask v2.1.3](https://img.shields.io/badge/Flask-v2.1.3-0099ff) ![Python v3.9](https://img.shields.io/badge/Python-v3.9-0099ff)

## Overview
Eyebeast allows you to browse up to six months of data for a given region on NationStates, organised into snapshots of how the region looked at a particular point in time. In the main production application, these snapshots are taken as a component of Nightly, Calamity Refuge's main maintenance and processing routine.

Eyebeast's component of that routing (mining) runs once a week from, from midnight to 12:00 noon, Pacific time, every Wednesday. After a snapshot reaches six months of age, its applicable flags and banners are pruned from the server, and its record is removed from the database.

## Usage
The splash page is a simple search box, where an operator may input a region name, or a region's URL. On submission, the operator is taken to the main results page, which features all search results and a persistent search bar, where they may move swiftly into the next search on completion. Each results page presents all data components of a snapshot.

An operator may toggle between available snapshots with the `◀ Forward` and `Backward ▶` nav buttons. World Factbook Entries can be copied with the `Copy` button on the page, and flags or banners can be downloaded with a simple left click.

## Details
Eyebeast is a Python-based utility, with a flask framework, designed to run in a virtual environment, making casual queries to an sqlite3 database. A stock wsgi configuration file is provided.