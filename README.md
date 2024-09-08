
# Nine Men's Morris

## Introduction
Welcome to Nine Men's Morris, a classic strategy board game dating back to the Roman Empire. This game is designed for two players, aiming to form 'mills'—a line of three of their pieces. It’s a game of strategy and tactical skill, now available with advanced AI options!

## Game Rules

### Objective
The objective is to reduce your opponent to two pieces or block all their possible moves.

### Setup
- Each player starts with nine pieces.
- The board consists of three concentric squares connected by lines at the midpoints of their sides.

### Phases of the Game
- **Placing Pieces Phase**: Players take turns placing their pieces on any empty spot on the board.
- **Moving Pieces Phase**: Once all pieces are placed, players take turns moving their pieces to adjacent spots.
- **Flying Phase**: When a player is reduced to three pieces, they can 'fly'—moving their pieces to any empty spot.

### Forming a Mill
A 'mill' is formed when three pieces align in a straight line. Forming a mill allows the player to remove one of the opponent's pieces, except those in a mill (unless no other pieces are available).

### Winning the Game
The game is won by reducing the opponent to two pieces or blocking all the opponent's moves.

## Project Architecture

### Main Files and Directories
- `Nine_Men's_Morris.py`: The main entry point of the game. Handles command-line arguments, initializes the game, and manages the GUI or console modes.
- `game.py`: Contains the core Game class and game logic.
- `game_state.py`: Manages the state of the game, including players, pieces, and moves.
- `move.py`: Defines the MoveType enum and move-related logic.
- `piece.py`: Represents individual pieces on the board.
- `player.py`: Abstract base class for players and its specific player types.
- `strings.py`: String constants used throughout the project.
- `utils.py`: Utility functions for board and game operations.
- `exceptions/`: Custom exception classes for error handling.
- `player_types/`: Different player implementations, such as RandomPlayer, SmartPlayer, GuiUserPlayer, and GuiMultiAgentsPlayer.
- `search_agents/`: Implements search algorithms like Minimax, AlphaBeta, and DQN (Deep Q-Network).
- `logs/`: Logs game results (when using multiple games) into CSV format for easy analysis.

### Classes and Inheritance
- `GameManager`: Manages the overall game flow, including initialization and player turns.
- `GameState`: Maintains the current state of the game (board, players, and pieces).
- `MoveType`: Enum for different types of moves.
- `Piece`: Represents a piece on the board.
- `Player`: Abstract class for player types (GUI, random, smart, etc.).
- `GuiUserPlayer`: Allows a human player to interact through the GUI.
- `RandomPlayer`: A player that makes random moves.
- `SmartPlayer`: Uses a heuristic-based approach to make moves.
- `GuiMultiAgentsPlayer`: Interfaces AI agents like Minimax, AlphaBeta, and DQN with the GUI.
- `AlphaBetaAgent`, `DQNAgent`, `MCTSAgent`: Implements different AI strategies (AlphaBeta, DQN, MCTS).

### AI Players
- **Random Player**: Makes random moves and serves as a basic opponent.
- **Smart Player**: Employs a more advanced heuristic-based approach.
- **AlphaBeta Agent**: Uses the AlphaBeta pruning algorithm to minimize/maximize outcomes.
- **DQN Agent**: Deep Q-Network-based agent that learns through training.
- **MCTS Agent**: Monte Carlo Tree Search agent for strategic exploration.

## Setup and Installation

### Prerequisites
Ensure you have the following installed:
- **Python**: 3.7 or higher
- **Libraries**: Listed in `requirements.txt`

### Installation
Clone the repository:

```bash
git clone https://github.com/TomerElal/Nine_Mens_Morris.git
cd Nine_Mens_Morris
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

### Command-Line Options
You can run the game from the terminal with various options:

#### Without arguments (default to opening screen):
```bash
python Nine_Men's_Morris.py
```

#### With arguments (to run games in sequence):
```bash
python Nine_Men's_Morris.py --player1 [type] --player2 [type] --num_games [number] --first_player [player] --delay [seconds] --load
```

#### Example:
To run 10 games between an AlphaBeta AI and a Random AI with the AlphaBeta player starting and no delay:

```bash
python Nine_Men's_Morris.py --player1 alphabeta --player2 random --num_games 10 --first_player player1 --delay 0 --load
```

#### Parameters:
- `--train`: Train the DQN agent.
- `--load`: Load a pre-trained DQN model.
- `--player1`: Type of the first player (random, smart, alphabeta, mcts, dqn, user).
- `--player2`: Type of the second player.
- `--num_games`: Number of games to run.
- `--first_player`: The player who starts (player1 or player2).
- `--delay`: Delay between moves (in seconds) for viewing purposes.

### Saving Results to CSV
When running multiple games in sequence, the results are saved to a CSV file located in the `logs/` directory. The file is named as follows:

```bash
{player1.name}_vs_{player2.name}_{num_of_games}_games.csv
```

The CSV contains the following columns:
- **Winner**: 1 (Player 1) or 2 (Player 2).
- **PiecesLeft**: Number of pieces left for the winner.
- **TotalMoves**: Total number of moves in the game.
- **Score**: Score calculated from the game outcome.

## Libraries
The project uses the following Python libraries:
- `pygame`: For the graphical user interface.
- `torch`: For implementing the DQN (Deep Q-Network) agent.
- `colorama`: For colored console output.
- `numpy`: For numerical operations.
- `pandas`: For handling CSV logging and data analysis.

To install the required libraries:

```bash
pip install -r requirements.txt
```

## Additional Information

### AI Agents:
- **AlphaBetaAgent**: Implements the AlphaBeta pruning algorithm to make decisions based on the minimax principle.
- **DQNAgent**: A reinforcement learning agent that uses neural networks to make decisions by training through many episodes.
- **MCTSAgent**: Uses Monte Carlo simulations to explore possible moves and outcomes.

### GUI and Console Modes
You can choose between running the game in a graphical user interface (GUI) or a console-based game. By default, the game runs in GUI mode, but you can run console games by changing the `gui_display` flag in the `GameManager`.
