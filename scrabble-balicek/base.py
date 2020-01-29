
import copy
import random

"""
Base class for the player + few utilities

DO NOT MODIFY this file.
        
It will be always replaced by default version of Brute, so any changes will be discarded anyway..

PUT ALL YOUR IMPLEMENTATION TO player.py

"""


class BasePlayer:
    def __init__(self, name, dictionary, board, bag, lettersInBag):
        self.name = name;         #student's name, will be filled by BRUTE
        self.text = "basicPlayer" #student' debug info, e.g. version, name of algorithm..
        self.cols = len(board[0]) #number of columns of the board
        self.rows = len(board)    #number of rows of the board
        self.dictionary = copy.deepcopy(dictionary) #dictionary is of type 'dictionary' (aka hashtable)
        self.board = copy.deepcopy(board)
        self.bag = copy.deepcopy(bag)
        self.myScore = 0;         #total score of this player 
        self.otherScore = 0;      #total score of other player
        self.lettersInBag = lettersInBag
        self.tournament = True   #will be set externally by Brute/Tournament. If true, you can use extended rules for tournament
     
        tripper_letter_score = ((1,5), (1, 9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13, 5), (13,9))
        double_letter_score = ((0, 3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8, 12), (11,0), (11,7), (11,14), (12,6), (12,8), (14, 3), (14, 11))

        self.weights = []
        for i in range(self.rows):
            self.weights.append( [1 for i in range(self.cols) ] )

        for coords in tripper_letter_score:
            self.weights[ coords[0] ][coords[1]] = 3
        for coords in double_letter_score:
            self.weights[ coords[0] ][coords[1]] = 2


    def move(self):
        """
            See player.py for possible return values
        """
        return None

        
    def update(self, board, bag, myScore, otherScore, lettersInBag):
        """ 
            this method load changed made by the second player. Note that self.board and self.bag are changed
        """
        self.board = copy.deepcopy(board)
        self.bag = copy.deepcopy(bag)
        self.myScore = myScore
        self.otherScore = otherScore
        self.lettersInBag = lettersInBag

    def inBoard(self, row, col):
        """ reutrn true of given cell row:col is inside the board """
        return row >=0 and row < self.rows and col >=0 and col < self.cols;


    def isEmpty(self, row, col):
        """ return true if the given cell is empty """
        return self.board[row][col] == ""

    def print(self):
        """ 
            fo debug - print the board
        """
        #print("Player:", self.name, self.text,", bag: ", self.bag, ", bigBag.size=",self.lettersInBag)
        print("  ",end="")
        for c in range(self.cols):
            print("{0:3}".format(c), end="")
        print()

        for r in range(self.rows):
            print("{0:3}".format(r), end="")
            for c in range(self.cols):
                if self.board[r][c] == "":
                    print(" . ",end="")
                else:
                    print(" " + self.board[r][c] + " " , end="")
            print()

    def cellValue(self, row, col):
        return self.weights[row][col]

    def letterValue(self,letter):
        letter_values = {"A": 1,"B": 3,"C": 3,"D": 2,"E": 1,"F": 4,"G": 2,"H": 4,"I": 1,"J": 8,"K": 5,"L": 1,"M": 3,"N": 1,"O": 1,"P": 3,"Q": 10,"R": 1,"S": 1,"T": 1,"U": 1,"V": 4,"W": 4,"X": 8,"Y": 4,"Z": 10}
        if letter in letter_values:
            return letter_values[letter]
        return 0


# ========================== various useful functions ==========================

def readDictionary(filename):
    """
        read the dictionary (one word per line), convert all to UPPER case and return as DICTIONARY 
    """
    f = open(filename,'r')
    d = {}
    for line in f:
        line = line.rstrip().upper()
        if len(line) > 0:
            d[line] = 1
    f.close()
    return d



def randomizeArray(array):
    """
        shuffle the array
    """
    for i in range(len(array)-1):
        rpos = random.randint(i+1,len(array)-1);
        array[i], array[rpos] = array[rpos], array[i]

def createInitialBag():
    """
        create a 'big bag' of letters from which both players draw their own letters
    """
    init_bag = []

    BAG =    {"A": 9, "B": 2, "C": 2, "D": 4, "E": 10, "F": 2, "G": 3, "H": 2,"I": 9,"J": 1,"K": 1,"L": 4,"M": 2,"N": 6,"O": 8,"P": 2,"Q": 1,"R": 6, "S": 4,"T": 6,"U": 4,"V": 2,"W": 2,"X": 1,"Y": 2,"Z": 1 }

    for letter in BAG:
        count = BAG[letter]
        for i in range(count):
            init_bag.append(letter)
    randomizeArray(init_bag)
    return init_bag



def createBoard(word):
    """
        create board and fill its center by the iven word
    """
    size = 15;

    board = []
    for i in range(size):
        board.append( [ "" for i in range(size) ]   )

    if (len(word) >= size):
        print("Error: cannot create the board, the inital word '",word,"' is too long.")
        quit()
    left = (size-len(word))//2;
    for i in range(left, left+len(word)):
        board[size//2][i] = word[i-left]
    return board





