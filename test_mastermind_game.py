import unittest
from mastermind_game import Game
from mastermind_game import *

'''
Tests the function count_bulls_and_cows
(couldn't really figure out how to test the class Game since it contains mostly turtle calls)
'''

def test_bulls_and_cows(code, guess, expected):
    '''
    Function - test_bulls_and_cows
    Tests the return tuple for the bulls_and_cows function
    The function should take two lists, the secret code and the user guess
    and return a tuple of two elements: number of bulls, number of cows
    '''

    bulls_and_cows = count_bulls_and_cows(code,guess)

    print("The computer's code is: {}\n \
            Your guess is: {}\n \
            Your bulls and cows result is: {} \n \
            The expected value is: {}".format(code,guess,bulls_and_cows,expected))

def main():
    code = ['red','black','purple','yellow']
          
    test_bulls_and_cows(code, ['yellow','black','purple','red'], (2,2))

    test_bulls_and_cows(code, ['blue','black','green','red'], (1,1))

    test_bulls_and_cows(code, ['blue','purple','green','black'], (0,2))

    test_bulls_and_cows(code, ['red','black','purple','yellow'], (4,0))

    test_bulls_and_cows(code, ['purple','yellow','black','red'], (0,4))

main()
    
    
    
    
