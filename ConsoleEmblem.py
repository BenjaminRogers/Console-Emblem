import numpy


class Board:

    squares = []
    units = []

    def __init__(self, map_size):
        self.size = map_size
        self.x = map_size[0]
        self.y = map_size[1]

        for y in range(map_size[1]):
            for x in range(map_size[0]):
                self.squares.append(Square([x + 1, y + 1]))
                #Can't compare lists and tuples, but this should be a tuple. Fix later
    def display(self):
        """Function takes the list of grid squares and prints them in a grid w/ coordinates. 
        """
        for i in range(self.x):
            print(i + 1, end = '\t')
        for i in range(len(self.squares)):
            if i % self.x == 0:
                print((i + 1) // 10)
            for j in range(len(self.units)):
                if self.squares[i].coords == self.units[j].coords:
                    self.squares[i].symbol = self.units[j].symbol
            print(self.squares[i].symbol, end = '\t')
        print(self.y)

    @staticmethod
    def get_distance(unit, x, y):
        """This function is used to get the distance, not counting diagonals, between any two spaces on the grid."""
        distance = 0
        distance += abs(unit.coords[0] - x)
        distance += abs(unit.coords[1] - y)
        return distance


class Square:
    def __init__(self, coords, symbol = '[]'):
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.symbol = symbol

    def get_coords(self):
        return self.coords

class Unit:
    valid_moves = []
    def __init__(self, symbol, coords, board, speed=3, atk_range = 1):
        self.symbol = symbol
        self.coords = coords
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.speed = speed
        self.atk_range = atk_range
        board.units.append(self)

    def get_coords(self):
        return self.coords

    def move(self, coords):
        valid_input = False

        while not valid_input:
            try:
                destination = [int(coords[0]), int(coords[1])]
            except:
                coords = input('Incorrect input. Try again!').split()
                continue
            if destination in self.valid_moves:
                self.x = destination[0]
                self.y = destination[1]
                self.coords = [self.x, self.y]
                for i in range(len(board.squares)):
                    for j in range(len(board.units)):
                        if board.squares[i].coords != board.squares[j].coords:
                            board.squares[i].symbol = '[]'
                valid_input = True
            elif destination not in self.valid_moves:
                return self.move(input("That is not a valid move.").split())

        del(self.valid_moves[:])

    def attack(self, coords):
        valid_targets = []
        valid_input = False
        for i in range(len(board.units)):
            if board.get_distance(self, board.units[i].x, board.units[i].y) <= self.speed:
                valid_targets.append(board.units[i].coords)
        while not valid_input:
            try:
                target = [int(coords[0], int(coords[1]))]
            except:
                coords = input('Incorrect input. Try again!').split()
                continue
            if target in valid_targets:
                pass#Start here!

    def get_valid_spaces(self, choice):
        if choice == 'move':
            for i in range(len(board.squares)):
                distance = board.get_distance(self, board.squares[i].x, board.squares[i].y)
                if distance <= self.speed:
                    board.squares[i].symbol = '[▒]'
                    self.valid_moves.append(board.squares[i].coords)



board_size = (10, 8)
board = Board(board_size)
player = Unit('[a]', [5, 6], board)
player2 = Unit('[b]', [10, 8], board)
done = 0
turn_options = ["move", "attack"]
while not done:
    board.display()
    player_choice = input("What do you want to do?")
    while player_choice not in turn_options:
        player_choice = input("That is not a valid option. Try again")
        continue
    player.get_valid_spaces(player_choice)
    board.display()
    if player_choice == 'move':
        move_to = input('Where do you want to go?').split()
        player.move(move_to)
    elif player_choice == 'attack':
        target = input('Which square would you like to attack?').split()
        player.attack(target)
