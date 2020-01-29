import sys
import base
import random
import itertools
import string
from collections import namedtuple


print("Importing players from %s and %s" % (sys.argv[1],sys.argv[2]))
P1 = __import__(sys.argv[1], globals(), locals(), [], 0)
P2 = __import__(sys.argv[2], globals(), locals(), [], 0)


Coord =      P1.Coord
Valuable =   P1.Valuable
Move =       P1.Move
ValidWords = P1.ValidWords

def coord_same_row(begin : Coord, end : Coord) -> bool:
    return begin.row == end.row

def coord_same_col(begin : Coord, end : Coord) -> bool:
    return begin.col == end.col

def coord_same_line(begin : Coord, end : Coord) -> bool:
    return coord_same_row(begin, end) or coord_same_col(begin, end)

def coord_is_between(this : Coord, begin : Coord, end : Coord) -> bool:
    """
    Checks whether the this coordinate lies in a line between begin and end.
    It is used by Player.consider_complex_moves to validate whether all filled blank spaces add up to a whole word
    """
    assert(coord_same_line(begin, end))
    if coord_same_row(begin, end): #Word is placed in_row
        return coord_same_row(this, begin) and begin.col <= this.col and this.col < end.col 
    return coord_same_col(this, begin) and begin.row <= this.row and this.row < end.row

def is_empty(board : list, row : int, col : int) -> bool:
    return board[row][col] == ''

def in_board(row : int, col : int) -> bool:
    return P1.in_board(row, col)

def letter_value(letter : str) -> int:
    return P1.letter_value(letter)

def cell_value(row :int, col : int) -> int:
    return P1.cell_value(row, col)

def word_value(board: list, begin: Coord, end: Coord) -> int:
    assert(coord_same_line(begin, end))
    if coord_same_row(begin, end): #Summing in_row
        return sum(letter_value(board[begin.row][x]) * cell_value(begin.row, x) for x in range(begin.col, end.col))
    return sum(letter_value(board[y][begin.col]) * cell_value(y, begin.col) for y in range(begin.row, end.row))

def find_maximal_word(board : list, start : Coord, search_in_row : bool) -> tuple:
    if not in_board(*start) or is_empty(board, *start):
        return (start, start)

    if search_in_row:
        LL, RR = start.col - 1, start.col + 1
        while in_board(start.row, LL) and not is_empty(board, start.row, LL):
            LL -= 1
        LL += 1
        while in_board(start.row, RR) and not is_empty(board, start.row, RR):
            RR += 1

        return Coord(start.row, LL), Coord(start.row, RR)
    UU, DD = start.row - 1, start.row + 1
    while in_board(UU, start.col) and not is_empty(board, UU, start.col):
        UU -= 1
    UU += 1
    while in_board(DD, start.col) and not is_empty(board, DD, start.col):
        DD += 1

    return Coord(UU, start.col), Coord(DD, start.col)

def word_length(begin : Coord, end : Coord) -> int:
    assert(coord_same_line(begin, end))
    return end.col - begin.col if coord_same_row(begin, end) else end.row - begin.row



def compute_score_gain(moves: list, board: list) -> int:
    assert(isinstance(board, list))
    assert(isinstance(board[0], list))
    assert(isinstance(moves, list))

    moves = [Move(Coord(row, col), letter, 0) for row, col, letter in moves]

    moves.sort(key = lambda move: move.coord)
    first, last = moves[0], moves[-1]
    assert(coord_same_line(first.coord, last.coord)) #All letters lie either in the same row or column
    assert(all(in_board(*move.coord) for move in moves))

    in_row = coord_same_row(first.coord, last.coord)
    word_bounds = [find_maximal_word(board, change.coord, not in_row) for change in moves] + [find_maximal_word(board, first.coord, in_row)]

    return sum(word_value(board, *bounds) for bounds in word_bounds if word_length(*bounds) > 1)


def replaceLetters(player, lettersToReplace, bag):
    #print("Player ", player.name, " want's to exchange ", len(lettersToReplace), ", bag has " , len(bag) , " letters")
        
    if len(lettersToReplace) > 7:
        print("More than 7 letters of change requested")
        return player.bag
    elif len(lettersToReplace) == 0:
        print("Zero letters to be changed")
        return player.bag

    elif len(lettersToReplace) > len(bag):
        print("No replacement will be made, as the user either wants to change more letters than there are in the bag")
        return player.bag

    else:
        listLetters = list(lettersToReplace)
        newBag = []
        for letter in player.bag:
            if letter not in listLetters:
                newBag.append(letter)
            else:
                listLetters.remove(letter)
           
        new = "" 
        for i in range(len(lettersToReplace)):
            if len(bag) > 0:
                newBag.append(bag.pop())
                new += newBag[-1]
            else:
                print("Bag has been depleted")
        #print("New replacement ", new)
        return newBag



def afterMove(lastPlayer, lastPlayerResult, nextPlayer, board, bag):

    """
        simplifed game handling procedure. We assume here that both player behave correctly, e.g. they do not
        invalide their 'self.bag' etc..

        On Brute/Tournament, this function will also check all return types and validiy of actions
    """

    if (lastPlayerResult is None):
        #player 'pass', no change
        #print("Player ", lastPlayer.name, " is passing ")
        return 0
    
    if isinstance(lastPlayerResult, str):
    
        newBag = replaceLetters(lastPlayer, lastPlayerResult, bag)    
        lastPlayer.update(board, newBag, lastPlayer.myScore, nextPlayer.myScore, len(bag))
        nextPlayer.update(board, nextPlayer.bag, nextPlayer.myScore, lastPlayer.myScore, len(bag))
        #the second player does not need to be updated, as the board didn't
        #change
        return 0

    if isinstance(lastPlayerResult,list):
        #player is placing some letters to the game
        #print("Player ", lastPlayer.name , " is placing stuff .. ", lastPlayerResult)
        lettersToReplace = ""
        board_changes = 0
        for change in lastPlayerResult:
            assert(isinstance(change, list) and len(change) == 3)
            row, col, letter = change
            assert(in_board(row, col) and board[row][col] == "")
            board[row][col] = letter
            lettersToReplace += letter
            #print("Placing ", letter, "at ", row,col)
            board_changes+=1
        new_score = lastPlayer.myScore + compute_score_gain(lastPlayerResult, board)
        #print("Score increased by %d" % score_gain)


        newBag = [letter for letter in lastPlayer.bag if letter not in lettersToReplace] if len(bag) == 0 else replaceLetters(lastPlayer, lettersToReplace, bag)
        lastPlayer.update(board, newBag, new_score, nextPlayer.myScore, len(bag))
        nextPlayer.update(board, nextPlayer.bag, nextPlayer.myScore, new_score, len(bag))
        return board_changes

    print("Wrong result from player.move; exit now")
    input()
    quit()
    return 0

if __name__ == "__main__":

    index = 0
    words = base.readDictionary('dic.txt') #words is represented as python-dictionray

    p1_wins, p2_wins, draws = 0,0,0
    p1_score, p2_score = 0,0

    while True:
        index += 1
        #words = ['PA', 'AP', 'ALP', 'LP', 'AAL']
        #board = base.createBoard("ALP") #this word should be from the dictionray

        starting_word = random.choice(list(words))
        while len(starting_word) >= 15:
            starting_word = random.choice(list(words))

        board = base.createBoard(starting_word) #random word from the dictionray
    
        bag = base.createInitialBag()
        #bag = list("AELPAPRLAP") * 10
    
        player1bag = bag[0:7]   #letters for the player1
        player2bag = bag[7:14]  #letters for the player2
        bag = bag[14:] #remove first 14 letters
    
    
        p1 = P1.Player("P1", words, board, player1bag, len(bag))
        p2 = P2.Player("P2", words, board, player2bag, len(bag))
        #p1.print()
    
        noChangeMoves = 0
        turn = 0
        while True:      
    
            result = p1.move()
            s1 = afterMove(p1, result, p2, board, bag)

    
            #p1.print()
    
            turn += 2
            result = p2.move()
            s2 = afterMove(p2, result, p1, board, bag)
        
            #p2.print()
    
            if s1 + s2 == 0:
                noChangeMoves+=1
                if noChangeMoves == 3:
                    print("Game finished after 3 moves without change of score.")
                    break
            else:
                noChangeMoves = 0

            if len(p1.bag) == 0 and len(p2.bag) == 0:
                print("Bag exhausted! Ending game")
                break

        print("Game no. %d after %d turns:" % (index, turn))
        print("State of bags:\n\tbig ... %s\n\tp1  ... %s\n\tp2  ... %s\n" % (''.join(bag), ''.join(p1.bag), ''.join(p2.bag)))

        p1_score += p1.myScore
        p2_score += p2.myScore

        winner = ''
        if p1.myScore > p2.myScore:
            p1_wins += 1
            winner = "P1 victory!"
        elif p2.myScore > p1.myScore:
            p2_wins += 1
            winner = "P2 victory!" 
        else:
            draws += 1
            winner = "DRAW!"
        print("Score:\t%s\n\tP1 ... %d\n\tP2 ... %d" % (winner,p1.myScore, p2.myScore))
        assert(p1.myScore == p2.otherScore and p1.otherScore == p2.myScore)
        p2.print()
        print("Total results out of %d games: " % (index))
        print("\tP1 won %d (%.2f%%) with score %d\n\tP2 won %d (%.2f%%) with score %d\n\tdraw   %d (%.2f%%)" % 
              (p1_wins, p1_wins*100 / index, p1_score, p2_wins, p2_wins * 100/index, p2_score, draws, draws*100/index))
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")