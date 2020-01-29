import base
import random
import itertools
import string
from collections import namedtuple

Coord = namedtuple('Coord', ['row', 'col'])
Valuable = namedtuple('Valuable', ['stuff', 'score'])
Move = namedtuple('Move', ['coord','letter','score'])
ValidWords = namedtuple('ValidWords', ['in_col', 'in_row'])

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





def write(board : list, letter : str, row : int, col : int):
    assert(isinstance(board, list) and isinstance(board[0], list) and type(row) == int and type(col) == int and isinstance(letter, str))
    """
    Wrapper function to simplify writing letters to board by means of starred tuple unpacking
    """
    board[row][col] = letter

def is_empty(board : list, row : int, col : int) -> bool:
    return board[row][col] == ''

def in_board(row : int, col : int) -> bool:
    pass

def letter_value(letter : str) -> int:
    pass

def cell_value(row :int, col : int) -> int:
    pass

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


def build_heat_map(board : list) -> tuple:
    """
    Analyzes the game board, finds squares that should be considered in the later stage of turn and precomputes possible gain form each square.
    Each square is checked whether it is a neighbour to at least one letter. It if is, it is added to useable_squares and the value of neighbouring 
    words is calculated and saved into the heat_map matrix. Both data structures are returned. Only squares marked useable are to be considered later, 
    since the others are either out of bounds or have literally zero neighbours

    """
    assert(isinstance(board, list))
    assert(isinstance(board[0], list))


    height, width = len(board), len(board[0])
    heat_map = [[None] * width for i in range(height)]
    useable_squares = {}

    for pos in map(Coord._make, itertools.product(range(height), range(width))):
        if not is_empty(board, *pos): #If this square is already filled by a letter
            continue
        #if the square is not surrounded by any letter
        if all(not in_board(*neighbour) or is_empty(board, *neighbour) for neighbour in (Coord(pos.row + dy, pos.col + dx) for dy, dx in ((1,0), (0,1), (-1,0), (0,-1)))):
            continue

        #find four potentially surrounding words
        words_in_row = [find_maximal_word(board, Coord(pos.row, pos.col + dx), True) for dx in (-1, 1)]
        words_in_col = [find_maximal_word(board, Coord(pos.row + dy, pos.col), False) for dy in (-1, 1)]
            
        in_row_score = sum(map(lambda word_bounds: word_value(board, *word_bounds), words_in_row))
        in_col_score = sum(map(lambda word_bounds: word_value(board, *word_bounds), words_in_col))

        #Only non zero value is interesting for us to get that juicy scrabble money
        assert(in_row_score or in_col_score)

        heat_map[pos.row][pos.col] = ValidWords(in_col_score, in_row_score)
        useable_squares[pos] = ValidWords([], [])

    return heat_map, useable_squares    


def analyze_square_useability(board : list, heat_map : list, useable_squares : dict, bag_set : set, dictionary : set):
    assert(isinstance(bag_set, set))
    assert(isinstance(board, list))
    assert(isinstance(board[0], list))
    assert(isinstance(useable_squares, dict))
    assert(isinstance(dictionary, dict))

    for coord in useable_squares:
        assert(is_empty(board, *coord))
        neighbour_values = heat_map[coord.row][coord.col]
        write(board, 'x', *coord) #Pretend as if the letter was placed on the board

        if neighbour_values.in_col == 0: #Both squares above and beneath are empty. Every letter counts as a one-letter word
            for letter in bag_set: # So add a "word" for each letter in bag
                useable_squares[coord].in_col.append(Valuable(letter, 0))
        else:
            begin, end = find_maximal_word(board, coord, False)
            assert(word_length(begin, end) >= 2)
            for letter in bag_set:
                write(board, letter, *coord)
                #Find maximal words intersecting at this newly filled letter
                in_col = get_string(board, begin, end)
                if in_col in dictionary:
                    score = neighbour_values.in_col + cell_value(*coord) * letter_value(letter)
                    useable_squares[coord].in_col.append(Valuable(letter, score))

        if neighbour_values.in_row == 0: #Both squares to the left and right are empty. 
            for letter in bag_set:
                useable_squares[coord].in_row.append(Valuable(letter, 0))
        else:
            begin, end = find_maximal_word(board, coord, True)
            assert(word_length(begin, end) >= 2)
            for letter in bag_set:
                write(board, letter, *coord) #Pretend as if the letter was placed on the board
                #Find maximal words intersecting at this newly filled letter
                in_row = get_string(board, begin, end)
                if in_row in dictionary:
                    score = neighbour_values.in_row + cell_value(*coord) * letter_value(letter)
                    useable_squares[coord].in_row.append(Valuable(letter, score))

        write(board, '', *coord) #Restore the board state when advancing to the next square

    return {coord : words for coord, words in useable_squares.items() if words.in_col or words.in_row }


def find_simple_moves(board : list, heat_map : list, useable_squares : dict, bag_set : set) -> list:
    """
        Goes through the board trying each letter in bag_set for each useable square. If such move would create a pair of valid words, it is recorded.
        Should a useable_square prove to not be useable, it is removed. I.e. if no word could be formed when writing to this square, erase it.

        Returns list of valid sinple-letter moves
    """
    assert(isinstance(bag_set, set))
    assert(isinstance(board, list))
    assert(isinstance(board[0], list))
    assert(isinstance(useable_squares, dict))

    simple_moves = []

    for coord, words in useable_squares.items():
        assert(all(score >= 0 and letter in bag_set for letter, score in itertools.chain(words.in_col, words.in_row)))

        for letter, score_in_col in words.in_col:
            for l, score_in_row in words.in_row:
                if l == letter:
                    simple_moves.append(Move(coord, letter, score_in_row + score_in_col))
                    break
    simple_moves.sort(reverse=True, key = lambda move : move.score)
    return simple_moves


def choose_best_simple_move(simple_moves : list, heat_map : list, useable_squares : dict, bag_set : set) -> Valuable:
    """
    Main function making decisions about simple one-letter moves.
    It builds on top of knowledge summarized in the pottential score gain heat map. For simplicity sake a semi-bruteforce is used
    to try all available letters in all squares that can be filled. These 'useable_squares' are determined by build_heat_map
    and reflect the fact that some squares are totally unuseable due to their high distance from the rest of filled letters.

    For each useable square a letter is checked whether or not it forms a valid word both in_col as well as in_row.
    Move with the highest score is found and returned.
    """
    assert(isinstance(bag_set, set))
    assert(isinstance(useable_squares, dict))
    assert(isinstance(simple_moves, list))
    assert(all(simple_moves[i].score >= simple_moves[i+1].score for i in range(len(simple_moves)-1))) #Assert it is sorted

    if len(simple_moves) == 0:
        return Valuable(None, 0)

    letter_usage = {letter : 0 for letter in bag_set}
    for move in simple_moves:
        letter_usage[move.letter] += 1   

    max_score = simple_moves[0].score

    highest_score_moves = list(itertools.takewhile(lambda move : move.score == max_score, simple_moves))
    unique = [move for move in highest_score_moves if move.letter in [letter for letter, count in letter_usage.items() if count == 1]]
    result = min(unique if len(unique) else highest_score_moves, key = lambda move : letter_value(move.letter))

    return Valuable([[*result.coord, result.letter]], result.score)

def setup_free_functions(player_instance):                       
    global cell_value, letter_value, in_board

    cell_value = lambda row, col: player_instance.cellValue(row, col)
    letter_value = lambda letter : player_instance.letterValue(letter)
    in_board = lambda row, col : player_instance.inBoard(row, col)

def get_string(board : list, begin : Coord, end : Coord) -> str:
    assert(isinstance(board, list))
    assert(isinstance(board[0], list))
    assert(isinstance(begin, Coord))
    assert(isinstance(end, Coord))
    assert(coord_same_line(begin, end))

    if coord_same_row(begin, end):
        return ''.join(board[begin.row][x] for x in range(begin.col, end.col))
    return ''.join(board[y][begin.col] for y in range(begin.row, end.row))



class Player(base.BasePlayer):
    
    def __init__(self, name, dictionary, board, bag, bigBagSize):
        base.BasePlayer.__init__(self, name, dictionary, board, bag, bigBagSize) #always keep this line and DON't change it
        self.text = "Thomas The Dank Engine" #fill the name of your awesome player!
        self.other_passed = False
        self.passed = False
        setup_free_functions(self) 

    def update(self, board, bag, my_score, other_score, letters_in_bag):
        """
        Override inherited method from BasePlayer to keep track of whether the opponent has passed (away) or not

        """
        if other_score != self.otherScore: #Other player's score is updated, so he played stuff
            self.other_passed = False

        #Delegate call to the original update method
        base.BasePlayer.update(self, board, bag, my_score, other_score, letters_in_bag)


    def consider_pass(self):
        """
        It is obvious that no valid move can be made by palcing letters onto the board.
        This function chooses, which way of skipping will be chosen. Either change letters or pass depending on the circumstances
        """

        if self.lettersInBag == 0: #If there would not be anything to get, change nothing
            return None
        elif self.lettersInBag <= 7: #If there is no more than one bag remaining, get it all!
            return ''.join(sorted(self.bag, key = lambda letter : letter_value(letter))[:self.lettersInBag])

        elif self.lettersInBag > 24: #During the early game exhaust the bag as fast as possible
            return ''.join(self.bag) #by exchanging seven letters every time

        #Now we are in the late-game.. .There is 8 to 24 letters in the bag

        elif self.passed and self.other_passed: #If we need to keep playing to increase the score
            random.shuffle(self.bag)
            return ''.join(self.bag[:5])

        return None


    @staticmethod
    def compute_complex_move_value(board : list, coords : list) -> Valuable:
        assert(len(coords) >= 2)
        assert(isinstance(board, list))
        assert(isinstance(board[0], list))
        assert(isinstance(coords, list))
        horizontally = coord_same_row(coords[0], coords[-1])

        value = word_value(board, *find_maximal_word(board, coords[0], horizontally)) #Make the main word count
        for coord in coords: #And add all the perpendicular
            bounds = find_maximal_word(board, coord, not horizontally)
            if word_length(*bounds) > 1:
                value += word_value(board, *bounds)

        return value;


    @staticmethod
    def mix_letters(possible_letters : list, bag : list):

        assert(isinstance(bag, list) and len(bag)) 
        assert(isinstance(possible_letters, list))
        assert(all(isinstance(l, list) and len(l) > 1 for l in possible_letters))

        if len(possible_letters) == 1:
            for letter in possible_letters[0]:
                if letter in bag:
                    yield [letter]
            return

        for letter in possible_letters[0]:
            if letter in bag:
                bag.remove(letter)
                for remainder in Player.mix_letters(possible_letters[1:], bag):
                    yield [letter] + remainder
                bag.append(letter)
        return




    def try_possibilities(self, board : list, considered_coords : list, useable_squares : list) -> Valuable:
        assert(len(considered_coords) >= 2)

        are_in_row = coord_same_row(considered_coords[0], considered_coords[-1])
        begin, end = find_maximal_word(board, considered_coords[0], are_in_row)
        assert(word_length(begin, end) >= len(considered_coords))
        assert(coord_is_between(considered_coords[0], begin, end) and coord_is_between(considered_coords[-1], begin, end))

        bag = self.bag.copy()
        constrained = [coord for coord in considered_coords if len(useable_squares[coord].in_col) == 1]
        if any(a != b and useable_squares[constrained[a]].in_col[0].stuff == useable_squares[constrained[b]].in_col[0].stuff for a, b in itertools.product(range(len(constrained)), repeat=2)):
            return Valuable(None, 0) #If there are two constrained options with the same letter, return
        unconstrained = [coord for coord in considered_coords if len(useable_squares[coord].in_col) > 1 ]
        assert(len(constrained) + len(unconstrained) == len(considered_coords))

        #Place letters that need to be placed
        for constrained_coord in constrained:
            required_letter = useable_squares[constrained_coord].in_col[0].stuff
            assert(required_letter in bag)
            write(board, required_letter, *constrained_coord)
            bag.remove(required_letter)

        assert(len(unconstrained) <= len(bag))

        best = Valuable(None, 0)

        if len(unconstrained) == 0:
            word = get_string(board, begin, end)
            if word not in self.dictionary:
                return Valuable(None, 0)
            score = Player.compute_complex_move_value(board, considered_coords)
            moves = [[coord.row, coord.col, useable_squares[coord].in_col[0].stuff] for coord in considered_coords]
            return Valuable(moves, score)
        else:
            possible_letters = [[data.stuff for data in useable_squares[coord].in_col] for coord in unconstrained]
            for letter_variation in Player.mix_letters(possible_letters, bag):
                assert(len(letter_variation) == len(unconstrained))
                for coord, letter in zip(unconstrained, letter_variation):
                    write(board, letter, *coord)
                word = get_string(board, begin, end)
                if word not in self.dictionary:
                    continue
                score = Player.compute_complex_move_value(board, considered_coords)
                if score > best.score:
                    moves = [[coord.row, coord.col, useable_squares[coord].in_col[0].stuff] for coord in constrained ] 
                    moves += [[coord.row, coord.col, letter] for coord, letter in zip(unconstrained, letter_variation)]
                    best = Valuable(moves, score)
        return best








        

    def consider_complex_moves(self, board : list, heat_map : list, useable_squares : dict):
        assert(isinstance(board, list))
        assert(isinstance(board[0], list))
        assert(isinstance(heat_map, list))
        assert(isinstance(heat_map[0], list))
        assert(isinstance(useable_squares, dict))

        if not self.tournament:
            return Valuable(None, 0)
        best = Valuable(None, 0)

        for row in range(self.rows):
            coords_in_row = [coord for coord in useable_squares if coord.row == row]
            if not coords_in_row:
                continue
            coords_in_row.sort(key = lambda coord : coord.col)
            while True:
                while len(coords_in_row) and len(useable_squares[coords_in_row[0]].in_col) == 0:
                    coords_in_row.pop(0)
                if len(coords_in_row) <= 1:
                    break
                #Take at most seven of them, because we have only 7 letters in bag
                considered_coords = coords_in_row[:len(self.bag)]
                for i in range(1,len(considered_coords)):
                    if considered_coords[i].col != considered_coords[i-1].col + 1 or len(useable_squares[considered_coords[i]].in_col) == 0:
                        considered_coords = considered_coords[:i]
                        break

                used_letters = {letter : 0 for letter in self.bag}
                for index, coord in enumerate(considered_coords):
                    assert(len(useable_squares[coord].in_col))
                    for letter, score in useable_squares[coord].in_col:
                        used_letters[letter] += 1
                #TODO probably useless? considered_coords = considered_coords[:len([letter for letter, score in used_letters.items() if score > 0])] #If we can use at most x letters, then have at most x coords

                while len(considered_coords) > 1:
                    for coord in considered_coords: #Fill the coordinates with some string just to find word boundaries 
                        write(board, '!', *coord)
                    result = self.try_possibilities(board, considered_coords, useable_squares)
                    if result.score > best.score:
                        best = result
                    for coord in considered_coords:   #Restore the board
                        write(board, '', *coord)
                    considered_coords.pop()

                coords_in_row.pop(0)
                

        return best if best.score else Valuable(None, 0)


    def move(self):

        heat_map, useable_squares = build_heat_map(self.board)
        assert(in_board(*coord) and is_empty(self.board, *coord) for coord in useable_squares)
        assert(heat_map[row][col].in_col or heat_map[row][col].in_row for row, col in useable_squares)

        useable_squares = analyze_square_useability(self.board, heat_map, useable_squares, set(self.bag), self.dictionary)
        #Dictionary Coord(row, col) -> (in_col...[(letter, score)]
        #                               in_row... [(letter, score)] if those letters here placed to the board)

        simple_moves = find_simple_moves(self.board, heat_map, useable_squares, set(self.bag))
        best_simple_move = choose_best_simple_move(simple_moves, heat_map, useable_squares, set(self.bag))
        best_complex_move = self.consider_complex_moves(self.board, heat_map, useable_squares)
        
        chosen_move = None
        #We found no valid move, it is therefore wise to report a pass or change of letters
        if best_simple_move.score == 0 and best_complex_move.score == 0:
            chosen_move = self.consider_pass()
            self.passed = True
        else:
            chosen_move = best_simple_move.stuff if best_simple_move.score > best_complex_move.score else best_complex_move.stuff
            self.passed = False

        self.other_passed = True
        return chosen_move


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


        newBag = [letter for letter in lastPlayer.bag if letter not in lettersToReplace] if len(bag) == 0 else replaceLetters(lastPlayer, lettersToReplace, bag)
        lastPlayer.update(board, newBag, new_score, nextPlayer.myScore, len(bag))
        nextPlayer.update(board, nextPlayer.bag, nextPlayer.myScore, new_score, len(bag))
        return board_changes

    print("Wrong result from player.move; exit now")
    input()
    quit()
    return 0

if __name__ == "__main__":

    game_number = 0
    words = base.readDictionary('dic.txt') #words is represented as python-dictionray

    p1_wins, p2_wins, draws = 0,0,0
    p1_score, p2_score = 0,0

    while True:
        game_number += 1
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
    
    
        p1 = Player("FIRST", words, board, player1bag, len(bag))
        p2 = Player("SECOND", words, board, player2bag, len(bag))
        #p1.print()
    
        noChangeMoves = 0
        turn = 0
        while True:

    
            #p1.print()
            result = p1.move()
            s1 = afterMove(p1, result, p2, board, bag)   

    
    
            turn += 2
            #p2.print()
            result = p2.move()
            s2 = afterMove(p2, result, p1, board, bag)
        
    
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

        print("Game no. %d after %d turns:" % (game_number, turn))
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
        print("Total results out of %d games: " % (game_number))
        print("\tP1 won %d (%.2f%%) with score %d\n\tP2 won %d (%.2f%%) with score %d\n\tdraw   %d (%.2f%%)" % 
              (p1_wins, p1_wins*100 / game_number, p1_score, p2_wins, p2_wins * 100/game_number, p2_score, draws, draws*100/game_number))
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


    
    




