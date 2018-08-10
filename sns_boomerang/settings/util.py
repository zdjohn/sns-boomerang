import re
import hashlib


def letters_and_numbers_only(text):
    regex_pattern = '^[a-z0-9]+(-[a-z0-9]+)*$'
    p = re.compile(regex_pattern)
    return not p.match(text) is None


def compute_hash(*args):
    m = hashlib.md5()
    m.update(''.join(args).encode('utf-8'))
    return m.hexdigest()