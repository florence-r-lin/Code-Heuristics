# Connect Four 2.0!
# A.I. Connect Four 
# Will be able to:
#Look ahead one move for either checker 'X' or 'O'
#Choose a move that can win the game (if a win is available!)
#Choose a move that can block an opponent's win (in the upcoming turn—if it's possible to do so)
#Defeat its creator at Connect Four (well, possibly...)

#given functions (also functions written in hw9pr2)

import random

def inarow_Neast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading east and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True


def sneakyRecur(self, x):
    if x==0:
        return x
    else:
        return self.sneakyRecur(x-1)

def inarow_Nsouth(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading south and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start + (N-1) > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start+i][c_start] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True

def inarow_Nnortheast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading northeast and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start - (N-1) < 0 or r_start > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start-i][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True

def inarow_Nsoutheast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading southeast and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start + (N-1) > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start+i][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True






class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)] #data is not a variable as we do not need to input it. 

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

        s += '\n'
        
        for col in range(0, self.width):
            s += " " + str(col)

        return s      # the board is complete, return it


    def addMove(self, col, ox):
        """ addMove takes two arguments
            col = index of the column to which the checker
            will be added
            ox = 1-character string representing the checker 
            to add to the board 'X' or 'O'
            addMove checks the row below to see if it is filled.
            If it is, then addMove adds something above it. We keep 
            the return inside the for loop to stop the loop once 
            it fills the row above so it doesn't keep replacing the 
            entire column with the once checker.
        """
        H = self.height
        for row in range(0,H):
            if  self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return #inside the for loop

        self.data[H-1][col] = ox #sets the bottom most row as a checker in case the entire column is empty. 



    def clear(self):
        """ clears the board of X's and O's"""
        W = self.width
        H = self.height

        for row in range(0, H):
            for col in range(0, W):
                self.data[row][col] = ' '
        


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



    def allowsMove(self, c):
        """ check if a column is a legal move
            returns True if the calling object (of type Board) 
            does allow a move into column c. It returns False if 
            column c is not a legal column number for the calling 
            object. It also returns False if column c is full.
        """
        
        H = self.height
        W = self.width
        D = self.data

        if c >= W or c < 0:
            return False
        elif D[0][c] != ' ' : #top row's index is 0
            return False
        else:
            return True

    def isFull(self):
        """ returns True is the calling object of type Board is 
            full of checkers. It should return False otherwise. 
        """
        H = self.height
        W = self.width

        for row in range(0, H):
            for col in range(0, W): 
                if self.data[row][col] == ' ':
                    return False

                
        return True

    def delMove(self, c):
        """ removes the top checker from column c.
            If the column is empty, then delMove does nothing
        """

        H = self.height

        for row in range (0,H):
            if  self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return #inside the for loop


    def winsFor(self, ox):
        """ winsFor code argument OX is a 1-character checker:
            either 'X' or 'O'. It should return True 
            if there are four checkers of type ox in a 
            row on the board. It should return False 
            othwerwise.
        """
            
        # this is pseudocode
        H = self.height
        W = self.width

        for row in range (0,H):
            for col in range (0, W):
                if inarow_Neast (ox, row, col, self.data, 4) == True \
                    or inarow_Nsouth(ox, row, col, self.data, 4) == True \
                        or inarow_Nnortheast(ox, row, col, self.data, 4) == True \
                            or inarow_Nsoutheast(ox, row, col, self.data, 4) == True:
                            return True
        return False


    def colsToWin(self, ox):
        """returns a list of columns at which ox would win on the next move
            takes one argument "X" or "O"
            place a checker in each column and each time see if the game is a win.
        """
        L = []
        
        for c in range (self.width):
            if self.allowsMove(c) == True: 
                self.addMove(c, ox)
                if self.winsFor(ox) == True:
                    L = L + [c]
                self.delMove(c)

        return L


    def aiMove(self, ox):
        """ accepts a single argument which will be either X or O
            returns a single integer which is a legal column.
            if there is a way for X or O to win then aiMove returns
            that move.
        """
        if ox == 'O':
            xo = 'X'
        else:
            if ox == 'X':
                xo = 'O'

        B = []
        L = self.colsToWin(ox)
        L2 = self.colsToWin(xo)

        #if you can win, you need to win in the next move
        if L != []:
            return random.choice(L)

        #if you cannot win...
        elif L2 !=[]:
            return random.choice(L2)

        else:
            
            for c in range (self.width):
                if self.allowsMove(c) == True:
                    B = B + [c]
            return random.choice(B)


    
    def hostGame(self):
        """ host a game of connect four! 
            alternates between X and O where X moves first
            asks user for column number for each move
        """

        print()
        print ("Let's play Connect Four!")
        print()
        print (self) #prints the board

        users_checker = str(input('Player 1, choose a checker (X or O) or choose "both" for the AI to play against itself: '))
        if users_checker == 'X':
            while True:  #one X turn and one O turn in the while loop
                users_col = -1 #prompts the user to input a valid column number
                while self.allowsMove(users_col) == False: #same as saying while not self.allowsMove(users_col):
                    users_col = int(input("Player 1, choose a column: "))

                self.addMove(users_col, users_checker) 
                print (self)
                if self.winsFor("X"):
                    return "First Player wins! X wins! Congratulations!"

                # AIs turn
                AI_col = self.aiMove('O')
                self.addMove(AI_col, 'O') 

                print (self)
                if self.winsFor("O"):
                    return "Second Player wins! O wins! Sorry Player 1 lost!"

                if self.isFull() == True:
                    return "GameOver!"
        
    
        elif users_checker == 'O':
            print('Since X always goes first, AI will go first!')
            AI_col = self.aiMove('X')
            self.addMove(AI_col, 'X') 

            print (self)
            if self.winsFor("X"):
                return "Second Player wins! X wins! Congratulations!"

            if self.isFull() == True:
                return "GameOver!"
        
            while True:  #one X turn and one O turn in the while loop
                users_col = -1 #prompts the user to input a valid column number
                while self.allowsMove(users_col) == False: #same as saying while not self.allowsMove(users_col):
                    users_col = int(input("Player 1, choose a column: "))

                self.addMove(users_col, users_checker) 
                print (self)
                if self.winsFor("X"):
                    return "First Player wins! X wins! Congratulations!"

        else: #user picks computer to play both X and O; users_checker == 'both'
            
            while True:
                AI_col = self.aiMove('X')
                self.addMove(AI_col, 'X') 
                print (self)
                if self.winsFor("X"):
                    return "Second Player wins! X wins! Congratulations!"

                if self.isFull() == True:
                    return "GameOver!"

                AI_col = self.aiMove('O')
                self.addMove(AI_col, 'O') 

                print (self)
                if self.winsFor("O"):
                    return "Second Player wins! O wins! Congratulations!"

                if self.isFull() == True:
                    return "GameOver!"


    def playGame(self, px, po, ss = False):
        """Plays a game of Connect Four.
            p1 and p2 are objects of type Player OR
            the string 'human'.
            If ss is True, it will "show scores" each time.

            define both players and board each time
            E.g.
            px = 'human'  #Player('X', 'LEFT', 1)     
            po = 'human' #Player('O', 'LEFT', 1)   
            b = Board(7,6)  
        """

        nextCheckerToMove = 'X'
        nextPlayerToMove = px

        while True:

            # print the current board
            print(self)

            # choose the next move
            if nextPlayerToMove == 'human':
                col = -1
                while not self.allowsMove(col):
                    col = int(input('Next col for ' + nextCheckerToMove + ': '))

                    if not self.allowsMove(col):
                        print('column full, please choose another column!')

            else: # it's a computer player
                if ss:
                    scores = nextPlayerToMove.scoresFor(self)
                    print((nextCheckerToMove + "'s"), 'Scores: ', [int(sc) for sc in scores])
                    print()
                    col = nextPlayerToMove.tiebreakMove(scores)
                else:
                    col = nextPlayerToMove.nextMove(self)

            # add the checker to the board
            self.addMove(col, nextCheckerToMove)

            # check if game is over
            if self.winsFor(nextCheckerToMove):
                print(self)
                print('\n' + nextCheckerToMove + ' wins! Congratulations!\n\n')
                break
            if self.isFull():
                print(self)
                print('\nThe game is a draw.\n\n')
                break

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
                nextPlayerToMove = po
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = px

        print('Come back 4 more!')
            

    #new variation of connectfour (swaps third row with fifth row when third row has been filled!)

    def playCrazyGame(self, px, po, ss = False):
        """Plays a game of Connect Four.
            p1 and p2 are objects of type Player OR
            the string 'human'.
            If ss is True, it will "show scores" each time.

            define both players and board each time
            E.g.
            px = 'human'  #Player('X', 'LEFT', 1)     
            po = 'human' #Player('O', 'LEFT', 1)   
            b = Board(7,6)  
        """

        nextCheckerToMove = 'X'
        nextPlayerToMove = px

        while True:

            # print the current board
            print(self)

            # choose the next move
            if nextPlayerToMove == 'human':
                col = -1
                while not self.allowsMove(col):
                    col = int(input('Next col for ' + nextCheckerToMove + ': '))

                    if not self.allowsMove(col): #if column is full it will prompt you to choose another column
                        print('column full, please choose another column!')

                
            else: # it's a computer player
                if ss:
                    scores = nextPlayerToMove.scoresFor(self)
                    print((nextCheckerToMove + "'s"), 'Scores: ', [int(sc) for sc in scores])
                    print()
                    col = nextPlayerToMove.tiebreakMove(scores)
                else:
                    col = nextPlayerToMove.nextMove(self)

            # add the checker to the board
            self.addMove(col, nextCheckerToMove)

            #variation = ROW SWAP! swaps row 3 for row 5
            if self.checkifrowFull(3) == True:
                print("WARNING!!!!!! Board row swapped")
                for c in range(7):
                    bot = self.data[5][c]
                    up = self.data[3][c]
                    self.data[5][c] = up
                    self.data[3][c] = bot
                    

            # check if game is over
            if self.winsFor(nextCheckerToMove):
                print(self)
                print('\n' + nextCheckerToMove + ' wins! Congratulations!\n\n')
                break
            if self.isFull():
                print(self)
                print('\nThe game is a draw.\n\n')
                break

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
                nextPlayerToMove = po
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = px
                
        #if row three is all full, ret
        #if checkifrowFull == True:

        print('Come back for more! <3 Let us play again!')


    def checkifrowFull(self, r):
        """ Checks if a row is full of checkers or not
            returns true or false """

        H = self.height
        W = self.width

        for col in range (0,W):
                if self.data[r][col] == ' ':
                    return False
                
        return True #needs to be after the for loop ends and it goes throguh each col.




                

# Player Class Final Proejct

class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Construct a player for a given checker, tie-breaking type,
           and ply.
           ply is the amount of moves the player can look ahead"""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Create a string represenation of the player."""
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self):
        """ returns the opposite checker of self.ox (a player)"""
        
        if self.ox == 'O':
            return 'X'
            
        else: #if self.ox == 'X':
            return 'O'

    
    def scoreBoard(self, b):
        """ returns a single float value representing the 
            input b (an object of type board). If the board b
            is a win for self, return 100
            if board b is neither win or loss, return 50
            if boars b is a loss, return 0
        """
        if b.winsFor(self.ox) == True:
            return 100.0
        elif b.winsFor(self.oppCh()) == True:
            return 0.0
        else:
            return 50.0

    def tiebreakMove(self, scores):
        """ takes scores which will be a nonempty
        list of floating-point numbers 
        returns a column number based on method chosen by player"""
        
        MS = max(scores) #100, 100, ..
        maxIndices = []
        

        for i in range(len(scores)):
            if MS == scores[i]: #square bracket to collect the index number of each list of index 0 - i
                maxIndices = maxIndices + [i] #maxIndices is the list of indexs/position of the max numbers

        #if len(maxIndices) == 1:
            #return maxIndices[0] #return the index number maxIndices is holding if maxIndices has only one number

        if self.tbt == 'LEFT':
             return maxIndices[0]
        elif self.tbt == 'RIGHT':
            return maxIndices[-1]
        else:
            return random.choice(maxIndices)

    def scoresFor(self, b):
        """ returns a list of scores with the xth score
            representing the "goodness" of the input board after 
            the player moved to column c. Goodness is measured 
            by what happens in the game after self.ply moves.
            
            scoresFor looks at all columns and returns the score that we
            will get by moving our checker into each of the columns

            returns a list of 7 numbers which will be either 100, 50, 0 or -1. 

            The way the function works.. is that for a board b

            | | | | | | | |
            | | | | | | | |
            | | | | |X| | |
            | |O| | |O| | |
            | |X|X| |X| | |
            | |X|O| |O|O| |
            ---------------
             0 1 2 3 4 5 6

            ScoresFor - if our opponent is O - will return [50,50,50,100,50,50,50]
            this is because, with the loop and recurssion, what happens is tha that
            col 3 for the opponent will score 100 until b.addmove(3) occurs. That is
            when the opponent's score will be 50 and so it will be the largest amount 
            when 100-opponent's score is taken. Thus it will be targetted as the best
            place for me to add my checker.
            
            """

        
        scores = [50]*b.width #list "scores" = length of 50 * the width of the board

        for col in range (b.width):
            if b.allowsMove(col) == False:
                scores[col] = -1
            elif b.winsFor(self.ox) == True:
                scores[col] = 100
            elif b.winsFor(self.oppCh()) == True:
                scores[col] = 0
            elif self.ply == 0:
                scores[col] = 50
            else:
                b.addMove(col, self.ox)
                op = Player(self.oppCh(), self.tbt, self.ply -1)
                opscores = op.scoresFor(b) # the seven scores th eopponent thinks it gets
                M = max(opscores)
                My = 100 - M #myscore
                scores[col] = My 
                b.delMove(col)

        return scores #list of scores


    def nextMove(self,b):
        """ This method accepts b, an object of type Board, 
        and returns an integer—namely, the column number that 
        the calling object (of class Player) chooses to move to.
        """
        return self.tiebreakMove(self.scoresFor(b))



b = Board(7,6)

"""
for r in range(1,4):
    for c in range(7):
        b.data[r][c] = 'X'
for r in range(4,6):
    for c in range(7):
        b.data[r][c] = 'O'

print(b)
"""

"""
px = Player('X', 'LEFT', 3)
po = Player('O', 'LEFT', 2)
"""

"""
for c in range(7):
    bot = b.data[5][c]
    up = b.data[3][c]
    b.data[5][c] = up
    b.data[3][c] = bot
print(b)

#variation = top row dissapears when full
            if self.checkifrowFull(0) == True:
                print("WARNING!!!!!! Board row dissapeared!")
                
                for c in range(self.width):
                    if self.data[0][c] != ' ':
                        self.data[0][c] = ' '
                    return
                    
                print(self)

"""