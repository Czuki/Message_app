from psycopg2 import connect, OperationalError, ProgrammingError

username = ''
password = ''
hostname = ''

def connect_to_db(database=''):
    cnx = connect(user=username, password=password, host=hostname, database=database)
    cnx.autocommit = True
    cursor = cnx.cursor()
    return cursor

def execute_sql(sql,database=''):
    with connect_to_db(database) as cursor:
        cursor.execute(sql)

def create_workshop_db():
    try:
        sql = "CREATE DATABASE workshop"
        execute_sql(sql)
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
        execute_sql(sql, 'workshop')
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
        text varchar(200),
        foreign key (from_id) references users(id) ON DELETE CASCADE,
        foreign key (from_id) references users(id) ON DELETE CASCADE
        );
        """
        execute_sql(sql, 'workshop')
        print('Table Created')
    except ProgrammingError as err:
        print(err)
    except OperationalError as err:
        print(err)


create_workshop_db()
create_table_users()
create_table_messages()
