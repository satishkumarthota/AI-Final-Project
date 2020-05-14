Connect4 is a two-player connection board game in which the players first choose a colour and then take turns dropping one coloured disc from the top into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs. Connect Four is a solved game. The first player can always win by playing the right moves.

Connect4 is a strategy board game where the player who aligns four disks wins. Program has two main components: 1. the search algorithm, and 2. the evaluation function. The evaluation function quantifies how desired or undesired a state of the board is for the agent. The search algorithm helps the agent decided on the next move by efficiently exploring what might be the consequences of each move. This program implements the Minmax algorithm  with Alpha Beta pruning — which substantially cuts the search space

Scoring Mechanism
We are scoring the dropping piece based on the position where it is getting dropped.
Center column       						opponent line of two = -2
Lines of two=2						opponent winnable line of three= -100
Lines of three=5
Win(connect4 )=100

Minmax: In minmax max algorithm we should look at the depth and the terminal node , in this situation the terminal node AI agent winning or the player winning or we use up all the pieces in the game  and we going to return the heuristic value of the board otherwise we need to recursively check the tree to find out the best scores.
Alpha-Beta pruning:
we can construct a game tree in which each node represents a possible game state. The internal nodes at an even depth represent either the initial game state (the root) or a game state which resulted from a move made by the opponent. The internal nodes at an odd depth represent game states resulting from moves made by us. If a state is game-ending (four tokens connected or board is full), it is a leaf node. Each leaf node is awarded a certain score and not further expanded.

The Evaluation function is supposed to evaluate how good a given state is for the agent, i.e., how close it is to winning the game. Once a player1 makes a move that should trigger the player2 to make a move.
Score heuristic will be implemented and will be independent from which piece was most recently dropped kid of look at all of the board and count how many 3 same coloured circles and 2 same coloured and if 4 same coloured found in a row it would get the highest score.
Here we need to pick the best move , for that we need to look at all the different columns we can make a move, basically run the score position  on all the columns and pick the highest score returned . This will actually show us which columns we can actually drop it in and then evaluate it from there.
