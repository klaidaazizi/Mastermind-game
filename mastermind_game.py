'''
Klaida Azizi
CS5001
Mastermind Game project
'''

import turtle
import random
import time
from Point import Point
from Marble import Marble

MARBLE_RADIUS = 15
PEG_RADIUS = 5

def count_bulls_and_cows(secret_code, guess):
    '''
    function - count_bulls_and_cows
    input: two lists, the secret code and the user guess
    output: a tuple of two elements: number of bulls, number of cows
    '''
    bulls = 0
    cows = 0
    for i in range(len(secret_code)):
        if guess[i] == secret_code[i]:
            bulls += 1
        elif guess[i] in secret_code:
            cows += 1
    return bulls, cows
        
class Gameboard:
    '''
    Class - Gameboard
    It controls the graphic part of the game. Coded in turtle.
    '''
    def __init__(self):
        # screen and game board
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen() # screen
        self.screen.title('Mastermind')
        self.screen.setup(width = 600, height = 800)
        self.pen.color('black')
        self.pen.hideturtle()
        self.pen.speed(0)

    def prompt_name(self):
        name = turtle.textinput("Mastermind Game", "Your Name:")
        return name
    
    def draw_gameboard(self):
        # draw gameboard on the leftside
        self.draw_rectangle(Point(-280,-180), 300, 500, 90)

    def draw_rectangle(self, position, width, height, angle):
        #general function to draw a rectangle in turtle
        self.pen.pensize(3)
        self.pen.up()
        self.pen.goto(position.x, position.y)
        self.pen.down()
        self.pen.forward(width)
        self.pen.left(angle)
        self.pen.forward(height)
        self.pen.left(angle)
        self.pen.forward(width)
        self.pen.left(angle)
        self.pen.forward(height)
        self.pen.left(angle)

    def draw_leaderboard(self):
        # draw leaderboard on the right side
        self.draw_rectangle(Point(40,-180), 230, 500, 90)
        try:
            with open('leaderboard.txt', 'r') as leaderboard: #open leaderboard file
                leader = leaderboard.readlines()
                leaders = []
                for each in leader:
                    each = each.strip()
                    leaders.append(each)
        except FileNotFoundError:
            self.leaderboard_error()
        else:
            self.pen.up()
            self.pen.goto(120,280)
            self.pen.down()
            self.pen.write('Leaders', font = ("Arial", 14, "bold"), align = "left")
            self.pen.up()
            self.pen.goto(80,250)
            if len(leaders) >= 2: # if more than 2 winners in file, read only the last 2
                self.pen.write(str(leaders[-1]), font = ("Arial", 13, "normal"), align = "left")
                self.pen.up()
                self.pen.goto(80,230)
                self.pen.write(str(leaders[-2]), font = ("Arial", 13, "normal"), align = "left")
            elif len(leaders) == 1: # if only one previous winner
                self.pen.write(str(leaders[0]), font = ("Arial", 13, "normal"), align = "left")
                self.pen.up()
            else: # if empty leaderboard file, open new one
                leaderboard = open('leaderboard.txt.','a')
                leaderboard.close()
                
    def draw_playboard(self):
        # draw playboard at the bottom
        self.draw_rectangle(Point(-280,-300), 550, 100, 90) 
       
    def draw_emptymarbles(self):
        x = -210
        y = 260
        guesses_list = []
        guess = []
        for i in range(10):
            # marbles for 4 user guesses
            marble1 = Marble(Point(x,y), '', MARBLE_RADIUS)
            marble1.draw()
            marble2 = Marble(Point(x + 40,y), '', MARBLE_RADIUS)
            marble2.draw()
            marble3 = Marble(Point(x + 80,y), '', MARBLE_RADIUS)
            marble3.draw()
            marble4 = Marble(Point(x + 120,y), '', MARBLE_RADIUS)
            marble4.draw()

            # bulls and cows pegs
            marble5 = Marble(Point(x + 170, y + 20), '', PEG_RADIUS)
            marble5.draw()
            marble6 = Marble(Point(x + 190,y + 20), '', PEG_RADIUS)
            marble6.draw()
            marble7 = Marble(Point(x + 170,y), '', PEG_RADIUS)
            marble7.draw()
            marble8 = Marble(Point(x + 190,y), '', PEG_RADIUS)
            marble8.draw()

            # list of one row
            guess = [marble1, marble2,marble3,marble4,marble5,marble6,marble7,marble8]
            y -= 45 # decrease y position for the next row
            guesses_list.append(guess) #list of lists of all rows
        return guesses_list
                
    def draw_marbleboard(self):
        # 6 colored marbles in the bottom
        marbleboard = []
        y = -265
        x = -250
        blue = Marble(Point(x,y), 'blue', MARBLE_RADIUS)
        blue.draw()
        red = Marble(Point(x+45,y), 'red', MARBLE_RADIUS)
        red.draw()
        green = Marble(Point(x+90,y), 'green', MARBLE_RADIUS)
        green.draw()
        yellow = Marble(Point(x+135,y), 'yellow', MARBLE_RADIUS)
        yellow.draw()
        purple = Marble(Point(x+180,y), 'purple', MARBLE_RADIUS)
        purple.draw()
        black = Marble(Point(x+225,y), 'black', MARBLE_RADIUS)
        black.draw()
        marbleboard.extend([blue,red,green,yellow,purple,black])
        return marbleboard
    
    def confirm_guess(self):
        # check button to confirm guess
        self.screen.addshape('checkbutton.gif')
        self.pen.shape('checkbutton.gif')
        self.pen.penup()
        self.pen.goto(40,-250)
        self.pen.stamp()

    def delete_guess(self):
        # delete button to delete guess
        self.screen.addshape('xbutton.gif')
        self.pen.shape('xbutton.gif')
        self.pen.penup()
        self.pen.goto(100,-250)
        self.pen.stamp()

    def quit_game(self):
        # quit button to quit out of the game
        self.screen.addshape('quit.gif')
        self.pen.shape('quit.gif')
        self.pen.penup()
        self.pen.goto(200,-250)
        self.pen.stamp()
        
    def win(self, user, score):
        # if user wins
        self.screen.addshape('winner.gif')
        self.pen.shape('winner.gif')
        self.pen.penup()
        self.pen.home()
        self.pen.stamp()
        with open('leaderboard.txt', 'a') as winners:
            winners.write('\nUser {}: {}' .format(user, score)) #add new winner to existing list of winners and scores
        
    def lose(self):
        # if user loses
        self.screen.addshape('lose.gif')
        self.pen.shape('lose.gif')
        self.pen.penup()
        self.pen.home()
        self.pen.stamp()
        turtle.exitonclick()

    def quit(self):
        # if user quits
        self.screen.addshape('quitmsg.gif')
        self.pen.shape('quitmsg.gif')
        self.pen.penup()
        self.pen.home()
        self.pen.stamp()
        turtle.exitonclick()
    
    def leaderboard_error(self):
        # if there's a leaderboard file error
        self.screen.addshape('leaderboard_error.gif')
        self.pen.shape('leaderboard_error.gif')
        self.pen.up()
        self.pen.home()
        stamp = self.pen.stamp()
        time.sleep(2)
        self.pen.clearstamp(stamp)
        
    def draw_board(self): 
    # draw gameboard 
        self.draw_gameboard()
        self.draw_leaderboard()
        self.draw_playboard()
        self.delete_guess()
        self.confirm_guess()
        self.quit_game()

class Game:
    '''
    Class - Game
    It controls the game and makes game decisions based on functions
    '''
    def __init__ (self, user, marbleboard, marbles):
        self.gameboard = Gameboard() 
        self.user = user # user name
        self.marbleboard = marbleboard #colored marbles at the bottom
        self.marbles = marbles #empty marbles for user guess
        self.pegs = [] # list of pegs
        for i in range(len(self.marbles)):
            pegs = self.marbles[i][4:]
            self.pegs.append(pegs)
        self.colors = ["red", "blue", "green", "yellow", "purple", "black"]
        self.code = self.generate_code() # generate random code
        self.guess = [] # list of colors guessed by user
        self.row = 0 # row of current color choice
        self.column = 0 # column of current color choice 
        self.score = 0 # overall score 
        
    def generate_code(self):
        # generates random code (computer's code)
        code = random.sample(self.colors, 4)
        # print(code)
        return code

    def count_bulls_and_cows(self):
        # takes the bulls and cows list and decides on how to color the pegs based on it
        bulls_and_cows = count_bulls_and_cows(self.code, self.guess)
        if bulls_and_cows[0] == 4: # if 4 bulls, the user wins
            self.gameboard.win(self.user, self.score)
        else:
            bulls_cows = ['black'] * bulls_and_cows[0] + ['red'] * bulls_and_cows[1] # list of black and red pegs
            for i in range(len(bulls_cows)): # color pegs with color from list of pegs
                self.pegs[self.row][i].set_color(bulls_cows[i])
                self.pegs[self.row][i].draw()
            if self.score == 10: # if 10 wrong guesses, user loses
                self.gameboard.lose()
            
    def color_marble(self):
        # colors the marble at the particular column with color selected
        self.marbles[self.row][self.column].set_color(self.guess[self.column])
        self.marbles[self.row][self.column].draw()
       
    def click(self, x, y):
        # click function - controller of the click 
        if abs(x - 220) < 80 and abs(y + 240) < 36: #if click on quit
            self.gameboard.quit()
        elif abs(x - 40) < 40 and abs(y + 250) < 40: #if click on confirm
            if len(self.guess) == 4:
                self.score += 1 # increase score by 1 for next round
                self.count_bulls_and_cows() 
                self.row += 1
                self.column = 0
                self.guess = []
                self.gameboard.draw_marbleboard()
        elif abs(x - 100) < 40 and abs(y + 250) < 40: #if click on delete
            self.gameboard.draw_marbleboard()
            for i in range(4):
                self.marbles[self.row][i].draw_empty()
            self.guess = []
            self.column = 0
        else:
            for i in range(len(self.marbleboard)):
                if self.marbleboard[i].clicked_in_region(x,y): # if user clicks on a color
                    color = self.marbleboard[i].get_color() # get color that user chose
                    self.marbleboard[i].draw_empty() # draw empty marble instead
                    if len(self.guess) == 4:
                        self.gameboard.draw_marbleboard()
                        self.guess = [] 
                        self.row += 1
                        self.column = 0
                    else:
                        if color not in self.guess: # no duplicate colors
                            self.guess.append(color)
                            self.color_marble()
                            self.column += 1
        # print(self.guess)
        return self.guess
        
    
def main():
    
    gameboard = Gameboard() 
    user = gameboard.prompt_name() # prompt user for name
    gameboard.draw_board() # draw gameboard
    marbles = gameboard.draw_emptymarbles() # draw empty marbles
    marbleboard = gameboard.draw_marbleboard() #draw marbleboard
    game = Game(user,marbleboard, marbles) # call game class
    gameboard.screen.onclick(game.click) # call click function
    

if __name__ == "__main__":
    main()

