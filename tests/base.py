"""
Collection of base classes/methods etc. to supplement the unit test(s)
"""


def all_instance_of(iterable, type_to_be_checked):
    return all([isinstance(o, type_to_be_checked) for o in iterable])
