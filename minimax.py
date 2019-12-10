# Nick Weisberg

import time as time

##########################################################################################
class SearchTerminationRecord(object):
    """A record to return information about the search
    """

    def __init__(self, value, move, time=0, nodes=0):
        self.value = value      # minimax value
        self.move = move        # a move with the stated minimax value
        self.time = time        # how much time was spent searching
        self.nodes = nodes      # How many nodes were expaded during the search

    def __str__(self):
        """Create a string representation of the Result data
        """
        text = 'Chose move <{}> with Minimax value {} after {:.4f} seconds, expanding {} nodes'
        return text.format(self.move, self.value, self.time, self.nodes)

    def display(self):
        """Display the record to the console
        """
        print(str(self))


##########################################################################################
class Minimax(object):
    """ An implementation of MiniMax Search
    """

    ifny = 2**20

    def __init__(self, game):
        """ Remember the game object.
        """
        self.game = game

    def minimax_decision_max(self, state):
        """ Return the move that Max should take in the given state
        """
        start = time.perf_counter()
        self.nodes_expanded = 0
        
        alpha = -self.ifny
        beta = self.ifny
        best = -self.ifny
        best_action = self.game.actions(state)[0]

        self.nodes_expanded += 1
        for act in self.game.actions(state):
            val = self.__min_value(self.game.result(state, act), alpha, beta, 1)
            if val > best:
                # remember something better
                best = val
                best_action = act
            alpha = max(alpha, best)

        end = time.perf_counter()

        return SearchTerminationRecord(best, best_action, end - start, self.nodes_expanded)

    def minimax_decision_min(self, state):
        """ Return the move that Min should take in the given state
        """
        
        start = time.perf_counter()
        self.nodes_expanded = 0
        
        alpha = -self.ifny
        beta = self.ifny

        best = self.ifny
        best_action = self.game.actions(state)[0]
        
        self.nodes_expanded += 1
        for act in self.game.actions(state):
            val = self.__max_value(self.game.result(state, act), alpha, beta, 1)
            if val < best:
                # remember something better
                best = val
                best_action = act
            beta = min(beta, best)
        
        end = time.perf_counter()
        
        return SearchTerminationRecord(best, best_action, end - start, self.nodes_expanded)

    def __max_value(self, state, alpha, beta, depth):
        """ Return the minimax value of the given state, assuming Max's turn to move.
        """

        if self.game.is_terminal(state):
            # the game is over, return the utility
            best = self.game.utility(state)
        elif self.game.cutoff_test(state, depth):
            best = self.game.eval(state)
        else:
            # look for the best among Max's options
            best = -self.ifny
            self.nodes_expanded += 1
            for act in self.game.actions(state):
                val = self.__min_value(self.game.result(state, act), alpha, beta, depth+1)
                if val > best:
                    # remember something better
                    best = val
                if best >= beta: return best
                alpha = max(alpha, best)
        return best

    def __min_value(self, state, alpha, beta, depth):
        """ Return the minimax value of the given state, assuming Min's turn to move.
        """
        if self.game.is_terminal(state):
            # the game is over, return the utility
            best = self.game.utility(state)
        elif self.game.cutoff_test(state, depth):
            best = self.game.eval(state)
        else:
            # look for the best among Max's options
            best = self.ifny
            self.nodes_expanded += 1
            for act in self.game.actions(state):
                val = self.__max_value(self.game.result(state, act), alpha, beta, depth+1)
                if val < best:
                    # remember something better
                    best = val
                if best <= alpha: return best
                beta = min(beta, best)
        return best


