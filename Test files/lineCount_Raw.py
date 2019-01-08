from itertools import (takewhile, repeat)  # Used to count lines in file quickly
from timeit import default_timer as timer

from functools import partial

# Target file location
loc = "F:\\Dtan Temp\\ForChrisDiggle\\Interesting CSV\\6.1 Slow discharge 2.csv"


# Reads the file as raw binary. Ends up being pretty freaking fast
def rawInCount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(2048 * 2048) for _ in repeat(None)))
    return sum(buf.count(b'\n') for buf in bufgen)


def functools(filename):  # This is the one I ended up using
    buffer = 2 ** 16
    with open(filename) as f:
        return sum(x.count('\n') for x in iter(partial(f.read, buffer), ''))


start = timer()
print(rawInCount(loc))
end = timer()
print(end - start)  # Time in seconds, e.g. 5.38091952400282

start = timer()
print(functools(loc))
end = timer()
print(end - start)  # Time in seconds, e.g. 5.38091952400282
