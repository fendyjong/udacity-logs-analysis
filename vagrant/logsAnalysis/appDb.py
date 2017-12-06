# "Database code" for the DB Logs Analysis

import psycopg2

DBNAME = "news"


def get_answer(question):
    """Return all answer from the question"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    query = ""
    if question == 1:
        # 1. What are the most popular three articles of all time?
        query = "SELECT articles.title, count(log.path) AS total FROM articles LEFT JOIN log ON articles.slug = substring(log.path, 10) GROUP BY articles.title ORDER BY total DESC;"
    elif question == 2:
        # 2. Who are the most popular article authors of all time?
        query = "SELECT authcle.name, count(log.path) AS total FROM (SELECT authors.name AS name, articles.slug AS slug FROM authors LEFT JOIN articles ON authors.id = articles.author GROUP BY authors.name, articles.slug) AS authcle LEFT JOIN log ON authcle.slug = substring(log.path, 10) GROUP BY authcle.name ORDER BY total DESC;"
    elif question == 3:
        # 3. On which days did more than 1% of requests lead to errors?
        query = "SELECT errors.date, errors.total FROM (SELECT time::date AS date, COUNT(status) AS total FROM log WHERE log.status = '404 NOT FOUND' GROUP BY date ORDER BY total DESC) AS errors, (SELECT ROUND(0.01 * COUNT(log)) AS total FROM log) AS log_count WHERE errors.total > log_count.total;"
    else:
        return ""

    c.execute(query)
    result = c.fetchall()
    db.close()

    return result


def download_answer_as_text(question):
    answer = get_answer(int(question))

    filename = 'download/answer-{}.txt'.format(question)
    with open(filename, 'w') as f:
        for row in answer:
            for col in row:
                if isinstance(col, (str)):
                    f.write('| {:50} '.format(col))
                elif isinstance(col, (int, long, float, complex)):
                    f.write('| {:10} '.format(col))
                else:
                    f.write('| {:%Y-%m-%d}      '.format(col))
            f.write('|\n')

    return filename
