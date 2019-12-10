# Nick Weisberg

from game import Game
import Players
import minimax as Searcher


# create the game, and the initial state
game = Game(n=5, depthlimit=5)
#game2 = Game(n=5, depthlimit=depth)

state = game.initial_state()

# set up the players
current_player = Players.VerboseComputer(game, Searcher.Minimax(game))
#current_player = Players.HumanMenu(game)

#other_player = Players.VerboseComputer(game2, Searcher.Minimax(game2))
other_player = Players.HumanMenu(game)


# play the game
while not game.is_terminal(state):

    state.display()

    # ask the current player for a move
    choice = current_player.ask_move(state)
    
    # check the move
    assert choice in game.actions(state), "The action <{}> is not legal in this state".format(choice)

    # apply the move
    state = game.result(state, choice)
    
    
    # swap the players
    current_player, other_player = other_player, current_player

# game's over
state.display()
game.congratulate(state)
