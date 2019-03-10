VAXT
----

Generic Time Series Data toolkit on timescaledb.

Vaxt translates as `time` in Azerbaijani. I chose this name by flipping through google translate for the word `time`.

Goals:

* Identify some patterns around using TimescaleDB
* Use the Django ORM and migrations for interacting with the database, presenting HTTP apis
* Write a generic interface to store ad-hoc data
* Grafana Compatible
* (Bonus) InfluxDB Compatable /write HTTP endpoint


Timescale Specific Things
~~~~~~~~~~~~~~~~~~~~~~~~~

Install Timescaledb

https://docs.timescale.com/v0.12/getting-started/installation/linux/installation-apt-ubuntu


::

    # Add our PPA
    sudo add-apt-repository ppa:timescale/timescaledb-ppa
    sudo apt-get update

    # To install for PG 10.2+
    sudo apt install timescaledb-postgresql-10

Configure Timescaledb with their tool, and create/configure the database

::

    timescaledb-tune
    createdb vaxt


