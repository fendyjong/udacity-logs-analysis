# Udacity - Intro to Programming Nanodegree -  Logs Analysis Project

## Description
This Logs Analysis project is intended to test my understanding of PostgreSQL and Python programming.

Technology used:
- __Vagrant__ to isolate development environment
- __Flask framework__ for the web display
- __PostgreSQL__ for the database

## Setup Project
### Enter vagrant environment
    $ cd vagrant
    $ vagrant up && vagrant ssh

### Import newsdata.sql to psql
    $ psql -d news -f newsdata.sql

### Start Development Server inside vagrant environment
    $ cd /vagrant/logsAnalysis
    $ export FLASK_APP=index.py
    $ flask run --host=0.0.0.0

### OPTIONAL: Debug Mode
Add the following line before __"flask run --host=0.0.0.0"__ to display error code in the web

    $ export FLASK_DEBUG=1
