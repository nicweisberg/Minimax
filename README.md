# Minimax
 Implementation of minimax search with alpha-beta pruning


Minimax search is a decision making algorithm commonly found in two-player games such as chess or tic-tac-toe. It's essential a graph traversal algorithm that makes decisions based on the idea that it can only make every second decision about which path to explore, while the other player makes every other decision. With this is mind, the algorithm assumes the other player has the exact opposite goal as they do. More specifically, the algorithm makes every decision on the assumption that the following decision made will be the worst possible decision to achieve their goal. Having this knowledge allows the algorithm to "look ahead" down different paths, playing against itself as the other player, so it can determine the path to go down.

It works quite similar to how a human would play a game like chess: "If I move this piece here, my opponent will likely move their piece here, and then I'll move here", and so on. Computers are obviously more efficient than humans at keeping track of all the different possible paths, and that's why modern computers now have no trouble beating chess masters.

Alpha-beta pruning is a modification to basic minimax search, in that it doesn't waste its time exploring paths that it knows to be fruitless. More specifically, if a particual path is found to certainly be worse that a previously examined move, no other time will be spend exploring that part of the search tree.

My assignment was to implement minimax search on a modified version of chess, played with pieces similar to pawns, queens and kings.
