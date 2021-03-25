from Plane import Plane
from PlaneValidator import PlaneValidator
from Game import Game
import os

class UI:

    def __init__(self, game):
        self.__game = game
        self.__difficulty = 0

    def choose_difficulty(self):
        string = "\nAI 1"
        string += "\n\t✯ Will fire randomly in the 64 squares until it hits a plane"
        string += "\n\t✯ When it hits a plane, will try to hit adjacent blocks until it finds the cockpit"
        
        string += "\n\nAI 2"
        string += "\n\t✯ Will fire randomly in 48 squares excluding the corners until it hits a plane"
        string += "\n\t✯ 25 percent more chances to hit the cockpit during a random strike"
        string += "\n\t✯ When circumstances allow it, will figure your destroyed plane position so it doesn't hit any square from it again"
        
        print(string)
        is_input_correct = False
        while is_input_correct == False:
            is_input_correct = True
            user_input = input("Choose 1 or 2: ")

            try:
                int(user_input)
            except:
                is_input_correct = False
            else:
                user_input = int(user_input)
            
            if is_input_correct:
                if user_input != 1 and user_input != 2:
                    is_input_correct = False
        
        self.__game.set_difficulty(user_input)

    def choose_state(self):
        print("Do you want to start from where you left off? Y/N")
        is_input_correct = False
        while is_input_correct == False:
            user_input = input()
            if user_input.capitalize() == "Y":
                if os.stat("gamestate.json").st_size != 0:
                    self.__game = Game.from_JSON("gamestate.json")
                    if self.__game.won or self.__game.lost:
                        print("Cannot continue from last game because the game was finished.")
                    else:
                        self.play()
                        is_input_correct = True
                else:
                    print("Backup file is empty!")
            elif user_input.capitalize() == "N":
                self.__game = Game()
                self.choose_difficulty()
                self.place_planes()
                self.__game.computer_place_planes()
                self.play()
                is_input_correct = True
            else:
                print(user_input + " is not a valid option!")

    def print_update(self):
        """
        Prints the new boards after an update
        """
        print("Player's board: ")
        self.__game.print_player_table()

        print("\n")
        print("Computer's board: ")
        self.__game.print_computer_table()
        print("\n\n")

    def print_init(self):
        string = "\tEnter the orientation(U = Up, D = Down, L = Left, R = Right), and coords of the cabin(row:(1-8), col:(A-H))"
        print(string)

    def place_planes(self):
        self.print_update()
        self.print_init()
        placed_planes = 0
        while placed_planes < 2:
            user_input = input()
            is_input_correct = True

            # Checking if the number of arguments is correct
            try:
                direction, row, col = user_input.split(" ")
                direction = direction.strip()
                row = row.strip()
                col = col.strip()
            except:
                is_input_correct = False
                print("Too few arguments")
            
            # Checking if the row is an integer
            if is_input_correct:
                try:
                    int(row)
                except:
                    is_input_correct = False
                    print("Row must be an integer")
                else:
                    row = int(row)

            direction = direction.capitalize()
            col = col.capitalize()
            if is_input_correct:
                plane = Plane(direction, row, col)
                board = self.__game.player_board
                try:
                    PlaneValidator.player_validate(plane, board)
                except Exception as e:
                    is_input_correct = False
                    print( e  )

            
            if is_input_correct:
                self.__game.player_place_plane(plane)
                placed_planes += 1
                self.print_update()
                
    def play(self):
        
        # Save game state after all planes were placed
        self.__game.dump_JSON("gamestate.json")

        while self.__game.won == False and self.__game.lost == False:
            print("Choose the coordinates that you wanna attack: 1-8, A-H: ")
            input_was_given = False
            user_input = None
            
            while input_was_given == False:
                user_input = input()
                is_input_correct = True

                if (user_input.strip().upper() == "EXIT"):
                    input_was_given = True
                    continue

                # Checking if the number of arguments is right
                try:
                    row, col = user_input.split(" ")
                    row = row.strip()
                    col = col.strip()
                except:
                    is_input_correct = False
                    print("Too few arguments")

                # Checking if row is an integer
                if is_input_correct:
                    try:
                        int(row)
                    except:
                        is_input_correct = False
                        print("Row must be an integer")
                    else:
                        row = int(row)

                # Checking if row is a number
                if is_input_correct:
                    if row < 1 or row > 8:
                        is_input_correct = False
                        print("Row must be between 1 and 8")

                # Checking if column is between 'A' and 'H'
                if is_input_correct:
                    col = col.capitalize()
                    if col < "A" or col > "H":
                        is_input_correct = False
                        print("Col must be between A and H")
            
                if is_input_correct:
                    xrow = row - 1
                    xcol = ord(col) - ord("A")
                    player_hits = self.__game.player_hits
                    if (xrow, xcol) in player_hits or [xrow, xcol] in player_hits:
                        is_input_correct = False
                        print("You already attacked this area once")
                    else:
                        input_was_given = True

            if (user_input.strip().upper() == "EXIT"):
                print("Saving and exiting...")
                break

            self.__game.player_attack(row, col)

            self.__game.computer_move()

            # Storing the state of the game at every iteration
            self.__game.dump_JSON("gamestate.json")

            self.print_update()


        if self.__game.won == True:
            print("You won!☻")
        elif self.__game.lost == True:
            print("You lost...")
