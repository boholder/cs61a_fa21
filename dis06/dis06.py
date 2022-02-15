def filter_iter(iterable, fn):
    """
    >>> is_even = lambda x: x % 2 == 0
    >>> list(filter_iter(range(5), is_even)) # a list of the values yielded from the call to filter_iter
    [0, 2, 4]
    >>> all_odd = (2*y-1 for y in range(5))
    >>> list(filter_iter(all_odd, is_even))
    []
    >>> naturals = (n for n in range(1, 100))
    >>> s = filter_iter(naturals, is_even)
    >>> next(s)
    2
    >>> next(s)
    4
    """
    iterator = iter(iterable)
    while True:
        try:
            v = next(iterator)
        except StopIteration:
            break

        if fn(v):
            yield v


def merge(a, b):
    """
    >>> def sequence(start, step):
    ...     while True:
    ...         yield start
    ...         start += step
    >>> a = sequence(2, 3) # 2, 5, 8, 11, 14, ...
    >>> b = sequence(3, 2) # 3, 5, 7, 9, 11, 13, 15, ...
    >>> result = merge(a, b) # 2, 3, 5, 7, 8, 9, 11, 13, 14, 15
    >>> [next(result) for _ in range(10)]
    [2, 3, 5, 7, 8, 9, 11, 13, 14, 15]
    """
    # unwilling to accept that I need to store all appeared values in memory
    window = []
    index = 0
    while True:
        # just want to make sure to find smallest potential element between a and b
        # don't empty the window, remain 1
        if index > len(window) - 2:
            # take each one element from a and b
            window.extend(x for x in [next(a), next(b)] if x not in window)
            window.sort()
        yield window[index]
        index += 1


def is_prime(n):
    """Returns True if n is a prime number and False otherwise.
    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    """

    def helper(i):
        if i > (n ** 0.5):  # Could replace with i == n
            return True
        elif n % i == 0:
            return False
        return helper(i + 1)

    return helper(2)


def primes_gen(n):
    """Generates primes in decreasing order.
    >>> pg = primes_gen(7)
    >>> list(pg)
    [7, 5, 3, 2]
    """
    while n > 1:
        if is_prime(n):
            yield n
        n -= 1
