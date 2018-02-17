import numpy


class Board:

    squares = []
    units = []

    def __init__(self, map_size):
        self.size = map_size
        self.x = map_size[0]
        self.y = map_size[1]
        self.move_preview = False
        for y in range(map_size[1]):
            for x in range(map_size[0]):
                self.squares.append(Square([x + 1, y + 1], self))
#Can't compare lists and tuples, but this should be a tuple. Fix later maybe

    def display(self):
        """Function takes the list of grid squares and prints them in a grid w/
        coordinates. Also keeps track of where each unit is on the grid and 
        whether or not each square is currently occupied.
        """
        for i in range(len(self.squares)):#This loop makes the units show up in the grid. Tried removing it and putting it elsewhere but it breaks every thing.
            for j in range(len(self.units)):
                if self.squares[i].coords == self.units[j].coords:
                    self.squares[i].symbol = self.units[j].symbol
                    self.squares[i].filled = True
                    break #break statement is necessary. Otherwise only one unit shows up.
                elif self.move_preview == True and self.squares[i].filled == False:
                    if any(ord(char) > 126 for char in self.squares[i].symbol):
                        break
                elif self.move_preview == False and self.squares[i].filled == False:
                    if any(ord(char) > 126 for char in self.squares[i].symbol):
                        self.squares[i].symbol = '[]'
                elif self.squares[i].coords != self.units[j].coords:
                    self.squares[i].symbol = '[]'
                    self.squares[i].filled = False
        for i in range(self.x):
            print(i + 1, end = '\t')
        for i in range(len(self.squares)):
            if i % self.x == 0:
                print((i + 1) // 10)

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
    def __init__(self, coords, board, symbol = '[]', filled = False):
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.symbol = symbol
        self.filled = filled

    def get_coords(self):
        return self.coords

class Unit:
    valid_moves = []
    def __init__(self, symbol, coords, board, hp = 1, speed=3, atk_range = 1, atk_power = 1):
        self.symbol = symbol
        self.coords = coords
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.hp = hp
        self.speed = speed
        self.atk_range = atk_range
        self.atk_power = atk_power
        board.units.append(self)


    def get_coords(self):
        return self.coords

    def player_turn(self, choice):
        turn_options = ["move", "attack"]
        while choice not in turn_options:
            choice = input('What would you like to do?')
        if choice == "move":
            self.get_valid_spaces()
            self.move(input("Where do you want to go?").split())
        elif choice == "attack":
            self.attack(input("Which square would you like to attack?").split())

    def move(self, coords):
        valid_input = False

        while not valid_input:
            try:
                destination = [int(coords[0]), int(coords[1])]
            except:
                if coords == ['cancel']:
                    board.move_preview = False
                    board.display()
                    self.player_turn(input('What would you like to do?'))
                    return None
                else:
                    coords = input('Incorrect input. Try again!').split()
                    continue
            if destination in self.valid_moves:
                self.x = destination[0]
                self.y = destination[1]
                self.coords = [self.x, self.y]
                for i in range(len(board.squares)):
                    for j in range(len(board.units)):
                        if board.squares[i].coords != board.units[j].coords:
                            board.squares[i].symbol = '[]'
                            board.squares[i].filled = False
                        elif board.squares[i].coords == board.units[j].coords:
                            board.squares[i].symbol = board.units[j].symbol
                            board.squares[i].filled = True
                valid_input = True
            elif destination not in self.valid_moves:
                return self.move(input("That is not a valid move.").split())

        del(self.valid_moves[:])

    def attack(self, coords):
        valid_targets = []
        valid_input = False

        while not valid_input:
            try:
                target_space = [int(coords[0]), int(coords[1])]

            except:
                if coords == ['cancel']:
                    board.move_preview = False
                    board.display()
                    self.player_turn(input('What would you like to do?'))
                    return None
                else:
                    coords = input('Incorrect input. Try again!').split()
                    continue

            for i in range(len(board.units)):
                if board.get_distance(self, board.units[i].x, board.units[i].y) <= (self.atk_range):
                    valid_targets.append(board.units[i].coords)

            if target_space in valid_targets:
                for i in range(len(board.units)):
                    if board.units[i].coords == target_space:
                        board.units[i].hp -= self.atk_power
                        if board.units[i].hp <= 0:
                            board.units[i].coords = [100, 100]
                    valid_input = True
            elif target_space not in valid_targets:
                return self.attack(input('That is not a valid choice').split())

    def get_valid_spaces(self):
        for i in range(len(board.squares)):
            distance = board.get_distance(self, board.squares[i].x, board.squares[i].y)
            if distance <= self.speed and board.squares[i].filled == False:
                board.squares[i].symbol = '[░]'
                self.valid_moves.append(board.squares[i].coords)
                board.move_preview = True
            elif distance <= (self.speed + self.atk_range):
                board.squares[i].symbol = '[▒]'
                board.move_preview = True# Start here. This needs  to be fixed
        board.display()


board_size = (10, 8)
board = Board(board_size)
player2 = Unit('[b]', [10, 8], board)
player = Unit('[a]', [10, 7], board)


done = 0
turn_options = ["move", "attack"]
print(board.units)
for i in range(len(board.units)):
    print(board.units[i].coords)
while not done:
    board.display()
    player.player_turn(input('What would you like to do?'))
