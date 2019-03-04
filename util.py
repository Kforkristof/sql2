import random
import string
import time
import datetime

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

print(get_submission_time())