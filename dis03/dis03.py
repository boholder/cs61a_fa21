# https://inst.eecs.berkeley.edu/~cs61a/fa21/disc/disc03
import math


def is_prime(n):
    """Returns True if n is a prime number and False otherwise.
    最简单的递归，不需要保存总的中间结果（尾递归），
    也不需要保存特殊单步的结果（记忆化）

    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    """

    def divisible(num, k):
        if k == 1:
            return True
        elif num % k == 0:
            return False
        else:
            return divisible(num, k - 1)

    # from n/2 to 1
    return divisible(n, int(n / 2))


def hailstone(n):
    """Print out the hailstone sequence starting at n, and return the number of elements in the sequence.
    需要保存一个共同的中间结果，放在参数中（尾递归）
    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """

    def step(num, count=0):
        print(int(num))
        # n is even
        if num == 1:
            return count + 1
        elif num % 2 == 0:
            return step(num / 2, count + 1)
        elif num % 2 == 1:
            return step(3 * num + 1, count + 1)

    return step(n)


def add_digit(num, digit):
    """
    >>> add_digit(10,1)
    110
    >>> add_digit(0,9)
    9
    >>> add_digit(10,0)
    10
    >>> add_digit(12,1)
    112
    >>> add_digit(1,9)
    91
    """
    if digit == 0:
        return num
    elif num == 0:
        return digit
    else:
        if num % 10 == 0 or num == 1:
            exp = int(math.log(num, 10)) + 1
        else:
            exp = math.ceil(math.log(num, 10))

        return digit * pow(10, exp) + num


def merge(n1, n2):
    """ Merges two numbers by digit in decreasing order
    就像合并两个有序链表一样......但是往数字的第一位加位数可难了
    第一个和第三个分支执行的一样,但不能合并，因为要先判是否为0再比大小。
    >>> merge(31, 42)
    4321
    >>> merge(21, 0)
    21
    >>> merge (21, 31)
    3211
    """

    def merge_helper(num1, num2, result=0):
        def add_num1_tail():
            return merge_helper(num1 // 10, num2, add_digit(result, num1 % 10))

        def add_num2_tail():
            return merge_helper(num1, num2 // 10, add_digit(result, num2 % 10))

        if num1 == 0 and num2 == 0:
            return result
        elif num1 == 0:
            return add_num2_tail()
        elif num2 == 0 or num1 % 10 < num2 % 10:
            return add_num1_tail()
        else:
            return add_num2_tail()

    return merge_helper(n1, n2)
