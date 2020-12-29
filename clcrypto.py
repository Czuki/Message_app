import hashlib
import random
import string


def hash_password(password, salt=None):
    """
    Hashes the password with salt as an optional parameter.
    If salt is not provided, generates random salt.
    If salt is less than 16 chars, fills the string to 16 chars.
    If salt is longer than 16 chars, cuts salt to 16 chars.
    :param str password: password to hash
    :param str salt: salt to hash, default None
    :rtype: str
    :return: hashed password
    """

    if salt == None or salt == "":
        salt = generate_salt()

    salt = salt + ("a" * (16 - len(salt))) if len(salt) < 16 else salt[:16]
    t_sha = hashlib.sha256()
    t_sha.update(salt.encode('utf-8') + password.encode('utf-8'))

    return salt + t_sha.hexdigest()




def check_password(pass_to_check, hashed):
    """
    Checks the password.
    The function does the following:
        - gets the salt + hash joined,
        - extracts salt and hash,
        - hashes `pass_to_check` with extracted salt,
        - compares `hashed` with hashed `pass_to_check`.
        - returns True if password is correct, or False. :)
    :param str pass_to_check: not hashed password
    :param str hashed: hashed password
    :rtype: bool
    :return: True if password is correct, False elsewhere
    """
    salt = hashed[:16]
    hash_to_check = hashed[16:]
    new_hash = hash_password(pass_to_check, salt)

    return new_hash[16:] == hash_to_check

def generate_salt():
    """
    Generates a 16-character random salt.
    :rtype: str
    :return: str with generated salt
    """
    salt = ""
    for i in range(0, 16):
        salt += random.choice(string.ascii_lowercase + string.ascii_uppercase)

    return salt

