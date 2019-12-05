

def chunk_iterable(iterable, chunk_size=500):
    current_chunk_size = 0
    current_chunk = []

    for item in iterable:
        current_chunk.append(item)
        current_chunk_size += 1

        if current_chunk_size == chunk_size:
            yield current_chunk
            current_chunk = []
            current_chunk_size = 0

    if current_chunk:
        yield current_chunk
