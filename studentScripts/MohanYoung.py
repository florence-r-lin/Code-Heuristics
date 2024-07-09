#file: final.py
#name: Tulika Mohan and Katharine Young

import random

# copied from hw10pr2
def inarow_Neast( ch, r_start, c_start, A, N ):
    """start from r_start and c_start and check for 
       N-in-a-row eastward of element ch, returning 
       True or False, as appropriate
    """
    NR = len(A)   
    NC = len(A[0])
    if r_start >= NR or c_start+ N-1 >= NC:   
        return False   
    for i in range(N):                  
        if A[r_start][c_start+i] != ch:   
            return False                
    return True   

def inarow_Nsouth( ch, r_start, c_start, A ,N):
    """start from r_start and c_start and check for 
       N-in-a-row southward of element ch, returning 
       True or False, as appropriate
    """
    NR = len(A)   
    NC = len(A[0])
    if r_start+N-1 >= NR or c_start >= NC:   
        return False   
    for i in range(N):                  
        if A[r_start+i][c_start] != ch:   
            return False                
    return True        

def inarow_Nsoutheast( ch, r_start, c_start, A, N ):
    """start from r_start and c_start and check for 
       N-in-a-row southeastward of element ch, returning 
       True or False, as appropriate
    """
    NR = len(A)   
    NC = len(A[0])
    if r_start+N-1 >= NR or c_start+N-1 >= NC:   
        return False   
    for i in range(N):                  
        if A[r_start+i][c_start+i] != ch:   
            return False                
    return True   

def inarow_Nnortheast( ch, r_start, c_start, A ,N):
    """start from r_start and c_start and check for 
       N-in-a-row northeastward of element ch, returning 
       True or False, as appropriate
    """
    NR = len(A)   
    NC = len(A[0])
    if r_start >= NR or c_start+N -1 >= NC:   
        return False   
    for i in range(N):                  
        if A[r_start-i][c_start+i] != ch:   
            return False                
    return True  






class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width 
        and height.
        """
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # the string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # bottom of the board

        # and the numbers underneath here

        return s       # the board is complete, return it

    def addMove(self,col,ox):
        """This method takes two arguments: the first, col, 
        represents the index of the column to which the checker will be 
        added. The second argument, ox, will be a 1-character string 
        representing the checker to add to the board. That is, ox should 
        either be 'X' or 'O' (again, capital O, not zero).
        """
        H = self.height
        for row in range(0, H):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return
        self.data[H-1][col] = ox


    def clear(self):
        """clears out the board"""
        self.data = [ [' ']*W for row in range(H) ]   

    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'

    def allowsMove(self,c):
        """this method should check to be sure that c is within the range 
        from 0 to the last column and make sure that there is still room 
        left in the column!
        """
        H = self.height
        W = self.width
        D = self.data

        if c not in range(self.width):
            return False
        else:
            for i in range(self.height):
                if self.data[i][c] == ' ':
                    return True
                else:
                    return False
        

    def isFull(self):
        """checks if board is full"""
        W = self.width
        D = self.data
        for a in range(W):
            if self.allowsMove(a) == True:
                return False
        return True    

    def delMove(self, c):
        """removes top checker from column c"""
        H = self.height
        for row in range(0, H):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return    

    def winsFor(self,ox):
        """checks if someone wins the game"""
        H = self.height
        W = self.width
        D = self.data

        for r_start in range(H):
            for c_start in range(W):
                if inarow_Neast( ox, r_start, c_start, D, 4 ) == True:
                    return True 
                elif inarow_Nsouth( ox, r_start, c_start, D, 4 ) == True:
                    return True 
                elif inarow_Nnortheast( ox, r_start, c_start, D, 4 ) == True:
                    return True 
                elif inarow_Nsoutheast( ox, r_start, c_start, D, 4 )== True:
                    return True
        return False

    def colsToWin(self, ox):
        """the colsToWin method should return the list of columns 
        where ox can move in the next turn in order to win and finish 
        the game. arguments:ox, which will be either the string 'X' or 
        the string 'O'
        return value: list 
        """
        x = []
        for col in range(self.width):
            if self.allowsMove(col) == True:
                self.addMove(col, ox)
                if self.winsFor(ox) == True:
                    x+= [col]
                self.delMove(col)
        return x

    def aiMove(self, ox):
        """ accepts a single argument, ox, which will be either 
        the string 'X' or the string 'O'. aiMove returns a single integer, 
        which must be a legal column in which to make a move. 
        """
        if ox == 'O':
            opponent = 'X'
        else:
            opponent = 'Y'

        x = self.colsToWin(ox)
        y = self.colsToWin(opponent)
        options = list(range(self.width))  

        if x == []:  #this means you can't win 
            if y != []: #but opponent can win
                return (y[0])  #block opponent's winning move 
            else:
                while True:
                    choice = random.choice(options)
                    if self.allowsMove(choice) == True:
                        return (choice)     # plays random move if no one can win in this turn 
        else:
            return (x[0])                    

    def hostGame(self):
        """host connect4
        """
        print()
        print("Welcome to this game of Connect 4!")
        print (self)
        print()
        print("Choose your fighter!")
        ox = input("X,O, or Neither")

        while True:
            if ox == "Neither": #AI plays against itself
                users_col =self.aiMove('X')
            elif ox == "O": # user chooses to play O
                users_col = self.aiMove('X')
            else:
                users_col = int(input("X. Choose a column:"))
                while self.allowsMove(users_col) == False:
                    users_col = int(input("O. Choose a column"))      
            self.addMove(users_col, "X")    
          
            print(self)
            if self.winsFor("X") == True:
                print("Nicely done! You won")
                break
            if self.isFull() == True:
                print("Board is full! Better luck next time")
                break

            if ox =='X' or ox == 'Neither':
                users_col = self.aiMove('O')
            else:
                users_col = int(input("O. Choose a column:"))   
                while self.allowsMove(users_col) == False:
                    users_col = int(input("X. Choose a column")) 
            self.addMove(users_col,"O")
            print(self)
            if self.winsFor("O") == True:
                print("Nicely done! You won")
                break
            if self.isFull() == True:
                print("Board is full! Better luck next time")
                break    




    def playGame(self, px, po):
        """ calls nextMove for two objects (px and po) of type Player in order to
            play a game 
        """
        nextCheckerToMove = 'X'


        while True:
            if nextCheckerToMove == 'X':
                plr = px
            else:
                plr = po
                
            #print C4 board
            print (self)
            if plr != 'human':
                col = -1
                while not self.allowsMove( col ):
                    col = plr.nextMove(self)
                self.addMove( col, nextCheckerToMove )
            else:
                col = -1
                while not self.allowsMove( col ):
                    col = input('Next col for ' + nextCheckerToMove + ': ')
                self.addMove( col, nextCheckerToMove )
            
            #check if the game is over
            if self.winsFor( nextCheckerToMove ):
                print (self)
                print ('\n' + nextCheckerToMove + ' wins! Good job!\n\n')
                break
            if self.isFull():
                print (self)
                print ('\nThe game is a tie. What a bummer! \n\n')
                break

            #connect 4 variation: pieces swapped with opponent's pieces
            if random.choice(range(15)) == 0:
                print ('Oops! The board has magically swapped all of your pieces with your opponents. Player X, continue playing the X pieces. Player O, continue playing the O pieces. Can you beat your own strategy?')
                print ('Good luck!')
                for row in range(0, self.height):
                    for col in range(0, self.width):
                        if self.data[row][col] == 'X':
                            self.data[row][col] = 'O'
                        elif self.data[row][col] == 'O':
                            self.data[row][col] = 'X'      



            # switch players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
            else:
                nextCheckerToMove = 'X'

        print ('Byyyyyyeeeee')







class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Construct a player for a given checker, tie-breaking type,
           and ply.
        """
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Create a string represenation of the player.
        """
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s


    def oppCh(self): 
        """ return the other kind of checker or playing piece, i.e., 
        the piece being played by self's opponent.
        """
        if self.ox == 'X':
            return 'O'
        else: 
            return 'X'

    def scoreBoard(self, b):
        """returns a single float value representing the score of 
        the input b, which you may assume will be an object of type Board. 
        This should return 100.0 if the board b is a win for self. It should 
        return 50.0 if it is neither a win nor a loss for self, and it should 
        return 0.0 if it is a loss for self (i.e., the opponent has won)"""
        if b.winsFor(self.ox):
            return 100
        elif b.winsFor(self.oppCh()):  
            return 0
        else:
            return 50    

    def tiebreakMove(self, scores):
        """This method takes in scores, which will be a nonempty list of 
        floating-point numbers, and returns its column number. If there is 
        more than one highest score because of a tie, this method should return 
        the COLUMN number of the highest score appropriate to the player's 
        tiebreaking type."""
        maxIndices = []
        maxscores = max(scores)
        for x in range(len(scores)):
            if maxscores == scores[x]:
                maxIndices += [x]
        if len(maxIndices) == 1:
            return maxIndices[0] 
        else:          
            if self.tbt == 'RIGHT':
                return maxIndices[len(maxIndices)-1]
            elif self.tbt == 'LEFT':
                return maxIndices[0]
            elif self.tbt == 'RANDOM':
                c = random.choice(range(len(maxIndices)))
                return maxIndices[c]   

    def scoresFor(self,b):
        """returns a list of scores, with the cth score representing 
        the "goodness" of the input board after the player moves to column c. 
        And, "goodness" is measured by what happens in the game after self.ply 
        moves """
        scores= [50,50,50,50,50,50,50]
        for col in range(7):
            if b.allowsMove(col) == False:
                scores[col] = -1
            elif b.winsFor(self.ox) == True:
                scores[col] = 100
            elif b.winsFor(self.oppCh()) == True:
                scores[col] = 0
            elif self.ply == 0:
                scores [col] = 50
            else:
                b.addMove(col,self.ox)
                if b.winsFor(self.ox) == True:
                    scores[col]=100
                else:
                    op = Player(self.oppCh(), self.tbt, self.ply-1)
                    opsc = op.scoresFor(b)
                    opscmax = max(opsc)
                    scores[col] = (100 - opscmax)
                b.delMove(col)
                
        return scores     

    def nextMove(self, b):
        """ accepts b and returns an integer which represents the column number 
            that the calling object (player) chooses to move to."""
        return self.tiebreakMove(self.scoresFor(b))