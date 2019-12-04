from itertools import zip_longest


def chunk_iterable(iterable, chunk_size=500):
    args = [iter(iterable)] * chunk_size
    return zip_longest(*args)
