import random
import string


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