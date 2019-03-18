import random
import string
import time
import datetime
import bcrypt


def random_id_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def check_ID(table, id):
    if id in table:
        return 1


def generate_random(table):
    id = random_id_generator(8, "AEIOSUMA23")
    while check_ID(table, id):
        id = random_id_generator()
    return id


def get_submission_time():
    realtime = time.time()
    st = datetime.datetime.fromtimestamp(realtime).strftime('%Y-%m-%d %H:%M:%S')
    return st


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
