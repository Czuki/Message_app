import argparse

def username_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="username")
    args = parser.parse_args()

    return args