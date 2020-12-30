import argparse
import clcrypto
from models import Messages, User
from psycopg2 import connect


#Lists of bool values to determine what arguments were used during console execute
LIST_MSG_KEY = [True, True, False, False, True]
SEND_MSG_KEY = [True, True, True, True, False]
#---------------------------------------------------------


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument("-u", "--username", help="username")
    parser_.add_argument("-p", "--password", help="password")
    parser_.add_argument("-t", "--to", help="to_user")
    parser_.add_argument("-s", "--send", help="message", nargs='+')
    parser_.add_argument("-l" "--list", help="msg_list", action="store_true")
    args_ = parser_.parse_args()

    return parser_, args_


def list_messages(cursor, args):
    current_user = User.load_user_by_username(cursor, args.username)
    if current_user:
        if clcrypto.check_password(args.password, current_user.hashed_password):
            print(f'Message list for user: {args.username}')
            msg_list = Messages.load_all_messages(cursor, current_user.id)
            for msg in msg_list:
                from_user = User.load_user_by_id(cursor, msg.from_id)
                print(f'{msg.id} -- {msg.text} -- From: {from_user.username} -- Date: {msg.creation_date}')
        else:
            print('Incorrect password')


def send_message(cursor, args):
    current_user = User.load_user_by_username(cursor, args.username)
    receiving_user = User.load_user_by_username(cursor, args.to)
    to_user_id = receiving_user.id
    if current_user:
        if clcrypto.check_password(args.password, current_user.hashed_password):
            message = Messages(current_user.id, to_user_id, ' '.join(args.send))
            message.save_to_db(cursor)


if __name__ == '__main__':

    parser, args = create_parser()

    cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
    cursor = cnx.cursor()
    cnx.autocommit = True

    user_choice_key = [bool(arg) for arg in vars(args).values()]

    if user_choice_key == LIST_MSG_KEY:
        list_messages(cursor, args)
    elif user_choice_key == SEND_MSG_KEY:
        send_message(cursor, args)
    else:
        parser.print_help()

    cnx.close()
