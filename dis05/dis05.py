from lab05.lab05 import is_leaf, branches, tree, label


def height(t):
    """Return the height of a tree.
    >>> height(tree(1))
    0
    >>> t = tree(3, [tree(5, [tree(1)]), tree(2)])
    >>> height(t)
    2
    >>> t = tree(3, [tree(1), tree(2, [tree(5, [tree(6)]), tree(1)])])
    >>> height(t)
    3
    """
    if is_leaf(t):
        return 0
    else:
        return max([height(b) for b in branches(t)]) + 1


def max_path_sum(t):
    """Return the maximum path sum of the tree.

    >>> t = tree(1, [tree(5, [tree(1), tree(3)]), tree(10)])
    >>> max_path_sum(t)
    11
    """
    if is_leaf(t):
        return int(label(t))
    else:
        return max([max_path_sum(b) for b in branches(t)]) + int(label(t))


def find_path(t, x):
    """
    >>> t = tree(2, [tree(7, [tree(3), tree(6, [tree(5), tree(11)])] ), tree(15)])
    >>> find_path(t, 5)
    [2, 7, 6, 5]
    >>> find_path(t, 10)  # returns None
    """

    def path(node, target, way=[]):
        if target == label(node):
            return way + [label(node)]

        # dead end
        if is_leaf(node):
            return None
        else:
            optional = list(
                filter(lambda p: p,
                       [path(b, target, way + [label(node)]) for b in branches(node)]))
            return optional[0] if optional else None

    return path(t, x)


def my_map(fn, seq):
    """Applies fn onto each element in seq and returns a list.
    >>> my_map(lambda x: x*x, [1, 2, 3])
    [1, 4, 9]
    """
    return [fn(x) for x in seq]


def my_filter(pred, seq):
    """Keeps elements in seq only if they satisfy pred.
    >>> my_filter(lambda x: x % 2 == 0, [1, 2, 3, 4])  # new list has only even-valued elements
    [2, 4]
    """
    return [x for x in seq if pred(x)]


def my_reduce(combiner, seq):
    """Combines elements in seq using combiner.
    seq will have at least one element.
    >>> my_reduce(lambda x, y: x + y, [1, 2, 3, 4])  # 1 + 2 + 3 + 4
    10
    >>> my_reduce(lambda x, y: x * y, [1, 2, 3, 4])  # 1 * 2 * 3 * 4
    24
    >>> my_reduce(lambda x, y: x * y, [4])
    4
    >>> my_reduce(lambda x, y: x + 2 * y, [1, 2, 3]) # (1 + 2 * 2) + 2 * 3
    11
    """
    if len(seq) == 1:
        return seq[0]
    else:
        temp = seq[0]
        for i in range(1, len(seq)):
            temp = combiner(temp, seq[i])
        return temp


def count_palindromes(L):
    """The number of palindromic words in the sequence of strings
    L (ignoring case).

    >>> count_palindromes(("Acme", "Madam", "Pivot", "Pip"))
    2
    """
    return len([w for w in L if w.lower() == w.lower()[::-1]])


def sum_tree(t):
    """
    Add all elements in a tree.
    >>> t = tree(4, [tree(2, [tree(3)]), tree(6)])
    >>> sum_tree(t)
    15
    """
    if is_leaf(t):
        return int(label(t))
    else:
        return sum([sum_tree(b) for b in branches(t)]) + int(label(t))


def balanced(t):
    """
    Checks if each branch has same sum of all elements and
    if each branch is balanced.
    >>> t = tree(1, [tree(3), tree(1, [tree(2)]), tree(1, [tree(1), tree(1)])])
    >>> balanced(t)
    True
    >>> t = tree(1, [t, tree(1)])
    >>> balanced(t)
    False
    >>> t = tree(1, [tree(4), tree(1, [tree(2), tree(1)]), tree(1, [tree(3)])])
    >>> balanced(t)
    False
    """
    all_branches_are_balanced = all([balanced(b) for b in branches(t)])

    sums = [sum_tree(t) for t in branches(t)]
    all_branches_have_same_sum = all([sums[0] == s for s in sums])

    return all_branches_are_balanced and all_branches_have_same_sum
