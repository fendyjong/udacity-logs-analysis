#Udacity - Intro to Programming Nanodegree -  Logs Analysis Project

##Enter vagrant environment
    $ cd vagrant
    $ vagrant up && vagrant ssh

##Import newsdata.sql to psql
- Unzip newsdata.zip
    $ psql -d news -f newsdata.sql

##Start development server inside vagrant
    $ cd /vagrant/logsAnalysis
    $ export FLASK_APP=index.py
    $ flask run --host=0.0.0.0

