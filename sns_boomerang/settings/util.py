import re


def letters_and_numbers_only(text):
    regex_pattern = '^[a-z0-9]+(-[a-z0-9]+)*$'
    p = re.compile(regex_pattern)
    return not p.match(text) is None
