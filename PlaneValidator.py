from Plane import Plane
from Board import Board

class PlaneValidator:

    @classmethod
    def basic_check(cls, plane):
        """
        Checks if the input given is at least in the possible range
        """
        
        if not plane.direction in ["U", "D", "L", "R"]:
            return False
        
        try:
            int(plane.row)
        except:
            return False
        
        if plane.row < 1 or plane.row > 8:
            return False
        
        if plane.col < "A" or plane.col > "H":
            return False
        return True

    @classmethod
    def does_it_fit(cls, plane):
        """
        Returns:
            True- plane fits inside 8 x 8 board
            False- plane has parts that are outside
        """
        plane_parts = plane.get_body()
        
        for i in range(0 , len(plane_parts) ):
            if (plane_parts[i][0] < 0 or plane_parts[i][0] > 7) or (plane_parts[i][1] < 0 or plane_parts[i][1] > 7):
                return False
        return True

    @classmethod      
    def no_overlap(cls, plane, board):
        """
        Returns:
            True- new plane doesn't overlap with anything on the board
            False- overlaps
        """
        plane_parts = plane.get_body()
        plane_parts.append((plane.row - 1, ord(plane.col) - ord("A")))
        table = board.data
        for i in range(0, len(plane_parts)):
            if table[ plane_parts[i][0] ][ plane_parts[i][1] ] != 0:
                return False
        return True
            
    @classmethod
    def player_validate(cls, plane, board):
        if cls.basic_check(plane) == False:
            raise ValueError("Invalid input")
        else:
            if cls.does_it_fit(plane) == False:
                raise ValueError("Plane doesn't fit in the board")
            else:
                if cls.no_overlap(plane, board) == False:
                    raise ValueError("Plane overlaps with another plane")
                else:
                    return True

    @classmethod
    def computer_validate(cls, plane, board):
        if cls.basic_check(plane) == False:
            return False
        else:
            if cls.does_it_fit(plane) == False:
                return False
            else:
                return cls.no_overlap(plane, board)

