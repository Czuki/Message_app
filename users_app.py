import argparse
import clcrypto
from models import User, Messages
from psycopg2 import connect, OperationalError, IntegrityError
import getpass

def check_pwd_len(password):
    while len(password) < 8:
        print('Password too short')
        password = getpass.getpass('New password: ')
    current_user.set_password(password)

def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument("-u", "--username", help="username")
    parser_.add_argument("-p", "--password", help="password")
    parser_.add_argument("-n", "--new_pass", help="new_pass")
    parser_.add_argument("-l", "--list", help="list users",action="store_true")
    parser_.add_argument("--delete", help="delete user", action="store_true")
    parser_.add_argument("-e", "--edit", help="edit user", action="store_true")
    args_ = parser_.parse_args()

    return parser_, args_


if __name__ == '__main__':

    parser, args = create_parser()

    cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
    cursor = cnx.cursor()
    cnx.autocommit = True

    username, password, new_pass, list_users, delete_user, edit_user = tuple(vars(args).values())

    user_choice_key = [bool(arg) for arg in vars(args).values()]
    edit_pass_key = [True, True, True, False, False, True]
    create_user_key = [True, True, False, False, False, False]
    delete_user_key = [True, True, False, False, True, False]

    if user_choice_key == edit_pass_key:
        current_user = User.load_user_by_username(cursor, username)
        if clcrypto.check_password(password, current_user.hashed_password):
            if len(new_pass) < 8:
                check_pwd_len(new_pass)
                print('password changed')
            current_user.save_to_db(cursor)
        else:
            print('Incorrect password')

    elif user_choice_key == create_user_key:
        current_user = User(username, password)
        if len(password) < 8:
            check_pwd_len(password)
        current_user.save_to_db(cursor)

    elif user_choice_key == delete_user_key:
        current_user = User(username, password)
        if clcrypto.check_password(password, current_user.hashed_password):
            current_user.delete(cursor)
        else:
            print('Incorrect password')

