class Plane:
    def __init__(self, direction, row, col):
        self.__direction = direction
        self.__row = row
        self.__col = col
    
    @property
    def cockpit_coords(self):
        """
        Returns the usable coords of the cockpit
        """
        return (self.__row - 1, ord(self.__col) - ord('A') )

    @property
    def direction(self):
        """
        Returns the direction of the plane
        A char from [U, D, L, R]
        """
        return self.__direction

    @property
    def row(self):
        """
        Returns the row of the plane's cockpit
        An integer between [1, 8]
        """
        return self.__row
    
    @property
    def col(self):
        """
        Returns the column of the plane's cockpit
        A char between [A, H]
        """
        return self.__col

    @property
    def body(self):
        """
        Returns the list of coords the plane's body occupies
        """
        i = self.row - 1
        j = ord(self.col) - ord("A")
        direction = self.direction
        plane_parts = []

        if direction == "U":
            plane_parts = [(i + 1, j), (i + 2, j), (i + 3, j), (i + 3, j - 1), (i + 3, j + 1), (i + 1, j - 1),
                           (i + 1, j - 2), (i + 1, j + 1), (i + 1, j + 2)]
            
        elif direction == "D":
            plane_parts = [(i - 1, j), (i - 2, j), (i - 3, j), (i - 3, j - 1), (i - 3, j + 1), (i - 1, j - 1),
                           (i - 1, j - 2), (i - 1, j + 1), (i - 1, j + 2)]

        elif direction == "L":
            plane_parts = [(i, j + 1), (i, j + 2), (i, j + 3), (i - 1, j + 3), (i + 1, j + 3), (i - 1, j + 1),
                           (i - 2, j + 1), (i + 1, j + 1), (i + 2, j + 1)]

        else:
            plane_parts = [(i, j - 1), (i, j - 2), (i, j - 3), (i - 1, j - 3), (i + 1, j - 3), (i - 1, j - 1),
                           (i - 2, j - 1), (i + 1, j - 1), (i + 2, j - 1)]

        return plane_parts