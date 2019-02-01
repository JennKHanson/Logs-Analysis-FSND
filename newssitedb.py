# !/usr/bin/env python3

# Database code for the Udacity Log Analysis Project


import psycopg2

DBNAME = "news"


def get__popular_articles():
    """What are the most popular three articles of all time?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT title, count(*) as views
        FROM articles, log
        WHERE log.path LIKE '%' || articles.slug || '%'
        GROUP BY articles.title
        ORDER BY views desc limit 3
    """)
    popular_articles = c.fetchall()
    print("What are the most popular three articles of all time?")
    print(popular_articles)
    db.close()


def get_popular_authors():
    """Who are the most popular article authors of all time?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
    SELECT authors.name, count(*) as views
    FROM articles, authors, log
    WHERE log.path LIKE '%' || articles.slug || '%'
    and articles.author = authors.id
    GROUP BY authors.name
    ORDER BY views desc
    """)
    popular_authors = c.fetchall()
    print("Who are the most popular atricle authors of all time?")
    print(popular_authors)
    db.close()


def get_errors():
    """On which days did more than 1% of requests lead to errors?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
    CREATE view requests as
    SELECT date(time),
    count(*) as dailyrequests,
    count(case when status != '200 OK' THEN 1 end) as dailyerrors
    FROM log
    GROUP by date
    """)
    c.execute("""
    CREATE view errorpercent as
    SELECT date, ((dailyerrors/dailyrequests::decimal) *100) as percent
    FROM requests
    """)
    c.execute("""
    SELECT date, percent FROM errorpercent
    WHERE percent > 1
    """)
    errors = c.fetchall()
    print("On which days did more than 1 percent of requests lead to errors?")
    print(errors)
    db.close()
