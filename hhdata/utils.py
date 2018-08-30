from django.db import connection

def exec_sql(path):
    fd = open(path, 'r')
    string = fd.read()
    build = string.replace('\n',' ')
    return my_custom_sql(build)

def my_custom_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = dictfetchall(cursor)
    return row

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
