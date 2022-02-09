from functools import reduce

HW_SOURCE_FILE = __file__


def summation(n, term):
    """Return the sum of numbers 1 through n (including n) wíth term applied to each number.
    Implement using recursion!

    >>> summation(5, lambda x: x * x * x) # 1^3 + 2^3 + 3^3 + 4^3 + 5^3
    225
    >>> summation(9, lambda x: x + 1) # 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10
    54
    >>> summation(5, lambda x: 2**x) # 2^1 + 2^2 + 2^3 + 2^4 + 2^5
    62
    >>> # Do not use while/for loops!
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'summation',
    ...       ['While', 'For'])
    True
    """
    assert n >= 1

    def helper(num, func, summary=0):
        if num == 0:
            return summary
        else:
            return helper(num - 1, func, summary + func(num))

    return helper(n, term)


def pascal(row, column):
    """Returns the value of the item in Pascal's Triangle 
    whose position is specified by row and column.
    这个公式：
    p(r,c) = p(r-1,c-1) + p(r-1,c)
    可以记忆化，
    因为 p(r-1,c-1) 和 p(r-1,c) 都需要计算他俩上面中间的那个数。

    >>> pascal(0, 0)
    1
    >>> pascal(1, 1)
    1
    >>> pascal(0, 5)	# Empty entry; outside of Pascal's Triangle
    0
    >>> pascal(3, 2)	# Row 3 (1 3 3 1), Column 2
    3
    >>> pascal(4, 2)     # Row 4 (1 4 6 4 1), Column 2
    6
    """

    # memoization
    grid = [[None for _ in range(column + 1)] for _ in range(row + 1)]

    def memo(r, c):
        # out of triangle
        if r < 0 or c < 0 or r < c:
            return 0

        # edge case
        elif r == 0 or c == 0:
            return 1

        if grid[r][c] is None:
            grid[r][c] = rec(r, c)

        return grid[r][c]

    def rec(r, c):
        return memo(r - 1, c - 1) + memo(r - 1, c)

    return memo(row, column)


def paths(m, n):
    """Return the number of paths from one corner of an
    M by N grid to the opposite corner.
    公式：
    P(m,n) = P(m-1,n) + P(m,n-1)
    需要记忆化，因为上方和右方的计算都需要计算中间的那个数。

    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """

    # memoization
    grid = [[None for _ in range(n + 1)] for _ in range(m + 1)]

    def memo(r, c):
        # edge case
        if r == 0 or c == 0:
            return 0
        elif r == 1 or c == 1:
            return 1
        else:
            if grid[r][c] is None:
                grid[r][c] = rec(r, c)
            return grid[r][c]

    def rec(r, c):
        return memo(r - 1, c) + memo(r, c - 1)

    return memo(m, n)


def couple(s, t):
    """Return a list of two-element lists in which the i-th element is [s[i], t[i]].

    >>> a = [1, 2, 3]
    >>> b = [4, 5, 6]
    >>> couple(a, b)
    [[1, 4], [2, 5], [3, 6]]
    >>> c = ['c', 6]
    >>> d = ['s', '1']
    >>> couple(c, d)
    [['c', 's'], [6, '1']]
    """
    assert len(s) == len(t)

    return [[s[i], t[i]] for i in range(len(s))]


def coords(fn, seq, lower, upper):
    """
    Reflect: What are the drawbacks to the one-line answer, in terms of using computer resources?
    python是先过filter再应用map，
    那缺点只能是诸如iter式所以串行执行，fn(x)计算多次这样的了。

    >>> seq = [-4, -2, 0, 1, 3]
    >>> fn = lambda x: x**2
    >>> coords(fn, seq, 1, 9)
    [[-2, 4], [1, 1], [3, 9]]
    """

    return [[x, fn(x)] for x in seq if lower <= fn(x) <= upper]


def riffle(deck):
    """Produces a single, perfect riffle shuffle of DECK, consisting of
    DECK[0], DECK[M], DECK[1], DECK[M+1], ... where M is position of the
    second half of the deck.  Assume that len(DECK) is even.

    >>> riffle([3, 4, 5, 6])
    [3, 5, 4, 6]
    >>> riffle(range(20))
    [0, 10, 1, 11, 2, 12, 3, 13, 4, 14, 5, 15, 6, 16, 7, 17, 8, 18, 9, 19]
    """

    mid = int(len(deck) / 2)
    # 显然不是题目推荐的利用奇偶的解法
    return list(reduce(list.__add__, [[deck[i], deck[i + mid]] for i in range(mid)]))
