#Ellie Brennock
#12/13/19

"""
current issue is with the getCurrentSurroundings(self) function
is saying the index is out of range, but the program should never be on
the edge of the world so there should always be room to check to all sides
"""

import random

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5
POSSIBLE_MOVES = ['N', 'E', 'W', 'S']

class Program(object):
    def __init__(self):
        """
        sets up dictionary of picobot rules
        """
        self.rules = {}


    def __repr__(self):
        """
        sets up for printing
        """
        unsortedKeys = list(self.rules.keys())
        sortedKeys = sorted(unsortedKeys)
        p = ''
        for i in range(len(sortedKeys)):
            p += str(sortedKeys[i][0]) + " " 
            p += sortedKeys[i][1] + " -> " 
            p += self.rules[sortedKeys[i]][0] + " "
            p += str(self.rules[sortedKeys[i]][1]) + '\n'
        return p

    def randomize(self):
        """
        completes a set of 45 randomized rules
        """
        surroundings = ['xxxx', 'Nxxx', 'NExx', 'NxWx', 'xxxS', 'xExS', 'xxWS', 'xExx', 'xxWx']
        state = 0
        movedir = ''
        for i in range(0, 5):
            for j in surroundings:
                state = random.choice(range(0, 5))
                movedir = random.choice(POSSIBLE_MOVES)
                while movedir in j:
                    movedir = random.choice(POSSIBLE_MOVES)
                self.rules[(i, j)] = (movedir, state)
    
    def getMove(self, state, surroundings):
        """
        returns the move for the current situation based 
        on state and surroundings
        """
        return self.rules[(state, surroundings)]


    def mutate(self):
        """
        chooses a rule from self.rules and changes the 
        value for that rule to a new random choice
        """
        key = random.choice(list(self.rules.keys()))
        state = random.choice(range(0, 5))
        while state != self.rules[key][1]:
            state = random.choice(range(0, 5))
        movedir = random.choice(POSSIBLE_MOVES)
        while movedir != self.rules[key][0]:
            movedir = random.choice(POSSIBLE_MOVES)
        self.rules[key] = (movedir, state)


    def crossover(self, other):
        """
        returns an offspring program with some rules
        from each parent (self and other)
        """
        program = Program()
        crossState = random.choice(range(0, 4))
        for i in self.rules:
            if i[0] <= crossState:
                program.rules[i] = self.rules[i]
        for j in other.rules:
            if j[0] > crossState:
                program.rules[j] =  other.rules[j]
        return program

    def __gt__(self, other):
        """Greater-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])

class World(object):

    def __init__(self, initial_row, initial_col, program):
        self.row = initial_row
        self.col = initial_col
        self.state = 0
        self.prog = program
        self.room = [[' ']*WIDTH for row in range(HEIGHT)]
        #places in walls on all 4 sides
        for c in range(WIDTH):
            self.room[0][c] = '+'
            self.room[HEIGHT - 1][c] = '+'
        for r in range(0, HEIGHT):
            self.room[r][0] = '+'
            self.room[r][WIDTH - 1] = '+'
        #places picobot in inital location
        self.room[self.row][self.col] = 'P'
        

    def __repr__(self):
        r = ''
        for row in range(HEIGHT):
            for col in range(WIDTH):
                r += self.room[row][col]
                r += ' '
            r += '\n'
        return r


    def getCurrentSurroundings(self):
        """
        returns the current surroundings of the program
        """
        surroundings = ''
        #checks north
        if self.room[self.row - 1][self.col] == '+':
            surroundings += 'N'
        else:
            surroundings += 'x'
        #checks east
        if self.room[self.row][self.col + 1] == '+':
            surroundings += 'E'
        else:
            surroundings += 'x'
        #checks west
        if self.room[self.row][self.col - 1] == '+':
            surroundings += 'W'
        else:
            surroundings += 'x'
        #checks south
        if self.room[self.row + 1][self.col] == '+':
            surroundings += 'S'
        else:
            surroundings += 'x'
        return surroundings
        
    def step(self):
        """
        moves a step according to getMove and updates world
        """
        (move, st) = self.prog.getMove(self.state, self.getCurrentSurroundings())
        self.room[self.row][self.col] = 'o'
        if move == 'N':
            self.row -= 1
        elif move == 'E':
            self.col += 1
        elif move == 'W':
            self.col -= 1
        else:
            self.row += 1
        self.state = st
        self.room[self.row][self.col] = 'P'

    def run(self, steps):
        """
        runs step steps number of times
        """
        for i in range(steps):
            self.step()

    def fractionVisitedCells(self):
        """
        calculates fraction of cells visited by the program
        """
        count = 1
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.room[row][col] == 'o':
                    count += 1
        return count / 529

def popList(size):
    """
    creates a list of size size of randomized programs
    """
    L = []
    for i in range(size):
        prog = Program()
        prog.randomize()
        L.append(prog)
    return L

def evaluateFitness(program, trials, steps):
    """
    runs the program a number of steps over a number of trials
    and averages the percentage of squares visited
    """
    fit = 0
    for i in range(trials):
        world = World(random.choice(range(1, 24)), random.choice(range(1, 24)), program)
        world.run(steps)
        fit += world.fractionVisitedCells()
    return fit / trials

def GA(popsize, numgens):
    """
    currently just creates a list of programs and how well they work
    """
    popLists = popList(popsize)
    L = [[0]*2]*popsize
    for i in range(popsize):
        L[i][0] = evaluateFitness(popLists[i], 42, 1000)
        L[i][1] = popLists[i]
    for j in range(numgens):
        Sl = sorted(L)
        length = int(len(Sl) * 0.1)
        Sl = Sl[len(Sl) - length:  -1]
        for i in range(popsize - len(Sl)):
            parent1 = random.choice(Sl)[1]
            parent2 = random.choice(Sl)[1]
            newProg = parent1.crossover(parent2)
            if random.choice([1,2, 3]) == 1:
                newProg.mutate()
            Sl.append([evaluateFitness(newProg, 42, 1000), newProg])
        L = Sl
        print("Generation " + str(j))
        ave = 0
        for k in L:
            ave += k[0]
        ave = ave / len(L)
        print('Average fitness: ' + str(ave))
        max = L[0][0]
        print('Best fitness: ' + str(max))
    print('Best Picobot program:')
    print(L[0][1])
    return L[0][1]

"""
Best fitness: 0.06593752813034474
Best Picobot program:
0 NExx -> W 4
0 NxWx -> E 3
0 Nxxx -> S 2
0 xExS -> W 3
0 xExx -> N 0
0 xxWS -> E 0
0 xxWx -> E 2
0 xxxS -> E 1
0 xxxx -> S 1
1 NExx -> S 4
1 NxWx -> E 3
1 Nxxx -> S 2
1 xExS -> W 3
1 xExx -> S 0
1 xxWS -> N 0
1 xxWx -> N 4
1 xxxS -> N 3
1 xxxx -> N 4
2 NExx -> S 4
2 NxWx -> E 0
2 Nxxx -> S 0
2 xExS -> W 0
2 xExx -> S 4
2 xxWS -> E 3
2 xxWx -> N 4
2 xxxS -> E 1
2 xxxx -> W 3
3 NExx -> S 2
3 NxWx -> E 3
3 Nxxx -> S 0
3 xExS -> N 1
3 xExx -> N 1
3 xxWS -> E 4
3 xxWx -> E 0
3 xxxS -> N 1
3 xxxx -> N 2
4 NExx -> W 4
4 NxWx -> E 3
4 Nxxx -> S 0
4 xExS -> N 1
4 xExx -> W 4
4 xxWS -> E 1
4 xxWx -> N 4
4 xxxS -> N 3
4 xxxx -> W 3
"""