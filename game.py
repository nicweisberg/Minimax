# Nick Weisberg


class GameState(object):
    """ The GameState class stores the information about the state of the game.
    """
    
    blank = ' '
    jedi = 'J'
    sith = 'S'
    rebel = 'R'
    
    
    def __init__(self, n):
    
    
        # initializing the board with rebels accross bottoma dn sith in the top middle 
        self.size = n
        self.gameState = dict()
        for r in range(1,self.size+1):
             for c in range(1,self.size+1):
                self.gameState[r,c] = self.blank
                if r==self.size:
                    self.gameState[r,c] = self.rebel
        self.gameState[1, (self.size//2)+1] = self.sith

        # counters for the eval function
        self.numRebels = n
        self.numSith = 1
        self.numJedi = 0
        
        self.stringified = self.__str__()
        self.numTurns = 1
        
        # a boolean to store if it's Max's turn; True by default
        self.maxs_turn = True
        
        # if this state is a winning state, store that information
        self.cachedWin = False
        
        
        # if cachedWin is True, then cachedWinner is a boolean
        # True means Max won; False means Min won
        self.cachedWinner = None
        
    def __str__(self):
        """ Translate the board description into a string.  
            Might use later for transposition table
        """
        s = ""
        for r in range(1,self.size+1):
            for c in range(1,self.size+1):
                s += str(self.gameState[r,c])
        return s
        


    def myclone(self):
        """ Make and return an exact copy of the state.
        """
        new_state = GameState(self.size)
        for rc in self.gameState:
            new_state.gameState[rc] = self.gameState[rc]        
        new_state.numRebels = self.numRebels
        new_state.numSith = self.numSith
        new_state.numJedi = self.numJedi
        new_state.numTurns = self.numTurns
        new_state.maxs_turn = self.maxs_turn
        new_state.cachedWin = self.cachedWin
        new_state.cachedWinner = self.cachedWinner
        new_state.stringified = self.__str__()
        
        return new_state

    def display(self):
        """
        Present the game state to the console.
        """
        for r in range(1, self.size+1):
            print("+" + ("-+"*self.size))
            print("|", end="")
            for c in range(1, self.size+1):
                print(self.gameState[r,c], end="")
                print("|",end="")
            print()
        print("+" + ("-+"*self.size))


class Game(object):
    """ The Game object defines the interface that is used by Game Tree Search
        implementation.
    """
    
    def __init__(self, n=5, depthlimit=1):
        """ Initialization.
        """
        self.size = n
        self.depth_limit = depthlimit

    def initial_state(self):
        """ Return an initial state for the game.
        """
        state = GameState(self.size)
        return state

    def is_mins_turn(self, state):
        """ Indicate if it's Min's turn
            True if it's Min's turn to play
        """
        return not state.maxs_turn

    def is_maxs_turn(self, state):
        """ Indicate if it's Min's turn
            True if it's Max's turn to play
        """
        return state.maxs_turn

    def is_terminal(self, state):
        """ Indicate if the game is over.
        """
        return state.cachedWin or state.numTurns > 300 # or number of turns exceed, nobody can move, 

    def actions(self, state):
        """ Returns all the legal actions in the given state.
        """

        actions = []
        
        # if its player 1's turn
        if state.maxs_turn==True:
            # look through all the squares on the board
            for coords in state.gameState:
                # if its a rebel append allowable move and attack actions
                if state.gameState[coords]=='R':
                    if state.gameState[(coords[0]-1, coords[1])]== ' ':
                        actions.append("Move: Rebel @ {} --> {}".format(coords, (coords[0]-1, coords[1])))
                    if ((coords[0]-1, coords[1]+1) in state.gameState) and (state.gameState[(coords[0]-1, coords[1]+1)]== 'S'):
                        actions.append("Attack: Rebel @ {} --> Sith @ {}".format(coords, (coords[0]-1, coords[1]+1)))
                    if ((coords[0]-1, coords[1]-1) in state.gameState) and (state.gameState[(coords[0]-1, coords[1]-1)]== 'S'):
                        actions.append("Attack: Rebel @ {} --> Sith @ {}".format(coords, (coords[0]-1, coords[1]-1)))
                        
                # if its a jedi append allowable move and attack actions
                elif state.gameState[coords]=='J':
                    for direction in [(-1, 0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]:
                        coord = (coords[0]+direction[0], coords[1]+direction[1])
                        # walk in each direction until reaching the edge of board, or a player
                        while (coord in state.gameState) and (state.gameState[coord] == ' '):
                            actions.append("Move: Jedi @ {} --> {}".format(coords, coord))
                            coord = (coord[0]+direction[0], coord[1]+direction[1])
                        # if we ran into a sith we can attack
                        if (coord in state.gameState) and (state.gameState[coord] == 'S'):
                            actions.append("Attack: Jedi @ {} --> Sith @ {}".format(coords, coord))
                    
        else:
            for coords in state.gameState:
                if state.gameState[coords]=='S':
                    for direction in [(-1, 0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]:
                        coord = (coords[0]+direction[0], coords[1]+direction[1])
                        if (coord in state.gameState) and (state.gameState[coord] == ' '):
                            actions.append("Move: Sith @ {} --> {}".format(coords, coord))
                        elif (coord in state.gameState) and (state.gameState[coord] == 'R'):
                            actions.append("Attack: Sith @ {} --> Rebel @ {}".format(coords, coord))
                        elif (coord in state.gameState) and (state.gameState[coord] == 'J'):
                            actions.append("Attack: Sith @ {} --> Jedi @ {}".format(coords, coord))
                


        if len(actions)==0:
            actions.append("Pass")
            
        actions.sort()
            
        return actions        
        
        
    def result(self, state, action):
        """ Return the state that results from the application of the
            given action in the given state.
        """
        # clone the state
        new_state = state.myclone()



        if action=="Pass":
            new_state.maxs_turn = not state.maxs_turn
            new_state.numTurns = state.numTurns + 1
            new_state.stringified = new_state.__str__()
            return new_state

        # parse the details of the action
        action = action.rstrip().rsplit(": ")
        type = action[0]
        details = action[1].rsplit(" --> ")
        start = details[0].rsplit(" @ ")
        who = start[0]
        source = start[1]
        source = source[1:len(source)-1]
        source = source.rsplit(",")
        source = (int(source[0]), int(source[1]))
        if type=="Attack":
            end = details[1].rsplit(" @ ")
            victim = end[0]
            target = end[1]
            target = target[1:len(target)-1]
            target = target.rsplit(",")
            target = (int(target[0]), int(target[1]))
        else:
            target = details[1]
            target = target[1:len(target)-1]
            target = target.rsplit(",")
            target = (int(target[0]), int(target[1]))        
        
        
        if type=="Attack":
            if victim=="Sith" or victim=="Rebel":
                if who=="Rebel" and target[0]==1:
                    new_state.gameState[source] = ' '
                    new_state.gameState[target] = 'J'
                    new_state.numJedi += 1
                    new_state.numRebels -= 1
                else:
                    new_state.gameState[source] = ' '
                    new_state.gameState[target] = who[0]
                    if victim=="Rebel": new_state.numRebels -= 1
                    if victim=="Sith": new_state.numSith -= 1
            else:
                new_state.gameState[target] = 'S'
                new_state.numSith += 1
                new_state.numJedi -= 1
        else:
            if who=="Rebel" and target[0]==1:
                new_state.gameState[source] = ' '
                new_state.gameState[target] = 'J'
                new_state.numJedi += 1
                new_state.numRebels -= 1
            else:
                new_state.gameState[source] = ' '
                new_state.gameState[target] = who[0]
        
        
        new_state.maxs_turn = not state.maxs_turn
        new_state.numTurns = state.numTurns + 1
        self._cache_winner(new_state)
        new_state.stringified = new_state.__str__()
        
        return new_state

    def utility(self, state):
        """ Calculate the utility of the given state.
            :param state: a legal game state
            :return: utility of the terminal state
        """
        
        if state.cachedWin and state.cachedWinner:
            return 10000
        elif state.cachedWin and not state.cachedWinner:
            return -10000
        else:
            return 0


    def cutoff_test(self, state, depth):
        """
            Check if the search should be cut-off early.
        """
        return self.depth_limit > 0 and depth > self.depth_limit

    def eval(self, state):
        """
            When a depth limit is applied, we need to evaluate the
            given state to estimate who might win.
        """
        valueOfPlayers = 0
        valueOfRebelAdvancments = 0
        valueOfLocations = 0



        for coordinate in state.gameState:
            if state.gameState[coordinate]==state.blank:
                continue
            elif state.gameState[coordinate]==state.rebel:
                valueOfRebelAdvancments = -coordinate[0]
            elif state.gameState[coordinate]==state.jedi:
                continue
            elif state.gameState[coordinate]==state.sith:
                continue
            
            valueOfLocations += valueOfRebelAdvancments

            
        valueOfPlayers = state.numRebels + 4*state.numJedi - 4*state.numSith
        
        return valueOfPlayers*4 + valueOfLocations

    def congratulate(self, state):
        """ Called at the end of a game, might show stats
        """
        
        winstring = 'Congratulations, {} wins (utility: {})'
        if state.cachedWin and state.cachedWinner:
            print(winstring.format("Player1", self.utility(state)))
        elif state.cachedWin and not state.cachedWinner:
            print(winstring.format("Player2", self.utility(state)))
        else:
            print('No winner')
        
        return

    def transposition_string(self, state):
        """ Returns a unique string for the given state.
        """
        return state.__str__()
    
    
    def _cache_winner(self, state):
        """ Look at the board and check if the new move was a winner.
        """
        
        
        player1Win = True
        player2Win = True
        for coord in state.gameState:
            if state.gameState[coord] == 'R' or state.gameState[coord] == 'J':
                player2Win = False
            elif state.gameState[coord] == 'S':
                player1Win = False
                
        if player1Win == True or player2Win == True:
            state.cachedWin = True
            if player1Win == True:
                state.cachedWinner = True
            else:
                state.cachedWinner = False

        return
      
