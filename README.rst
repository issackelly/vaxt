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

There are several things not specified in this document that are important to getting started. If you're trying this and you have specific issues, file an issue and/or a merge request and maybe I'll have time to help.

* Knowing about docker containers
* Knowing how to configure/extend postgresql
* Knowing about python environments

These notes are currently more for me, so I remember in 6 months what I did, than they are general-purpose docs.

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

Running from Docker
~~~~~~~~~~~~~~~~~~~

While I think the "ideal" state for this is a single-command getting started guide, that's not what I spent my day on, so it's still BYO.

This assumes that you have your timescale db running locallaly, that it's called "vaxt" and that a user with username "user" and password "password" can connect to it. These are probably bad assumptions for your setup.

::

    cd backend;
    docker build .
    ...
     ---> 247cf92dd90d
    Successfully built 247cf92dd90d
    docker run --network=host -it --env DATABASE_URL=postgres://user:pass@127.0.0.1/vaxt 247cf