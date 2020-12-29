import argparse
import clcrypto
from models import Messages, User
from psycopg2 import connect

def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument("-u", "--username", help="username")
    parser_.add_argument("-p", "--password", help="password")
    parser_.add_argument("-t", "--to", help="to_user")
    parser_.add_argument("-s", "--send", help="message", nargs='+')
    parser_.add_argument("-l" "--list", help="msg_list", action="store_true")
    args_ = parser_.parse_args()

    return parser_, args_

if __name__ == '__main__':

    parser, args = create_parser()

    cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
    cursor = cnx.cursor()
    cnx.autocommit = True

    username, password, to_user, msg_text, msg_list = tuple(vars(args).values())

    user_choice_key = [bool(arg) for arg in vars(args).values()]
    list_msg_key = [True, True, False, False, True]
    send_msg_key = [True, True, True, True, False]

    if user_choice_key == list_msg_key:
        current_user = User.load_user_by_username(cursor, username)
        if current_user:
            if clcrypto.check_password(password, current_user.hashed_password):
                print(f'Message list for user: {username}')
                msg_list = Messages.load_all_messages(cursor, current_user.id)

                for msg in msg_list:
                    from_user = User.load_user_by_id(cursor, msg.from_id)
                    print(f'{msg.id} -- {msg.text} -- From: {from_user.username} -- Date: {msg.creation_date}')
            else:
                print('Incorrect password')

    elif user_choice_key == send_msg_key:
        current_user = User.load_user_by_username(cursor, username)
        receiving_user = User.load_user_by_username(cursor, to_user)
        to_user_id = receiving_user.id

        print(to_user_id)
        if current_user:
            if clcrypto.check_password(password, current_user.hashed_password):
                print(type(msg_text))
                print(msg_text)
                message = Messages(current_user.id, to_user_id, ' '.join(msg_text))
                message.save_to_db(cursor)

