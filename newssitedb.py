#!/usr/bin/env python3

# Database code for the Udacity Log Analysis Project


import psycopg2

DBNAME = "news"


def get_popular_articles():
    """What are the most popular three articles of all time?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT title, count(*) as views
        FROM articles, log
        WHERE log.status = '200 OK'
        AND log.path LIKE '%' || articles.slug || '%'
        GROUP BY articles.title
        ORDER BY views desc limit 3
    """)
    popular_articles = c.fetchall()
    print("\n 1. What are the most popular three articles of all time?")
    print("-" * 70)
    for article in popular_articles:
        print(" {} - {} views".format(article[0], article[1]))
    db.close()


def get_popular_authors():
    """Who are the most popular article authors of all time?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT authors.name, count(*) as views
        FROM articles, authors, log
        WHERE log.status = '200 OK'
        AND log.path LIKE '%' || articles.slug || '%'
        AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views desc
        """)
    popular_authors = c.fetchall()
    print("\n 2. Who are the most popular article authors of all time?")
    print("-" * 70)
    for author in popular_authors:
        print(" {} - {} article views".format(author[0], author[1]))
    db.close()


def get_errors():
    """On which days did more than 1% of requests lead to errors?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        CREATE view serverrequests as
        SELECT date(time),
        COUNT(*) as dailyrequests,
        COUNT(case when status != '200 OK' THEN 1 end) as dailyerrors
        FROM log
        GROUP by date
        """)
    c.execute("""
        CREATE view errorpct as
        SELECT date, ((dailyerrors/dailyrequests::decimal(10,2)) *100)
        as percent
        FROM serverrequests
        """)
    c.execute("""
        SELECT to_char("date", 'Mon dd, yyyy'), round(percent, 2) FROM errorpct
        WHERE percent > 1
        """)
    errors = c.fetchall()
    print("""\n
        3. On which day(s) did more than 1 percent of requests lead to errors?
        """)
    print("-" * 70)
    for error in errors:
        print(" {} - {}% errors".format(error[0], error[1]))
    db.close()


get_popular_articles()
get_popular_authors()
get_errors()
