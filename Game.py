from random import choice
from PlaneValidator import PlaneValidator
from Plane import Plane
from Board import Board
import json

class Game:

    def __init__(self, player_board = None, computer_board = None):
        self.__player_board = player_board
        self.__computer_board = computer_board
        self.__difficulty = None
        self.__lost = False
        self.__won = False
        self.__player_kills = 0
        self.__computer_kills = 0
        self.__player_hits = []
        self.__computer_hits = []
        """Utility variables for AI V1"""
        self.__computer_landed_queue = []
        self.__computer_pending_queue = []
        """Utility variables for AI V2"""
        self.__possibilities_list = []

        if self.__player_board == None:
            self.__player_board = Board()
        if self.__computer_board == None:
            self.__computer_board = Board()

    
    @staticmethod
    def from_JSON(filename):

        with open(filename) as json_file:
            data = json.load(json_file)

            # Initializing an empty Game object
            game = Game()
            game.__player_board = Board(data['player_board'])
            game.__computer_board = Board(data['computer_board'])
            game.__difficulty = data['difficulty']
            game.__lost = data['lost']
            game.__won = data['won']
            game.__player_kills = data['player_kills']
            game.__computer_kills = data['computer_kills']
            game.__player_hits = data['player_hits']
            game.__computer_hits = data['computer_hits']
            game.__computer_landed_queue = data['computer_landed_queue']
            game.__computer_pending_queue = data['computer_pending_queue']
            game.__possibilities_list = data['possibilities_list']

            return game



    def dump_JSON(self, filename):
        data = {}
        data['player_board'] = self.__player_board.data
        data['computer_board'] = self.__computer_board.data
        data['difficulty'] = self.__difficulty
        data['lost'] = self.__lost
        data['won'] = self.__won
        data['player_kills'] = self.__player_kills
        data['computer_kills'] = self.__computer_kills
        data['player_hits'] = self.__player_hits
        data['computer_hits'] = self.__computer_hits
        data['computer_landed_queue'] = self.__computer_landed_queue
        data['computer_pending_queue'] = self.__computer_pending_queue
        data['possibilities_list'] = self.__possibilities_list
        
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    def set_difficulty(self, ai):
        """
        Sets the difficulty to the given value
        ai- integer between 1 and 2
        """
        self.__difficulty = ai
        if ai == 2:
            #special function that prepares the second AI
            self.first_time_run()


    @property
    def player_hits(self):
        """
        Returns the list of coords hit by the player
        """
        return self.__player_hits

    @property
    def lost(self):
        """
        Returns a bool that states whether the game is lost or not
        """
        return self.__lost

    @property
    def won(self):
        """
        Returns a bool that states whether the game is won or not
        """
        return self.__won

    @property
    def player_board(self):
        """
        Returns the player board
        """
        return self.__player_board

    @property
    def computer_board(self):
        """
        Returns the computer board
        """
        return self.__computer_board

    def computer_place_planes(self):
        """
        Randomly places 2 planes on the computer's board
        """
        correctly_placed_planes = 0
        while correctly_placed_planes < 2:
            direction = choice(["U", "D", "L", "R"])
            row = choice([1, 2, 3, 4, 5, 6, 7, 8])
            col = choice(["A", "B", "C", "D", "E", "F", "G", "H"])

            plane = Plane(direction, row, col)
            if PlaneValidator.computer_validate(plane, self.computer_board) == True:
                self.__computer_board.add_plane(plane)
                correctly_placed_planes += 1

    def player_place_plane(self, plane):
        """
        Places the given plane in the player board
        """
        self.__player_board.add_plane(plane)

    def player_attack(self, row, col):
        """
        Player attacks at coords (row, col)
        """
        row = row - 1
        col = ord(col) - ord("A")
        self.__player_hits.append( (row, col) )

        if self.__computer_board.data[row][col] == 0:
            self.__computer_board.hit_air(row, col)
        
        elif self.__computer_board.data[row][col] == 1:
            self.__computer_board.hit_hull(row, col)

        elif self.__computer_board.data[row][col] == 2:
            self.__computer_board.hit_cockpit(row, col)
            self.__player_kills += 1
            if self.__player_kills == 2:
                self.__won = True

    """AI 1"""

    @staticmethod
    def are_coords_valid(i, j):
        """
        Returns:
            True if the coords (i, j) are valid
            False otherwise
        """
        if (i < 0 or i > 7) or (j < 0 or j > 7):
            return False
        return True

    def computer_attack_coords(self, i, j):
        """
        Computer attacks coords i, j
        """
        self.__computer_hits.append( (i, j) )
        if self.__player_board.data[i][j] == 0:
            self.__player_board.hit_air(i, j)

        elif self.__player_board.data[i][j] == 1:
            self.__player_board.hit_hull(i, j)
            self.__computer_landed_queue.append( (i, j) )
                    
        elif self.__player_board.data[i][j] == 2:
            self.__player_board.hit_cockpit(i, j)
            self.__computer_kills += 1
            if self.__computer_kills == 2:
                self.__lost = True

    def computer_random_attack(self):
        """
        Attacks at a random spot
        """
        computer_chose = False
        while computer_chose == False:
            i = choice([0, 1, 2, 3, 4, 5, 6, 7])
            j = choice([0, 1, 2, 3, 4, 5, 6, 7])
            if not (i, j) in self.__computer_hits:
                computer_chose = True
                self.computer_attack_coords(i, j)

    def computer_attack_AI(self):
        """
        AI 1- decides whether to hit a random spot(if no elements in the landed queue or pending queue exist)
                           or to hit near a spot that was a confirmed hit(either from the pending queue or the landed queue)
        """
        if len(self.__computer_landed_queue) == 0 and len(self.__computer_pending_queue) == 0:
            self.computer_random_attack()
        
        else:
            computer_chose = False
            while computer_chose == False:
                if len(self.__computer_pending_queue) != 0:
                    while len(self.__computer_pending_queue) != 0 and computer_chose == False:
                        i = self.__computer_pending_queue[0][0]
                        j = self.__computer_pending_queue[0][1]
                        self.__computer_pending_queue.pop(0)
                    
                        if not (i, j) in self.__computer_hits:
                            computer_chose = True
                            self.computer_attack_coords(i, j)

                elif len(self.__computer_landed_queue) != 0:
                    i = self.__computer_landed_queue[0][0]
                    j = self.__computer_landed_queue[0][1]
                    self.__computer_landed_queue.pop(0)

                    di = [0, 0, 1, -1]
                    dj = [1, -1, 0, 0]

                    for x in range(0, 4):
                        next_i = i + di[x]
                        next_j = j + dj[x]
                        if Game.are_coords_valid(next_i, next_j):
                            self.__computer_pending_queue.append( (next_i, next_j) )
                else:
                    self.computer_random_attack()

    """AI 2"""

    def first_time_run(self):
        """
        Initializes variables
        """
        self.initialize_list()
        self.remove_corners()

    def find_coords(self, x ):
        """
        Returns the position of the coords given in the possibilities list
        """
        for i in range(0, len( self.__possibilities_list ) ):
            if x == self.__possibilities_list[i]:
                return i
        return -1

    def initialize_list(self):
        """
        Initializes the possibilities list with all elements from the 8 x 8 board
        """
        for i in range(0, 8):
            for j in range(0, 8):
                self.__possibilities_list.append( (i, j) )

    def remove_corners(self):
        """
        Removes the 2 x 2 corners from the possibilities list
        (no cockpits can be placed in those positions)
        """
        corners = [ (0, 0), (0, 1), (1, 0), (1, 1), (0, 6), (0, 7), (1, 6), (1, 7),
                   (6, 0), (6, 1), (7, 0), (7, 1), (6, 6), (6, 7), (7, 6), (7, 7) ]

        for i in range (0, len(corners)):
            pos = self.find_coords( corners[i] )
            self.__possibilities_list.pop(pos)

    """attack function"""

    def draw_plane(self, i, j):
        """
        Will try to identify the exact position and coords of the downed plane
        Then remove those coords from the possibilities list
        (based on the fact that if a plane is placed on the first 2 or last 2 lines or columns,
        there can only be one way to place it)
        """
        can_be_determined = False
        plane = 0
        plane_parts = []
        if i == 0 or i == 1:
            #first 2 lines
            plane = Plane("U", i + 1, chr(j + ord("A")))
            can_be_determined = True
        
        elif i == 6 or i == 7:
            #last 2 lines
            plane = Plane("D", i + 1, chr(j + ord("A")))
            can_be_determined = True
        
        elif j == 0 or j == 1:
            #first 2 columns
            plane = Plane("L", i + 1, chr(j + ord("A") ))
            can_be_determined = True

        elif j == 6 or j == 7:
            #last 2 columns
            plane = Plane("R", i + 1, chr( j + ord("A") ))
            can_be_determined = True
        else:
            can_be_determined = False

        if can_be_determined == True:
            plane_parts = plane.get_body()
            for x in plane_parts:
                pos = self.find_coords(x)
                if pos != -1:
                    self.__possibilities_list.pop(pos)
            
    def computer_attack_coords_v2(self, i, j):
        """
        Computer attacks coords (i, j)
        """
        pos = self.find_coords( (i, j) )
        self.__possibilities_list.pop(pos)

        if self.__player_board.data[i][j] == 0:
            self.__player_board.hit_air(i, j)

        elif self.__player_board.data[i][j] == 1:
            self.__player_board.hit_hull(i, j)
            self.__computer_landed_queue.append( (i, j) )
                    
        elif self.__player_board.data[i][j] == 2:
            self.__player_board.hit_cockpit(i, j)
            self.__computer_kills += 1
            if self.__computer_kills == 2:
                self.__lost = True
            else:
                self.draw_plane(i, j)

    def computer_random_attack_v2(self):
        """
        Attacks a random spot in the possibilities list
        """
        x = choice(self.__possibilities_list)
        i = x[0]
        j = x[1]
        self.computer_attack_coords_v2(i, j)

    def computer_attack_AI_v2(self):
        """
        AI 2- decides whether to hit a random spot if pending queue and landing queue are empty
        """
        if len(self.__computer_landed_queue) == 0 and len(self.__computer_pending_queue) == 0:
            self.computer_random_attack_v2()
        
        else:
            computer_chose = False
            while computer_chose == False:
                if len(self.__computer_pending_queue) != 0:
                    while len(self.__computer_pending_queue) != 0 and computer_chose == False:
                        i = self.__computer_pending_queue[0][0]
                        j = self.__computer_pending_queue[0][1]
                        self.__computer_pending_queue.pop(0)
                    
                        if (i, j) in self.__possibilities_list:
                            computer_chose = True
                            self.computer_attack_coords_v2(i, j)

                elif len(self.__computer_landed_queue) != 0:
                    i = self.__computer_landed_queue[0][0]
                    j = self.__computer_landed_queue[0][1]
                    self.__computer_landed_queue.pop(0)

                    di = [0, 0, 1, -1]
                    dj = [1, -1, 0, 0]

                    for x in range(0, 4):
                        next_i = i + di[x]
                        next_j = j + dj[x]
                        if Game.are_coords_valid(next_i, next_j):
                            self.__computer_pending_queue.append( (next_i, next_j) )
                else:
                    self.computer_random_attack_v2()

    def computer_move(self):
        """
        Computer's move, based on difficulty
        """
        if self.__difficulty == 1:
            self.computer_attack_AI()
        else:
            self.computer_attack_AI_v2()

    """Printing stuff"""

    def print_player_table(self):
        print(self.__player_board.str_player())

    def print_computer_table(self):
        print(self.__computer_board.str_computer())
        #print(self.__computer_board.str_player())    
