def count_stair_ways(n):
    """Returns the number of ways to climb up a flight of
    n stairs, moving either 1 step or 2 steps at a time.

    https://inst.eecs.berkeley.edu/%7Ecs61a/fa21/disc/disc04/#q1-count-stair-ways
    树型递归，有限的情况（1或2，两种情况）
    走格子问题，求排列（而非（划分题目的）求组合）

    >>> count_stair_ways(2)
    2
    >>> count_stair_ways(4)
    5
    """

    # 走0步和1步楼梯都只有一种方法
    if n == 0:
        return 1
    elif n < 0:
        return 0
    else:
        # 两种情况相加
        return count_stair_ways(n - 1) + count_stair_ways(n - 2)


def count_k(n, k):
    """ Counts the number of paths up a flight of n stairs
    when taking up to and including k steps at a time.
    树型递归，连续的情况，求排列。
    多于两种情况，当前n的结果为
        for i in range(1,k):
            count += count_k(n-i, k)
    找不到压缩为两种情况的办法。

    >>> count_k(0, 2)
    1
    >>> count_k(1, 2)
    1
    >>> count_k(2, 2)
    2
    >>> count_k(3, 3) # 3, 2 + 1, 1 + 2, 1 + 1 + 1
    4
    >>> count_k(4, 4)
    8
    >>> count_k(10, 3)
    274
    >>> count_k(300, 1) # Only one step at a time
    1
    """

    if n == 0:
        return 1
    elif n < 0:
        return 0
    elif k == 0:
        return 0
    else:
        return sum([count_k(n - i, k) for i in range(1, k + 1)])
