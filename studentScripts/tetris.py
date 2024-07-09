# tetris.py

# wow! it's the final project!


class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
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
        s += '\n'
        for i in range(0, col+1):
            s += ' ' + str((i)%10)


        return s       # the board is complete, return it
    
    def addMove(self, col, ox):
        """ addMove takes arguments col (index of column) and ox (1-character
            string X or O).
        """
        H = self.height
        for row in range(0, H):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return
        
        self.data[H-1][col] = ox

    def clear(self):
        """ clear should clear the board """
        for r in range(0, self.height):
            for c in range(0, self.width):
                if self.data[r][c] != ' ':
                    self.data[r][c] = ' '
        
        return self

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
        """ Returns True if the calling object allows a move into column c. 
            Returns False if column c is not a legal column number.
            Returns false if column c is full.
        """
        
        if c in range(0, self.width):
            if self.data[0][c] != ' ':
                return False          
            elif self.data[0][c] == ' ':
                return True
        else:
            return False
    
    def isFull(self):
        """ returns True if calling object is full.
            returns False otherwise.
        """

        for col in range(0, self.width):
            for row in range(0, self.height):
                if self.data[row][col] == ' ':
                    return False
                
        return True

    def delMove(self, c):
        """ Removes top checker from column c. If column empty, it does nothing. """

        H = self.height
        for row in range(0, H):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return
        
        self.data[H-1][c] = ' '
    

    def winsFor(self, ox):
        """ takes 'X' or 'O' as an argument. 
            returns True if there are four checkers of type ox in a row on the board.
            returns False otherwise.
        """
        H = self.height
        W = self.width
        D = self.data
        # Check for horizontal wins
        for row in range(0, H):
            for col in range(0, W - 3):
                if D[row][col] == ox and \
                   D[row][col + 1] == ox and \
                   D[row][col + 2] == ox and \
                   D[row][col + 3] == ox:
                    return True
        #vertical wins
        for col in range(0, W):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col] == ox and \
                   D[row+2][col] == ox and \
                   D[row+3][col] == ox:
                    return True
        #diagonal wins (1)
        for col in range(0, W-3):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col+1] == ox and \
                   D[row+2][col+2] == ox and \
                   D[row+3][col+3] == ox:
                    return True
        #diagonal wins (2)
        for col in range(3, W):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col-1] == ox and \
                   D[row+2][col-2] == ox and \
                   D[row+3][col-3] == ox:
                    return True
        else: 
            return False

    def colsToWin(self, ox):
        """ intakes an argument 'O' or 'X' and returns the list of columns where ox
            can move in the next turn to win the game... """
        
        W = self.width
        D = self.data
        L = []

        for col in range(0, W):
            if self.allowsMove(col) == True:
                self.addMove(col, ox)
                if self.winsFor(ox) == True:
                    L += [col]
                self.delMove(col)
        return L
                
    def aiMove(self, ox):
        """ accepts 'O' or 'X' and returns an integer, which is a column
            in which to make a move. """
        
        W = self.width
        L = self.colsToWin(ox)

        if L != []:
            return int(L[0])
        else: 
            if ox == 'O':
                oppx = 'X'
                M = self.colsToWin(oppx)
                if M != []:
                   return int(M[0])
                else:
                    if self.allowsMove(0) == True:
                        return 0
                    elif self.allowsMove(W/2) == True:
                        return int(W/2)
                    else:
                        return int(W)
                    
            else:
                oppo = 'O'
                N = self.colsToWin(oppo)
                if N != []:
                   return int(N[0])
                else:
                    if self.allowsMove(0) == True:
                        return 0
                    elif self.allowsMove(W/2) == True:
                        return int(W/2)
                    else:
                        return int(W)
            #check if blocking is possible

    def checkRow(self):
        """ checkRow checks if row r is full; returns True if full.
        """
        W = self.width
        H = self.height
        
        for c in range(0, W):
            if self.data[H-1][c] == ' ':
                return False
        return True


    def delRow(self, r):
        """ delRow deletes row r and then makes everything fall.
        """

        W = self.width
        H = self.height

        for r in range(r-1, -1, -1):
            for c in range(0, W):
                self.data[r+1][c] = self.data[r][c]
        for c in range(0, W):
            self.data[0][c] = ' '       
        
      




    def hostGame(self):
        """ hosts a game of Connect Four """

        print()
        print('hi. let us play Connect Four.')
        print()
        print(self)
        print()

        while True:
            print()
            users_col = int(input("X's choice: "))
            print()  
            while self.allowsMove(users_col) == False:
                users_col = int(input("Choose a column: "))
        
            self.addMove(users_col, 'X')
            print(self)

            if self.winsFor('X') == True:
                print('X wins!')
                print(self)
                break
            elif self.isFull() == True:
                print('tie!')
                print(self)
                break


            print()
            o_col = int(aiMove('O'))
            print()
        
            self.addMove(o_col, 'O')
            print(self)
        
            if self.winsFor('O') == True:
                print('O wins!')
                print(self)
                break
            elif self.isFull() == True:
                print('tie!')
                print(self)
                break

    def playGame(self, px, po):
        """Plays a game of Connect Four.
            p1 and p2 are objects of type Player OR
            the string 'human'.
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
            else: # it's a computer player
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
            
            #check if bottom row is full
            if self.checkRow() == True:
                self.delRow(5)
                print('Tetris :))')
                print(self)

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
                nextPlayerToMove = po
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = px

        print('Thanks for playing!')



class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Constructs a player for a given checker, tie-breaking type,
           and ply."""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Creates a string represenation of the player."""
    
        s = "\n" "Player for " + self.ox + "\n"
        s += "  tiebreak type: " + self.tbt + "\n"
        s += "  ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self):
        """Returns the other playing piece."""

        if self.ox == 'O':    
            s = 'X'
            return s
        elif self.ox == 'X':    
            s = 'O'
            return s

    def scoreBoard(self, b):
        """ Returns single float value representing score of input b
            (of type board). 
                Returns 100.0 if b is a win for self
                Returns 50.0 if b is a tie for self
                Returns 0.0 if b is a loss for self
        """
        a = self.ox
        d = self.oppCh()

        if b.winsFor(d) == True:
            return 0.0
        elif b.winsFor(a) == True:
            return 100.0
        else:
            return 50.0
    
    def tiebreakMove(self, scores): # ????
        """ Takes in scores, a nonempty list of floating-point numbers.
            
            If there's only one highest score in the list, returns COLUMN NUMBER.
            If there's more than one highest score, returns COLUMN NUMBER 
            based on tiebreak type.
        """

        m = max(scores) # max of the scores
        maxInd = []
        
        for n in range(0, len(scores)):
            if scores[n] == m:
                maxInd += [n]
        
        # wow I can't believe i voluntarily wrote a for loop 
        # what have I become

        if self.tbt == 'LEFT':
            mcol = maxInd[0]
            return mcol 
        elif self.tbt == 'RIGHT':
            l = len(maxInd) - 1
            mcol = maxInd[l]
            return mcol

    def scoresFor(self, b):
        """ Returns list of scores with cth score representing how 'good' the 
            input board is after the player moves to column c, as measured by
            what follows once self.ply moves.
        """

        scores = [50]*b.width
        H = b.height
        W = b.width
        D = b.data

        a = self.ox
        d = self.oppCh()

        for c in range (0, W):
            if b.allowsMove(c) != True:
                scores[c] = -1.0
            elif b.winsFor(a) == True:
                scores[c] = 100.0
            elif b.winsFor(d) == True:
                scores[c] = 0.0
            elif self.ply == 0:
                scores[c] = 50.0
            else:
                b.addMove(c, a)
                op = Player(self.oppCh(), self.tbt, self.ply-1)
                m = max(op.scoresFor(b))
                s = 100 - m
                scores[c] = s
                b.delMove(c)
        return scores

    def nextMove(self, b):
        """ Accepts b (board) and returns integer (column number that the 
            calling object chooses to move to).
        """

        return self.tiebreakMove(self.scoresFor(b))
# final.py

# wow! it's the final project!


class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
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
        s += '\n'
        for i in range(0, col+1):
            s += ' ' + str((i)%10)


        return s       # the board is complete, return it
    
    def addMove(self, col, ox):
        """ addMove takes arguments col (index of column) and ox (1-character
            string X or O).
        """
        H = self.height
        for row in range(0, H):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return
        
        self.data[H-1][col] = ox

    def clear(self):
        """ clear should clear the board """
        for r in range(0, self.height):
            for c in range(0, self.width):
                if self.data[r][c] != ' ':
                    self.data[r][c] = ' '
        
        return self

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
        """ Returns True if the calling object allows a move into column c. 
            Returns False if column c is not a legal column number.
            Returns false if column c is full.
        """
        
        if c in range(0, self.width):
            if self.data[0][c] != ' ':
                return False          
            elif self.data[0][c] == ' ':
                return True
        else:
            return False
    
    def isFull(self):
        """ returns True if calling object is full.
            returns False otherwise.
        """

        for col in range(0, self.width):
            for row in range(0, self.height):
                if self.data[row][col] == ' ':
                    return False
                
        return True

    def delMove(self, c):
        """ Removes top checker from column c. If column empty, it does nothing. """

        H = self.height
        for row in range(0, H):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return
        
        self.data[H-1][c] = ' '
    

    def winsFor(self, ox):
        """ takes 'X' or 'O' as an argument. 
            returns True if there are four checkers of type ox in a row on the board.
            returns False otherwise.
        """
        H = self.height
        W = self.width
        D = self.data
        # Check for horizontal wins
        for row in range(0, H):
            for col in range(0, W - 3):
                if D[row][col] == ox and \
                   D[row][col + 1] == ox and \
                   D[row][col + 2] == ox and \
                   D[row][col + 3] == ox:
                    return True
        #vertical wins
        for col in range(0, W):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col] == ox and \
                   D[row+2][col] == ox and \
                   D[row+3][col] == ox:
                    return True
        #diagonal wins (1)
        for col in range(0, W-3):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col+1] == ox and \
                   D[row+2][col+2] == ox and \
                   D[row+3][col+3] == ox:
                    return True
        #diagonal wins (2)
        for col in range(3, W):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col-1] == ox and \
                   D[row+2][col-2] == ox and \
                   D[row+3][col-3] == ox:
                    return True
        else: 
            return False

    def colsToWin(self, ox):
        """ intakes an argument 'O' or 'X' and returns the list of columns where ox
            can move in the next turn to win the game... """
        
        W = self.width
        D = self.data
        L = []

        for col in range(0, W):
            if self.allowsMove(col) == True:
                self.addMove(col, ox)
                if self.winsFor(ox) == True:
                    L += [col]
                self.delMove(col)
        return L
                
    def aiMove(self, ox):
        """ accepts 'O' or 'X' and returns an integer, which is a column
            in which to make a move. """
        
        W = self.width
        L = self.colsToWin(ox)

        if L != []:
            return int(L[0])
        else: 
            if ox == 'O':
                oppx = 'X'
                M = self.colsToWin(oppx)
                if M != []:
                   return int(M[0])
                else:
                    if self.allowsMove(0) == True:
                        return 0
                    elif self.allowsMove(W/2) == True:
                        return int(W/2)
                    else:
                        return int(W)
                    
            else:
                oppo = 'O'
                N = self.colsToWin(oppo)
                if N != []:
                   return int(N[0])
                else:
                    if self.allowsMove(0) == True:
                        return 0
                    elif self.allowsMove(W/2) == True:
                        return int(W/2)
                    else:
                        return int(W)
            #check if blocking is possible
            
        
      




    def hostGame(self):
        """ hosts a game of Connect Four """

        print()
        print('hi. let us play Connect Four.')
        print()
        print(self)
        print()

        while True:
            print()
            users_col = int(input("X's choice: "))
            print()  
            while self.allowsMove(users_col) == False:
                users_col = int(input("Choose a column: "))
        
            self.addMove(users_col, 'X')
            print(self)

            if self.winsFor('X') == True:
                print('X wins!')
                print(self)
                break
            elif self.isFull() == True:
                print('tie!')
                print(self)
                break


            print()
            o_col = int(aiMove('O'))
            print()
        
            self.addMove(o_col, 'O')
            print(self)
        
            if self.winsFor('O') == True:
                print('O wins!')
                print(self)
                break
            elif self.isFull() == True:
                print('tie!')
                print(self)
                break

    def playGame(self, pForX, pForO):
        """Plays a game of Connect Four.
            p1 and p2 are objects of type Player OR
            the string 'human'.
        """

        nextCheckerToMove = 'X'
        nextPlayerToMove = pForX

        while True:

            # print the current board
            print(self)

            # choose the next move
            if nextPlayerToMove == 'human':
                col = -1
                while not self.allowsMove(col):
                    col = int(input('Next col for ' + nextCheckerToMove + ': '))
            else: # it's a computer player
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
                nextPlayerToMove = pForO
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = pForX

        print('Thanks for playing!')




class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Constructs a player for a given checker, tie-breaking type,
           and ply."""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Creates a string represenation of the player."""
    
        s = "\n" "Player for " + self.ox + "\n"
        s += "  tiebreak type: " + self.tbt + "\n"
        s += "  ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self):
        """Returns the other playing piece."""

        if self.ox == 'O':    
            s = 'X'
            return s
        elif self.ox == 'X':    
            s = 'O'
            return s

    def scoreBoard(self, b):
        """ Returns single float value representing score of input b
            (of type board). 
                Returns 100.0 if b is a win for self
                Returns 50.0 if b is a tie for self
                Returns 0.0 if b is a loss for self
        """
        a = self.ox
        d = self.oppCh()

        if b.winsFor(d) == True:
            return 0.0
        elif b.winsFor(a) == True:
            return 100.0
        else:
            return 50.0
    
    def tiebreakMove(self, scores): # ????
        """ Takes in scores, a nonempty list of floating-point numbers.
            
            If there's only one highest score in the list, returns COLUMN NUMBER.
            If there's more than one highest score, returns COLUMN NUMBER 
            based on tiebreak type.
        """

        m = max(scores) # max of the scores
        maxInd = []
        
        for n in range(0, len(scores)):
            if scores[n] == m:
                maxInd += [n]
        
        # wow I can't believe i voluntarily wrote a for loop 
        # what have I become

        if self.tbt == 'LEFT':
            mcol = maxInd[0]
            return mcol 
        elif self.tbt == 'RIGHT':
            l = len(maxInd) - 1
            mcol = maxInd[l]
            return mcol

    def scoresFor(self, b):
        """ Returns list of scores with cth score representing how 'good' the 
            input board is after the player moves to column c, as measured by
            what follows once self.ply moves.
        """

        scores = [50]*b.width
        H = b.height
        W = b.width
        D = b.data

        a = self.ox
        d = self.oppCh()

        for c in range (0, W):
            if b.allowsMove(c) != True:
                scores[c] = -1.0
            elif b.winsFor(a) == True:
                scores[c] = 100.0
            elif b.winsFor(d) == True:
                scores[c] = 0.0
            elif self.ply == 0:
                scores[c] = 50.0
            else:
                b.addMove(c, a)
                op = Player(self.oppCh(), self.tbt, self.ply-1)
                m = max(op.scoresFor(b))
                s = 100 - m
                scores[c] = s
                b.delMove(c)
        return scores

    def nextMove(self, b):
        """ Accepts b (board) and returns integer (column number that the 
            calling object chooses to move to).
        """

        return self.tiebreakMove(self.scoresFor(b))
