"""Typing test implementation"""

from datetime import datetime

from ucb import main
from utils import lower, split, lines_from_file, remove_punctuation


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> choose(ps, s, 0)
    'hi'
    >>> choose(ps, s, 1)
    'fine'
    >>> choose(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    filtered = [p for p in paragraphs if select(p)]
    return filtered[k] if len(filtered) > k else ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    return lambda l: len([w for w in split(l) if lower(remove_punctuation(w)) in topic]) > 0
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    Arguments:
        typed: a string that may contain typos
        reference: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """

    def calculate_accuracy(t, r):
        # make longer r fits t's length:
        #     >>> accuracy('Cute', 'Cute Dog.')
        #     100.0
        if len(t) < len(r):
            r = r[:len(t)]

        correct = len(r)
        for i in range(len(r)):
            if t[i] != r[i]:
                correct -= 1

        return correct / len(t) * 100.0

    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if len(typed) == 0 and len(reference) == 0:
        return 100.0
    elif len(typed) == 0 or len(reference) == 0:
        return 0.0
    else:
        return calculate_accuracy(typed_words, reference_words)

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return len(typed) / 5 / elapsed * 60
    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, valid_words: list, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        valid_words: a list of strings representing valid words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    >>> abs_diff = lambda w1, w2, limit: abs(len(w2) - len(w1))
    >>> autocorrect("cul", ["culture", "cult", "cultivate"], abs_diff, 10)
    'cult'
    >>> autocorrect("inside", ["idea", "inside"], first_diff, 0.5)
    'inside'
    """

    # BEGIN PROBLEM 5
    if typed_word in valid_words:
        return typed_word

    def diff_wrapper(valid_word):
        return diff_function(valid_word, typed_word, limit)

    candidate = min(valid_words, key=diff_wrapper)
    return candidate if diff_function(candidate, typed_word, limit) <= limit else typed_word
    # END PROBLEM 5


def feline_flips(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths and returns the result.

    Arguments:
        start: a starting word
        goal: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_flips("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_flips("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_flips("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_flips("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_flips("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    >>> [feline_flips('silly', 'silly', k) > k for k in range(5)]
    [False, False, False, False, False]
    """

    # BEGIN PROBLEM 6
    def rec(start_word, goal_word, count=0):
        # 剪枝：到达limit时提前返回
        if count > limit:
            return limit + 1
        elif start_word == '':
            return count + len(goal_word)
        elif goal_word == '':
            return count + len(start_word)
        else:
            if start_word[0] != goal_word[0]:
                count += 1
            return rec(start_word[1:], goal_word[1:], count)

    return rec(start, goal)
    # END PROBLEM 6


def minimum_mewtations(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.

    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """

    # https://en.wikipedia.org/wiki/Levenshtein_distance
    # This is a DP problem
    # 可以记忆化 M[i][j] 代表 start[i:] 和 goal[j:] 的距离

    # BEGIN PROBLEM 7
    def rec(start_word, goal_word, count=0):
        if count > limit:
            return limit + 1

        # 不直接看答案我永远抽象不出这些规则
        elif min(len(start_word), len(goal_word)) == 0:
            # 两方长度不等，把差值补上
            return count + max(len(start_word), len(goal_word))
        elif start_word[0] == goal_word[0]:
            # 含有一个字符相同的情况
            return rec(start_word[1:], goal_word[1:], count)
        else:
            # 首字符不同，应用三种规则进入下一轮
            return min(rec(start_word, goal_word[1:], count + 1),  # add (correct first char of goal on start)
                       rec(start_word[1:], goal_word, count + 1),  # remove (remove one incorrect char from start)
                       rec(start_word[1:], goal_word[1:], count + 1))  # substitute (fix one incorrect char in start)

    return rec(start, goal)
    # END PROBLEM 7


def final_diff(start, goal, limit):
    """A diff function that takes in a string START, a string GOAL, and a number LIMIT.
    If you implement this function, it will be used.
    这个就是指调整上面公式里三种修正操作的权重，不再都是1
    越容易犯错的操作权重越大，比如越容易打错字母，则替换操作的权重可以设置高一些。
    """
    assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(sofar, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        sofar: a list of the words input so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> sofar = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(sofar, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    correct_count = 0
    for i in range(len(sofar)):
        if sofar[i] == prompt[i]:
            correct_count += 1
        else:
            # 因为要在第一个不正确的单词退出，必须线性，用for循环
            break

    progress = correct_count / len(prompt)
    upload({'id': user_id, 'progress': progress})
    return progress
    # END PROBLEM 8


def time_per_word(words, times_per_player):
    """Given timing data, return a match data abstraction, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_words(match)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_times(match)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    >>> p = [[1, 4, 6, 7], [0, 4, 6, 9]]
    >>> words = ['This', 'is', 'fun']
    >>> match = time_per_word(words, p)
    >>> get_words(match)
    ['This', 'is', 'fun']
    """
    # BEGIN PROBLEM 9
    return match(words,
                 [[player_time[i] - player_time[i - 1] for i in range(1, len(player_time))]
                  for player_time in times_per_player])
    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    times = get_times(match)
    words = get_words(match)
    player_indices = range(len(times))  # contains an *index* for each player
    word_indices = range(len(words))  # contains an *index* for each word

    # BEGIN PROBLEM 10
    # it's ok to use array, this function runs serially
    tie_lock = [False for _ in word_indices]

    def fastest_in_players(player_index, word_index):
        """Check if player is fastest on one particular word"""
        # in case of tie, the first player is chosen
        if tie_lock[word_index]:
            return False

        fastest_time = min(word_time for word_time in [times[i][word_index] for i in player_indices])
        player_time = times[player_index][word_index]

        if fastest_time == player_time:
            tie_lock[word_index] = True
            return time
        else:
            return False

    return [[words[word_index]
             for word_index in word_indices
             if fastest_in_players(player_index, word_index)]
            for player_index in player_indices]
    # END PROBLEM 10


def match(words, times):
    """A data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(match, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(match[0]), "word_index out of range of words"
    return match[0][word_index]


def get_words(match):
    """A selector function for all the words in the match"""
    return match[0]


def get_times(match):
    """A selector function for all typing times for all players"""
    return match[1]


def time(match, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(match[0]), "word_index out of range of words"
    assert player_num < len(match[1]), "player_num out of range of players"
    return match[1][player_num][word_index]


def match_string(match):
    """A helper function that takes in a match object and returns a string representation of it"""
    return "match(%s, %s)" % (match[0], match[1])


enable_multiplayer = False  # Change to True when you're ready to race.


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
