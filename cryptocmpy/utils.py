# -*- coding:utf-8 -*-
import re


def type_parser(v):
    v = str(v).strip()
    if v.lower() == ('none', 'null', 'n/a'):
        return None
    elif v.lower() in ('true', 'false'):
        return v.lower() == 'true'
    else:
        try:
            return int(v) if float(v).is_integer() else float(v)
        except (ValueError, TypeError):
            pass
        return v


def snake_case(word):
    """Make an underscored, lowercase form from the expression in the string.

    >>> snake_case("DeviceType")
    'device_type'

    :param str word: the word to be converted to snake case.
    :return str: the word converted to snake case.
    """
    word = re.sub(r'([A-Z])', r'_\1', word.strip()).lower()
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    return word.replace('-', '_').strip('_')
