import numpy


class Player:
    def __init__(self, map_name):
        self.map_name = map_name
        self.available_moves = len([o.coords for o in self.map_name.blue_team])

    def choose_unit(self):
        move_list = [o.coords for o in self.map_name.blue_team]
        while True:
            unit_chosen = input('Which unit would you like to pick?')
            check_int = unit_chosen.split()

            try:
                check_int = [int(check_int[0]), int(check_int[1])]
                unit_chosen = check_int
            except Exception as e:
                print(e)
                continue
            if unit_chosen in move_list:
                for i in range(len(self.map_name.blue_team)):
                    if self.map_name.blue_team[i].coords == unit_chosen:
                        unit_chosen = self.map_name.blue_team[i].player_turn()

            else:
                print('That is not one of your units.')
                continue
            if not unit_chosen:
                break
class Board:

    squares = []
    units = []
    blue_team = []
    red_team = []

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
            print('{:^4}'.format(i + 1), end='\t')
        for i in range(len(self.squares)):
            if i % self.x == 0:
                print((i + 1) // 10)

            # set text centered in a field 4 characters wide
            print('{:^4}'.format(self.squares[i].symbol), end='\t')

        print(self.y)

    @staticmethod #Why does this take x, y coordinates seperately? Fix this garbo
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
    def __init__(self, symbol, coords, map, hp = 1, speed=3, atk_range = 1, atk_power = 1):
        self.map = map
        self.symbol = symbol
        self.coords = coords
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.hp = hp
        self.speed = speed
        self.atk_range = atk_range
        self.atk_power = atk_power
        map.units.append(self)
        if self.symbol.startswith('[|'):
            self.team = 'Red'
            map.red_team.append(self)
        else:
            self.team = 'Blue'
            map.blue_team.append(self)


    def get_coords(self):
        return self.coords

    def player_turn(self):
        choice = input('What do you want to do?')
        turn_options = ["move", "attack", "cancel"]
        while choice not in turn_options:
            choice = input('I did not understand. What do you want to do?')
        if choice == "move":
            self.get_valid_spaces()
            self.move()
        elif choice == "attack":
            self.attack()
        elif choice == "cancel":
            return 'cancel'
        elif choice == 'done':
            return 'done'
#Fix move, fix attack. Player_turn and player.take_turn on the right track now. Need to changes those names later to make them more distinct
    def move(self):


        while True:
            coords_chosen = input('To which square would you like to move?')
            check_int = coords_chosen.split()
            try:
                check_int = [int(check_int[0]), int(check_int[1])]
                coords_chosen = check_int
            except Exception as e:
                print(e)
                if coords_chosen == 'cancel':
                    self.map.move_preview = False
                    self.map.display()
                    return 'cancel'
                continue


            if coords_chosen in self.valid_moves:
                self.x = coords_chosen[0]
                self.y = coords_chosen[1]
                self.coords = [self.x, self.y]
                for i in range(len(self.map.squares)):
                    for j in range(len(self.map.units)):
                        if self.map.squares[i].coords != self.map.units[j].coords:
                            self.map.squares[i].symbol = '[]'
                            self.map.squares[i].filled = False
                        elif self.map.squares[i].coords == self.map.units[j].coords:
                            self.map.squares[i].symbol = self.map.units[j].symbol
                            self.map.squares[i].filled = True
                player.available_moves -= 1
                del (self.valid_moves[:])
                return 'done'
            elif coords_chosen not in self.valid_moves:
                continue

    def attack(self):
        valid_targets = []
        while True:
            target_space = input('Which square would you like to attack?')
            check_int = target_space.split()
            try:
                check_int = [int(check_int[0]), int(check_int[1])]
                target_space = check_int
            except Exception as e:
                print(e)
                if target_space == 'cancel':
                    return 'cancel'
                continue
            for i in range(len(self.map.units)):
                if board.get_distance(self, self.map.units[i].x,self.map.units[i].y) <= self.atk_range:
                    if self.map.units[i] in self.map.red_team:
                        valid_targets.append(self.map.units[i].coords)

            if target_space in valid_targets:
                for i in range(len(self.map.units)):
                    if self.map.units[i].coords == target_space:
                        self.map.units[i].hp -= self.atk_power
                        if self.map.units[i].hp <= 0:
                            self.map.units[i].coords = [100, 100]
                            for j in range(len(self.map.red_team)):
                                if self.map.red_team[j] == self.map.units[i]:
                                    del self.map.red_team[j]
                return 'done'

            elif target_space not in valid_targets:
                print('That is not a valid target')
                continue
    def get_valid_spaces(self):
        for i in range(len(self.map.squares)):
            distance = self.map.get_distance(self, self.map.squares[i].x, self.map.squares[i].y)
            if distance <= self.speed and self.map.squares[i].filled == False:
                self.map.squares[i].symbol = '[░]'
                self.valid_moves.append(self.map.squares[i].coords)
                self.map.move_preview = True
            elif distance <= (self.speed + self.atk_range):
                self.map.squares[i].symbol = '[▒]'
                self.map.move_preview = True
        self.map.display()


board_size = (10, 8)
board = Board(board_size)

unit3 = Unit('[c]', [1, 1], board)
unit2 = Unit('[|b]', [1, 2], board)
unit = Unit('[a]', [1, 3], board) #Movable character

player = Player(board)

done = 0



while not done:
    player.available_moves = len(board.blue_team)

    while player.available_moves > 0:
        board.display()
        selected_unit = player.choose_unit()




    print('enemy turn goes here')