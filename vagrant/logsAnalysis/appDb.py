#! /usr/bin/env python
# "Database code" for the DB Logs Analysis

import psycopg2
import StringIO

DBNAME = "news"


def get_answer(question):
    """Return all answer from the question"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    query = ""
    if question == 1:
        # 1. What are the most popular three articles of all time?
        query = "SELECT " \
                    "articles.title, " \
                    "COUNT(log.path) AS total " \
                "FROM " \
                    "articles LEFT JOIN log " \
                "ON articles.slug = substring(log.path, 10) " \
                "GROUP BY articles.title " \
                "ORDER BY total DESC " \
                "LIMIT 3;"
    elif question == 2:
        # 2. Who are the most popular article authors of all time?
        query = "SELECT authcle.name, COUNT(log.path) AS total " \
                "FROM " \
                    "(SELECT authors.name AS name, articles.slug AS slug " \
                    "FROM authors LEFT JOIN articles " \
                    "ON authors.id = articles.author " \
                    "GROUP BY authors.name, articles.slug) AS authcle " \
                "LEFT JOIN log ON authcle.slug = substring(log.path, 10) " \
                "GROUP BY authcle.name " \
                "ORDER BY total DESC;"
    elif question == 3:
        # 3. On which days did more than 1% of requests lead to errors?
        query = "SELECT " \
                    "to_char(date, 'FMMonth FMDD, YYYY'), " \
                    "err/total AS ratio " \
                "FROM " \
                    "(SELECT time::date AS date, " \
                        "COUNT(*) AS total, " \
                        "SUM((status != '200 OK')::int)::float AS err " \
                    "FROM log GROUP BY date) AS errors " \
                "WHERE err/total > 0.01;"
    else:
        return ""

    c.execute(query)
    result = c.fetchall()
    db.close()

    return result


def download_answer_as_text(question):
    """ Render SQL Query results to text string """
    answer = get_answer(int(question))
    strIO = StringIO.StringIO()
    for row in answer:
        for col in row:
            if isinstance(col, (str)):
                # Check type of string
                strIO.write('| {:50} '.format(col))
            elif isinstance(col, (int, long, float, complex)):
                # Check type of number
                strIO.write('| {:10} '.format(col))
            else:
                # type of date
                strIO.write('| {:%Y-%m-%d} '.format(col))
        strIO.write('|\n')
    strIO.seek(0)

    return strIO
