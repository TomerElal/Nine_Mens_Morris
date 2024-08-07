
# Nine Men's Morris

## Introduction

Welcome to Nine Men's Morris, a classic strategy board game that dates back to the Roman Empire. This game is designed for two players who aim to form 'mills' - a line of three of their own pieces. It’s a game of strategy and tactical skill.

## Game Rules

### Objective

The objective of the game is to reduce your opponent to two pieces or block all their possible moves.

### Setup

- Each player starts with nine pieces.
- The board consists of three concentric squares connected by lines at the midpoints of their sides.

### Phases of the Game

1. **Placing Pieces Phase**: Players take turns placing their pieces on any empty spot on the board.
2. **Moving Pieces Phase**: Once all pieces are placed, players take turns moving their pieces to adjacent spots.
3. **Flying Phase**: When a player is reduced to three pieces, they can 'fly', meaning they can move their pieces to any empty spot on the board.

### Forming a Mill

A 'mill' is formed when three of a player's pieces are aligned in a straight line along the board's connections. Forming a mill allows the player to remove one of the opponent's pieces from the board, except those in a mill unless no other pieces are available.

### Winning the Game

The game is won by reducing the opponent to two pieces or by blocking all the opponent's moves.

## Project Architecture

### Main Files and Directories

- **game.py**: Contains the `Game` class and the main game logic.
- **game_state.py**: Manages the state of the game.
- **move.py**: Contains the `MoveType` enum and move-related logic.
- **Nine_Men's_Morris.py**: The main entry point of the game.
- **piece.py**: Represents individual pieces on the board.
- **player.py**: Defines the `Player` class and its subclasses.
- **strings.py**: Contains string constants used in the project.
- **utils.py**: Utility functions used throughout the project.
- **exceptions/**: Custom exception classes.
- **player_types/**: Contains different player implementations.
- **search_agents/**: Implements search algorithms like Minimax and Expectimax.

### Classes and Inheritance

- **Game**: Manages the overall game flow.
- **GameState**: Maintains the current state of the game.
- **MoveType**: Enum for different types of moves.
- **Piece**: Represents a piece on the board.
- **Player**: Abstract base class for players, with subclasses for specific player types.
  - **GuiUserPlayer**: Allows a human player to interact with the game through GUI.
  - **RandomPlayer**: Implements a player that makes random moves.
  - **GuiMultiAgentsPlayer**: Implements a player that uses various algorithms (e.g., Minimax, AlphaBeta) through GUI.
- **BaseAgent**: Base class for search agents.
  - **MinimaxAgent**: Implements the Minimax algorithm for decision making.
  - **ExpectiMaxAgent**: Implements the Expectimax algorithm.
  - **AlphaBetaAgent**: Implements the Alpha-Beta pruning algorithm.

## Setup and Installation

### Prerequisites

- **Python**: Ensure you have Python 3.7 or higher installed.
- **Libraries**: Install the necessary libraries using pip.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TomerElal/Nine_Mens_Morris.git
   cd Nine_Mens_Morris
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

To start the game, run the following command:
```bash
python Nine_Men's_Morris.py
```

## Project Contents

- **game.py**: Main game logic.
- **game_state.py**: Manages game state.
- **move.py**: Move types and logic.
- **Nine_Men's_Morris.py**: Entry point of the game.
- **piece.py**: Game piece representation.
- **player.py**: Base player class.
- **strings.py**: String constants.
- **utils.py**: Utility functions.
- **exceptions/**: Custom exception handling.
- **player_types/**: Different player types (human, random, minimax).
- **search_agents/**: Search algorithms (base agent, minimax).

## Libraries

The project uses the following Python libraries:
- `colorama`: For colored console output.
- `enum`: For creating enumerations.
- `copy`: For making deep copies of objects.

You can install all dependencies using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```
