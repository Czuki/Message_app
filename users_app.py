import argparse
import clcrypto
from models import User
from psycopg2 import connect
import getpass

#Lists of bool values to determine what arguments were used during console execute
EDIT_PASS_KEY = [True, True, True, False, False, True]
CREATE_USER_KEY = [True, True, False, False, False, False]
DELETE_USER_KEY = [True, True, False, False, True, False]
LIST_USERS_KEY = [True, True, False, True, False, False]
#---------------------------------------------------------


def check_pwd_len(password, current_user):
    """
    When password is too short
    provides safe console input
    for new password
    :param password: password that is too short
    :param current_user:
    :return: doesnt return a value, just sets a new password for current user
    """
    while len(password) < 8:
        print('Password too short')
        password = getpass.getpass('New password: ')
    current_user.set_password(password)


def create_parser():
    """
    Function wraps parser object creation
    and adds required arguments
    :return: parser and args objects
    """
    parser_ = argparse.ArgumentParser()
    parser_.add_argument("-u", "--username", help="username")
    parser_.add_argument("-p", "--password", help="password")
    parser_.add_argument("-n", "--new_pass", help="new_pass")
    parser_.add_argument("-l", "--list", help="list_users", action="store_true")
    parser_.add_argument("--delete", help="delete_user", action="store_true")
    parser_.add_argument("-e", "--edit", help="edit_user", action="store_true")
    args_ = parser_.parse_args()

    return parser_, args_


def pass_edit(cursor, args):
    """
    Loads user, checks password
    and enables setting new password
    :param cursor:
    :param args: parser console args
    """
    print('Password edit')
    current_user = User.load_user_by_username(cursor, args.username)
    if clcrypto.check_password(args.password, current_user.hashed_password):
        if len(args.new_pass) < 8:
            check_pwd_len(args.new_pass, current_user)
            print('Password changed')
        current_user.save_to_db(cursor)
    else:
        print('Incorrect password')


def create_user(cursor, args):
    """
    Creates new user if username is not taken
    :param cursor:
    :param args: parser console args
    """
    print('Creating user')
    current_user = User(args.username, args.password)
    if len(args.password) < 8:
        check_pwd_len(args.password, current_user)
    if current_user.save_to_db(cursor):
        print(f'User {args.username} created')


def delete_user(cursor, args):
    """
    Deletes current user
    :param cursor:
    :param args: parser console args
    """
    print('Deleting')
    current_user = User.load_user_by_username(cursor, args.username)
    if current_user:
        if clcrypto.check_password(args.password, current_user.hashed_password):
            current_user.delete(cursor)
            print(f'User {current_user.username} deleted')
        else:
            print('Incorrect password')


def list_users(cursor, args):
    """
    Prints list of all users
    :param cursor:
    :param args: parser console args
    """
    current_user = User.load_user_by_username(cursor, args.username)
    if current_user:
        if clcrypto.check_password(args.password, current_user.hashed_password):
            print('Users list:')
            print('ID.Username')
            print('-----------')
            for user in User.load_all_users(cursor):
                print(f'{user.id}.{user.username}')
            print('-----------')
        else:
            print('Incorrect password')


if __name__ == '__main__':

    parser, args = create_parser()

    cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
    cursor = cnx.cursor()
    cnx.autocommit = True

    user_choice_key = [bool(arg) for arg in vars(args).values()]

    if user_choice_key == EDIT_PASS_KEY:
        pass_edit(cursor, args)
    elif user_choice_key == CREATE_USER_KEY:
        create_user(cursor, args)
    elif user_choice_key == DELETE_USER_KEY:
        delete_user(cursor, args)
    elif user_choice_key == LIST_USERS_KEY:
        list_users(cursor, args)
    else:
        parser.print_help()

    cnx.close()
