from psycopg2 import connect, OperationalError, ProgrammingError

username = "postgres"
password = "coderslab"
hostname = "localhost"

def sql_execute_and_close_cnx(sql, dbname=''):
    cnx = connect(user="postgres", password="coderslab", host="localhost", database=dbname)
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

def create_table_users():
    try:
        sql = """
        CREATE TABLE users 
        (
        id serial primary key,
        username varchar(255),
        hashed_password varchar(80)
        );
        """
        sql_execute_and_close_cnx(sql, 'workshop')
        print('Table Created')
    except ProgrammingError as err:
        print(err)
    except OperationalError as err:
        print(err)

def create_table_messages():
    try:
        sql = """
        CREATE TABLE messages 
        (
        id serial primary key,
        from_id integer,
        to_id integer,
        creation_date timestamp,
        foreign key (from_id) references users(id),
        foreign key (from_id) references users(id)
        );
        """
        sql_execute_and_close_cnx(sql, 'workshop')
        print('Table Created')
    except ProgrammingError as err:
        print(err)
    except OperationalError as err:
        print(err)

create_workshop_db()
create_table_users()
create_table_messages()
