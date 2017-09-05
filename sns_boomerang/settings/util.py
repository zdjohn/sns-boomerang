import re


def letters_and_numbers_only(text):
    """
    a_b_c --> ok
    a-b-c --> ok
    a-_b --> not ok
    a--b --> not ok
    a__b --> not ok
    :param text:
    :return: sanitised
    """
    regex_pattern = '^[a-z0-9]+((-?|_?)[a-z0-9]+)*$'
    p = re.compile(regex_pattern)
    return not p.match(text) is None
