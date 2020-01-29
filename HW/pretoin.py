from enum import Enum
from queue import Queue
import sys

class SyntaxError(Exception):
    pass

class operation(Enum):
    PLUS    = "wfwefwefewef"
    MINUS   = "wfwefwefwdef"
    MUL     = "wfwefwefwedf"
    DIV     = "wfwefwefweff"
    POWER   = "wfwefwefxwef"

    def __str__(val):                                                            
        table = {operation.PLUS: '+', operation.MINUS: '-', operation.MUL : '*', operation.DIV : '/', operation.POWER: '**'} 
        return table[val]


def needs_parens_left(main, sub):
    precedence = {operation.PLUS : 1, operation.MINUS :1 , operation.MUL : 3, operation.DIV : 3, operation.POWER : 5}
    return precedence[sub] < precedence[main]

def needs_parens_right(main, sub):
    precedence = {operation.PLUS : 1, operation.MINUS :2 , operation.MUL : 3, operation.DIV : 4, operation.POWER : 5}
    return precedence[sub] < precedence[main] or (sub == main and main in (operation.DIV, operation.MINUS))


class literal_node:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class operation_node:
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def __str__(self):
        l = str(self.left)
        r = str(self.right)

        if type(self.left) == operation_node and needs_parens_left(self.operation, self.left.operation):
            l = '(' + l + ')'
        if type(self.right) == operation_node and needs_parens_right(self.operation, self.right.operation):
            r = '(' + r + ')'

        return l + str(self.operation) + r;

def tokenize(string : str):
    tokens = Queue()
    index = 0
    operators = {'+' : operation.PLUS, '-' : operation.MINUS, '/': operation.DIV}
    while index < len(string):
        if string[index] == ' ':
            index += 1
        elif string[index] in operators:
            tokens.put(operators[string[index]])
            index += 1
        elif string[index] == '*':
            if index < len(string) - 1 and string[index + 1] == '*':
                tokens.put(operation.POWER)
                index += 2
            else:
                tokens.put(operation.MUL)
                index += 1
        elif string[index].isdigit():
            start = index
            index += 1
            while index < len(string) and string[index].isdigit():
                index += 1
            tokens.put(int(string[start:index]))
        else:
            raise SyntaxError("Invalid syntax!")
    
    return tokens
    
def build_tree(tokens : Queue):

    def build_tree_internal(tokens : Queue):
        if tokens.empty():
            raise SyntaxError("Invalid syntax!")
        first = tokens.get()
        if type(first) == int:
            return literal_node(first)

        left = build_tree_internal(tokens)
        right = build_tree_internal(tokens)
        return operation_node(first, left, right)

    root = build_tree_internal(tokens)
    if not tokens.empty():
        raise SyntaxError("Invalid syntax!")
    return root


if  __name__ == '__main__':

    string = input()
    try:
        tokens = tokenize(string)
        root = build_tree(tokens)
        print(root)
    except SyntaxError:
        print('ERROR')


