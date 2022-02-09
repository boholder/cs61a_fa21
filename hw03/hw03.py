from operator import sub, mul

HW_SOURCE_FILE = __file__


def num_eights(pos):
    """Returns the number of times 8 appears as a digit of pos.

    >>> num_eights(3)
    0
    >>> num_eights(8)
    1
    >>> num_eights(88888888)
    8
    >>> num_eights(2638)
    1
    >>> num_eights(86380)
    2
    >>> num_eights(12345)
    0
    """

    def helper(num, count=0):
        if num == 0:
            return count
        elif num % 10 == 8:
            return helper(num // 10, count + 1)
        else:
            return helper(num // 10, count)

    return helper(pos)


def pingpong(n):
    """Return the nth element of the ping-pong sequence.
    一个相互递归！
    >>> pingpong(8)
    8
    >>> pingpong(10)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    -2
    >>> pingpong(30)
    -2
    >>> pingpong(68)
    0
    >>> pingpong(69)
    -1
    >>> pingpong(80)
    0
    >>> pingpong(81)
    1
    >>> pingpong(82)
    0
    >>> pingpong(100)
    -6
    """

    def pos_count(num, index):
        if index == n:
            return num
        elif index % 8 == 0 or num_eights(index):
            return neg_count(num - 1, index + 1)
        else:
            return pos_count(num + 1, index + 1)

    def neg_count(num, index):
        if index == n:
            return num
        elif index % 8 == 0 or num_eights(index):
            return pos_count(num + 1, index + 1)
        else:
            return neg_count(num - 1, index + 1)

    return pos_count(1, 1)


def missing_digits(n):
    """Given a number a that is in sorted, non-decreasing order,
    return the number of missing digits in n. A missing digit is
    a number between the first and last digit of a that is not in n.
    >>> missing_digits(1248) # 3, 5, 6, 7
    4
    >>> missing_digits(19) # 2, 3, 4, 5, 6, 7, 8
    7
    >>> missing_digits(1122) # No missing numbers
    0
    >>> missing_digits(123456) # No missing numbers
    0
    >>> missing_digits(3558) # 4, 6, 7
    3
    >>> missing_digits(35578) # 4, 6
    2
    >>> missing_digits(12456) # 3
    1
    >>> missing_digits(16789) # 2, 3, 4, 5
    4
    >>> missing_digits(4) # No missing numbers between 4 and 4
    0
    """

    def helper(num, digit, count=0):
        if num == 0:
            return count
        elif num % 10 == digit:
            return helper(num // 10, digit, count)
        elif num % 10 == digit - 1:
            return helper(num // 10, num % 10, count)
        else:
            return helper(num, digit - 1, count + 1)

    return helper(n // 10, n % 10)


def ascending_coin(coin):
    """Returns the next ascending coin in order.
    >>> ascending_coin(1)
    5
    >>> ascending_coin(5)
    10
    >>> ascending_coin(10)
    25
    >>> ascending_coin(2) # Other values return None
    """
    if coin == 1:
        return 5
    elif coin == 5:
        return 10
    elif coin == 10:
        return 25


def descending_coin(coin):
    """Returns the next descending coin in order.
    >>> descending_coin(25)
    10
    >>> descending_coin(10)
    5
    >>> descending_coin(5)
    1
    >>> descending_coin(2) # Other values return None
    """
    if coin == 25:
        return 10
    elif coin == 10:
        return 5
    elif coin == 5:
        return 1


def count_coins_without_optimal(change):
    """Return the number of ways to make change using coins of value of 1, 5, 10, 25.
    没有优化。（求组合数）
    比例题再复杂一点，需要辅助函数来决定下一个可选步数。
    http://composingprograms.com/pages/17-recursive-functions.html
    和教材最后的例题思路相同，对于每次迭代，结果由两部分组成：
    (划分n, 直到{下一个可选的步数}步数) 加上 (划分n-m, 直到m步数)

    这个{下一个步数}在1~k问题里是k-1，在这个硬币问题里是descending_coin(coin)。

    >>> count_coins_without_optimal(5)
    2
    >>> count_coins_without_optimal(10)
    4
    >>> count_coins_without_optimal(15)
    6
    >>> count_coins_without_optimal(20)
    9
    >>> count_coins_without_optimal(100) # How many ways to make change for a dollar?
    242
    >>> count_coins_without_optimal(200)
    1463
    """

    def rec(n, coin):
        # （上次传来的下一面值）没有下一个面值了
        if coin is None:
            return 0
        # 正好分完，算一种情况
        elif n == 0:
            return 1
        # 上一次传来的 n - coin是负数
        elif n < 0:
            return 0
        else:
            return rec(n - coin, coin) + rec(n, descending_coin(coin))

    return rec(change, 25)


def count_coins_with_tail_recursion(change):
    """Return the number of ways to make change using coins of value of 1, 5, 10, 25.
    引入尾递归优化。
    在非树型递归中，迭代只有一个发展方向，不存在这个问题。
    在树型递归中，下一次调用的迭代是什么含义？

    根据上面没优化的实现，在这类划分（求组合数）的问题中，
    总是能把多个子树（选择）调整为两个子树（选择），因此在尾递归中：

    下一次迭代代表 (划分n, 直到{下一个可选的步数}步数)，
    而传入的count参数则加上了 (划分n-m, 直到m步数) 的结果，
    反过来也对。

    >>> count_coins_with_tail_recursion(5)
    2
    >>> count_coins_with_tail_recursion(10)
    4
    >>> count_coins_with_tail_recursion(15)
    6
    >>> count_coins_with_tail_recursion(20)
    9
    >>> count_coins_with_tail_recursion(100) # How many ways to make change for a dollar?
    242
    >>> count_coins_with_tail_recursion(200)
    1463
    """

    def rec(n, coin, count=0):
        # （上次传来的下一面值）没有下一个面值了
        if coin is None:
            return count  # (+ 0)
        # 正好分完，算一种情况
        elif n == 0:
            return 1 + count
        # 上一次传来的 n - coin是负数
        elif n < 0:
            return count  # (+ 0)
        else:
            # 两个选择可以前后调换
            # return rec(n, descending_coin(coin), count + rec(n - coin, coin))
            return rec(n - coin, coin, count + rec(n, descending_coin(coin)))

    return rec(change, 25)


def count_coins(change):
    """Return the number of ways to make change using coins of value of 1, 5, 10, 25.
    这种划分问题是求组合，走格子问题求排列。
    分硬币思路：
    这确实也是个划分的问题，划分的计算是组合公式(C(m,n))：
    The number of ways to partition n using integers up to {biggest_proper_value:m} equal:
    the number of ways to partition n-m using integers up to m, and
    the number of ways to partition n using integers up to {next_smaller_value}.
    这个问题的组合由1，5，10，25四种物体组成，是离散的，比逐个减一的连续的题目复杂。

    举例 分15 共6种:
    15 1-cent coins
    10 1-cent, 1 5-cent coins
    5 1-cent, 2 5-cent coins
    5 1-cent, 1 10-cent coins
    3 5-cent coins
    1 5-cent, 1 10-cent coin

    - 选10 -> 剩5，能继续选10，5，1 -> 2种
    - 选5 -> 剩10，能继续选5，1 -> (1+2)种
        - 选5 -> 剩5，能继续选5，1 -> 2种
        - 选1 -> 剩9，能继续选1 -> 1种
    - 选1 -> 剩14，能继续选1 -> 1种

    选不同种类的硬币累加结果，但限制了后续迭代的硬币选择，
    这样才不会变成排列(A)而重复计算组合。

    优化：
    这是个树型递归，意味着可以记忆化优化。
    它要计算组合数，所以同时可以尾递归。

    反思：
    写这种复杂递归题目，应该在纸上画很久再下手写出代码。
    树型递归还要弄明白什么记忆化的数据结构是什么样子。

    >>> count_coins(5)
    2
    >>> count_coins(10)
    4
    >>> count_coins(15)
    6
    >>> count_coins(20)
    9
    >>> count_coins(100) # How many ways to make change for a dollar?
    242
    >>> count_coins(200)
    1463
    """
    # memoization，
    # 这里我掉坑了，应该意识到：
    # 不同最大面值限制下的同一个数字的划分是不同的，
    # 所以应该每个最大面值限制都有自己的独立记忆化数组。
    # 例：数字10在最大面值限制为10，5，1的情况下划分组合数分别为4，3，1
    memory = {1: [None] * (change + 1),
              5: [None] * (change + 1),
              10: [None] * (change + 1),
              25: [None] * (change + 1)}
    for line in memory.values():
        line[0] = 1
        line[1] = 1

    # 基本是和记忆化操作相关的wrapper
    def memo(num, coin_limit=25):
        if memory.get(coin_limit)[num] is None:
            # 计算累加
            memory.get(coin_limit)[num] = accumulate(num, floor(coin_limit, num))

        return memory.get(coin_limit)[num]

    # 把硬币面值降到目前num能接受的范围
    # 这个函数帮忙省略了一些base case
    def floor(coin, num):
        if num < coin:
            return floor(descending_coin(coin), num)
        else:
            return coin

    def accumulate(num, coin, count=0):
        """真正计算递归的函数
        依次调用rec()向下移动面值，累加不同面值选择的划分组合
        num: 当前处理的num
        coin: 在本次准备处理的面值
        count: 积累的累加
        """
        if coin is None:
            return count
        else:
            return accumulate(num, descending_coin(coin), count + memo(num - coin, coin))

    return memo(change)


def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.
    抄的。
    难点在不给函数赋名字的前提下调用函数，
    调用必须需要一个名字，于是问题变形成了：
    如何绕过def给函数命名。

    前面柯里化只是为了分两步调用，
    这里巧妙的点在于后面的lambda函数把自身作为参数传给自身，以命名。

    >>> make_anonymous_factorial()(5)
    120
    """
    return (lambda f: lambda x: f(f, x))(lambda f, x: 1 if x == 0 else mul(x, f(f, sub(x, 1))))
