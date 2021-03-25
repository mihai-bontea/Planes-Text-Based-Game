from Plane import Plane
from texttable import Texttable


class Board:

    def __init__(self, d = None):
        if d == None:
            self.__data = [[0 for _ in range(8)] for _ in range(8)]
        else:
            self.__data = d

    @property
    def data(self):
        """
        Returns the board
        """
        return self.__data

    def print_visual(self):
        """
        Prints the board in an easier to see way
        """
        dictionary = { 0 : " " , 2: "◙" , 1 : "█" }
        for i in range(0, 8):
            for j in range(0, 8):
                print( dictionary[self.data[i][j]], end = "")
            print()
                
    def add_plane(self, plane):
        """
        Represents a plane in the board
        """
        x = plane.cockpit_coords[0]
        y = plane.cockpit_coords[1]

        self.__data[x][y] = 2   #cockpit
        hull = plane.body
        for i in range(0, len(hull)):
            self.__data[ hull[i][0] ][ hull[i][1] ] = 1

    def hit_air(self, row, col):
        """
        Represent that air was hit at coords (row, col)
        """
        self.__data[row][col] = 3

    def hit_hull(self, row, col):
        """
        Represent that hull was hit at coords (row, col)
        """
        self.__data[row][col] = 4

    def hit_cockpit(self, row, col):
        """
        Represent that cockpit was hit at coords (row, col)
        """
        self.__data[row][col] = 5
    
    def str_player(self):
        """
        String representation of the player's board
        """
        t = Texttable()
        d1 = {0: " ", 1: "▇", 2: "▩", 3: "◌", 4: "➳" , 5: "☠"}
        for i in range(0, 8):
            lst = self.data[i][:]
            for j in range(0, 8):
                lst[j] = d1[lst[j]]
            t.add_row(lst)
        return t.draw()

    def str_computer(self):
        """
        String representation of the computer's board
        """
        t = Texttable()
        d2 = {0: " ", 1: " ", 2: " ", 3: "◌", 4: "➳" , 5: "☠"}
        for i in range(0, 8):
            lst = self.data[i][:]
            for j in range(0, 8):
                lst[j] = d2[lst[j]]
            t.add_row(lst)
        return t.draw()

        