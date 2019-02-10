# Logs Analysis Project

## Table of Contents

* [Description](#description)
* [Getting Started](#gettingstarted)
* [Views](#views)

<a name="description"><a>
## Description

The Log Analysis project is a Udacity project that is part of the Full Stack Web Developer Nanodegree.

The project is a reporting tool that uses information from a database containing newspaper articles and the web server log for a website. The reporting tool tracks the following:

    1) The most popular three articles of all time.

    2) The most popular article authors of all time.

    3) The days more than 1% of requests led to errors.
<a name="gettingstarted"><a>
## Getting Started

### Prerequisites
VirtualBox and Vagrant to create a Linux-based virtual machine (VM)

PostgreSQL

Psycopg


### How to Run the Project
1. Make sure you have installed VirtualBox and Vagrant (to launch a Linux-based virtual machine (VM)); PostgreSQL; and Psycopg
2. In the command line `cd` into the `vagrant` file
3. In the command line type `vagrant up` in order to bring the VM online
4. In the command line type `vagrant ssh` in order to log into the VM
5. Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
6. Unzip the data
7. Inside is a file called `newsdata.sql`. Put this file into the vagrant directory
8. To load the data, `cd` into the `vagrant` directory, then, into the command line, type `psql -d news -f newsdata.sql` 
9. To launch the program, type `python newsdb.py` or `python3 newsdb.py` into the command line

<a name="views"><a>
### Views
I used two views to answer the query, "The days more than 1% of requests led to errors." 

```CREATE view serverrequests as
SELECT date(time),
count(*) as dailyrequests,
count(case when status != '200 OK' THEN 1 end) as dailyerrors
FROM log
GROUP by date```

```CREATE view errorpct as
SELECT date, ((dailyerrors/dailyrequests::decimal) *100) as percent
FROM serverrequests```


