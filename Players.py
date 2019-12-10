# Nick Weisberg

##########################################################################################
class PlayerInterface(object):
    """ A class for Player interfaces
    """
    def __init__(self, game):
        self.game = game


##########################################################################################
class HumanMenu(PlayerInterface):
    """ This interface puts the actions in a menu, asks for a choice
        from the menu, and waits for the user to type something.
    """
    def __init__(self, game):
        PlayerInterface.__init__(self, game)

    def ask_move(self, state):
        """ Present the human player with a menu of possible moves.
            The moves are obtained from the game
        """

        # present the user with moves that are legal
        actions = self.game.actions(state)

        print("It's the Human's turn!  Choose one of the moves:")
        for i,act in enumerate(actions):
            print("#{}: {}".format(i, act))
        
        # wait for a valid choice from the menu
        choice = -1
        while choice > i or choice < 0:
            choice = int(input("Type in the move number: "))
            if choice > i or choice < 0:
                print("Can't choose that.")
        
        # return the choice
        return actions[(choice)]


##########################################################################################
class ComputerInterface(PlayerInterface):
    """ This subclass of PlayerInterface stores a search class object.
    """
    def __init__(self, game, searcher):
        PlayerInterface.__init__(self, game)
        self.searcher = searcher

    def _ask_move_searcher(self, state):
        """ This method interacts with the searcher object.
            Sub-classes can use this, and do other things as well.
        """
        if self.game.is_maxs_turn(state):
            result = self.searcher.minimax_decision_max(state)
        else:
            result  = self.searcher.minimax_decision_min(state)
        return result
       

##########################################################################################
class VerboseComputer(ComputerInterface):
    """ This interface uses the ComputerInterface to get a move 
        from the searcher.
    """
    def __init__(self, game, searcher):
        ComputerInterface.__init__(self, game, searcher)

    def ask_move(self, state):
        """ Get a move from the search algorithm.  Some dialogue on console IO.
        """
        print("Thinking...")

        result = super()._ask_move_searcher(state)

        print("...done")
        result.display()

        return result.move

