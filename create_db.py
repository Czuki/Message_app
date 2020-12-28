from psycopg2 import connect, OperationalError, ProgrammingError

username = "postgres"
password = "coderslab"
hostname = "localhost"

def sql_execute_and_close_cnx(sql):
    cnx = connect(user="postgres", password="coderslab", host="localhost")
    cursor = cnx.cursor()
    cnx.autocommit = True
    cursor.execute(sql)
    cursor.close()
    cnx.close()

def create_workshop_db():
    try:
        sql = "CREATE DATABASE workshop"
        sql_execute_and_close_cnx(sql)
        print('Database Created')
    except ProgrammingError as err:
        print(err)
    except OperationalError as err:
        print(err)

# def create_table():
#     try:
#         sql = "CREATE TABLE "
create_workshop_db()
