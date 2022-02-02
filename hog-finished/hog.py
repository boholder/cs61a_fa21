"""CS 61A Presents The Game of Hog."""
import math

from dice import six_sided, make_test_dice
from ucb import main

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.

    >>> roll_dice(2, make_test_dice(4, 6, 1))
    10
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'

    # BEGIN PROBLEM 1
    # finite sequence
    def dice_gen(n):
        i = 0
        while i < n:
            yield dice()
            i += 1

    # should just roll once
    roll_results = list(dice_gen(num_rolls))
    if 1 in set(roll_results):
        return 1
    else:
        return sum(roll_results)
    # END PROBLEM 1


def picky_piggy(score):
    """Return the points scored from rolling 0 dice.

    score:  The opponent's current score.
    >>> picky_piggy(0)
    7
    >>> picky_piggy(1)
    1
    >>> picky_piggy(2)
    4
    >>> picky_piggy(3)
    2
    >>> picky_piggy(4)
    8
    >>> picky_piggy(5)
    5
    >>> picky_piggy(6)
    7
    """

    # BEGIN PROBLEM 2
    # not easy to take arbitrary digit from arbitrary number
    # without stringify the number
    # https://stackoverflow.com/a/21270442/11397457
    # I just know the digit number of 1/7, i.e. 142857, is 6,
    # so I can just use this (get last digit after move right by given digits):
    def take_nth_digit(n):
        return math.floor(142857 / pow(10, 6 - n) % 10)

    if score == 0:
        return 7
    elif score % 6 == 0:
        # special
        return take_nth_digit(6)
    else:
        # let function take 1..5 as param
        return take_nth_digit(score % 6)
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 in the case
    of a player using Picky Piggy.
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    goal:            The goal score of the game.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < goal, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return picky_piggy(opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def hog_pile(player_score, opponent_score):
    """Return the points scored by player due to Hog Pile.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """
    # BEGIN PROBLEM 4
    if player_score == opponent_score:
        return player_score
    else:
        return 0
    # END PROBLEM 4


def next_player(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> next_player(0)
    1
    >>> next_player(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.

    >>> import hog
    >>> always_three = hog.make_test_dice(3)
    >>> always = hog.always_roll
    >>> s0, s1 = hog.play(always(5), always(3), score0=91, score1=10, dice=always_three)
    >>> s0
    106
    >>> s1
    10
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    commentary = say
    # BEGIN PROBLEM 5
    while True:
        # roll
        if who == 0:
            score0 += take_turn(strategy0(score0, score1), score1, dice, goal)
            score0 += hog_pile(score0, score1)
        else:
            score1 += take_turn(strategy1(score1, score0), score0, dice, goal)
            score1 += hog_pile(score1, score0)

        commentary = commentary(score0, score1)

        # quit?
        if score0 >= goal or score1 >= goal:
            break
        else:
            who = next_player(who)
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """

    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)

    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """

    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))

    return say


def announce_highest(who, last_score=0, running_high=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 9)
    9 point(s)! That's a record gain for Player 1!
    >>> f3 = f2(20, 9)
    >>> f4 = f3(20, 30)
    21 point(s)! That's a record gain for Player 1!
    >>> f5 = f4(20, 47) # Player 1 gets 17 points; not enough for a new high
    >>> f6 = f5(21, 47)
    >>> f7 = f6(21, 77)
    30 point(s)! That's a record gain for Player 1!
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'

    # BEGIN PROBLEM 7
    def say(score0, score1):
        if who == 0:
            return calc(running_high, score0)
        else:
            return calc(running_high, score1)

    def calc(max_diff, current_score):
        diff = current_score - last_score
        if diff > running_high:
            max_diff = diff
            print("{} point(s)! That's a record gain for Player {}!".format(diff, who))
        return announce_highest(who, current_score, max_diff)

    return say
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """

    def strategy(score, opponent_score):
        return n

    return strategy


def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TRIALS_COUNT times.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 1000)
    >>> averaged_dice(1, dice)
    3.0
    """

    # BEGIN PROBLEM 8
    def avg(*args):
        scores = []
        for i in range(trials_count):
            scores.append(original_function(*args))
        return sum(scores) / len(scores)

    return avg
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    max_avg_score = -1
    for i in range(1, 11):
        avg_score = make_averaged(roll_dice, trials_count)(i, dice)
        if avg_score > max_avg_score:
            max_avg_score = avg_score
            num_rolls = i
    return num_rolls
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)
    print('always_roll(6) win rate:', average_win_rate(always_roll(6)))

    # print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
    # print('picky_piggy_strategy win rate:', average_win_rate(picky_piggy_strategy))
    print('hog_pile_strategy win rate:', average_win_rate(hog_pile_strategy))
    # print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def picky_piggy_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy returns 0 dice if that gives at least CUTOFF points, and
    returns NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if picky_piggy(opponent_score) >= cutoff:
        num_rolls = 0
    return num_rolls
    # END PROBLEM 10


def hog_pile_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy returns 0 dice when this would result in Hog Pile taking
    effect. It also returns 0 dice if it gives at least CUTOFF points.
    Otherwise, it returns NUM_ROLLS.

    >>> hog_pile_strategy(2, 10, cutoff=10, num_rolls=6)
    6
    >>> hog_pile_strategy(20, 36, cutoff=7, num_rolls=6)
    0
    """
    # BEGIN PROBLEM 11
    if hog_pile(score + picky_piggy(opponent_score), opponent_score) >= cutoff:
        num_rolls = 0
    else:
        return picky_piggy_strategy(score, opponent_score, cutoff, num_rolls)

    return num_rolls
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Return the number of dice to roll to gain highest possible score.
    """
    # BEGIN PROBLEM 12
    return hog_pile_strategy(score, opponent_score, 10, max_scoring_num_rolls())
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
