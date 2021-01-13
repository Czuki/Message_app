# Message_app

Small console based app that allows to add users to database and send messages between users.

## Required modules

psycopg2-binary==2.8.6

## Usage

Modify 'create_db.py' with your database username, password, hostname, and execute 'create_db.py' file to create required PostgreSQL database.


Add users with 'users_app.py' file


- python3 users_app.py -u "username" -p "password"


To change password for user

- python3 users_app.py -u "username" -p "password" -e -n "new_password"

To list all created users 

- python3 users_app.py -u "username" -p "password" -l

To delete user

- python3 users_app.py -u "username" -p "password" --delete

Execute file without arguments to see available commands


---

Sending Messages

- python3 message_app.py -u "username" -p "password" -t "receiver" -s "message"

Check Messages

- python3 message_app.py -u "username" -p "password" -l

