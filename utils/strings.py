from colorama import Style, Fore

# Prompts

PLAYER_REMOVE_ERROR_TEMPLATE = (
    "Player {name} tried to remove opponent's piece at location {location} but there is no piece in this location"
)

WINNER_ANNOUNCEMENT_TEMPLATE = "\n🔶🔷🔶 {color}The Winner is {name} 🔶🔷🔶\n"
RESULT = "\n🔶🔷🔶 With a result of {color}{num_pieces_left} {other_color}pieces left on his side!{reset} 🔶🔷🔶\n\n"
UNCORRELATED_PIECE_COLOR_ERROR_TEMPLATE = (
    "{player_name} asked to move his piece (in {player_color} color) at location"
    " ({prev_row}, {prev_col}), but the color there is {actual_color}."
)

GAME_PHASE_ERROR_TEMPLATE = (
    "The current move type is to {move_type} and the player {player_name} tried to move his piece"
)

PIECE_NOT_EXIST_ERROR_TEMPLATE = "Couldn't find a piece with the specified location {position}"

GAME_PHASE_ERROR_REMOVE_TEMPLATE = (
    "The current move type is to {move_type} and {player_name} tried to remove opponent's piece"
)

GAME_PHASE_ERROR_PLACE_TEMPLATE = (
    "The current move type is to {move_type} and {player_name} tried to place a new piece"
)

UNCORRELATED_PIECE_COLOR_DEFAULT_MESSAGE = "The piece color does not match the expected color"

SEPERATOR = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

PLAYER_CHOOSE_MOVEMENT = (SEPERATOR + Fore.LIGHTMAGENTA_EX +
                           "\nIt's time for the {player_name} to move a piece.\n"
                           + Style.RESET_ALL + SEPERATOR)

PLAYER_CHOOSE_PLACEMENT = (SEPERATOR + Fore.LIGHTMAGENTA_EX +
                            "\nIt's time for the {player_name} choose a place for new piece.\n"
                            + Style.RESET_ALL + SEPERATOR)
PLAYER_CHOOSE_REMOVAL = (SEPERATOR + Fore.LIGHTYELLOW_EX +
                          "\n🚀🚀 It's time for the {player_name} to remove opponent's piece! 🚀🚀\n"
                          + Style.RESET_ALL + SEPERATOR)

PLAYER_MOVED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "{player_name} chose to move piece from location "

PLAYER_PLACED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "{player_name} chose to place a piece at location "

PLAYER_REMOVED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "{player_name} chose to remove opponent's piece from location "

TO_LOCATION = " to location "


INSERT_PIECE_INDEX_TO_MOVE = ("Choose a piece of yours to move.\nInsert it's index by the format [num_row][num_column]."
                              "\nFor example, if you want to move a piece that placed in row number 5 and"
                              " column number 2, insert: 52\n📝️ Your Choice 👉🏻:  ")

INSERT_PIECE_NEW_INDEX = (SEPERATOR + Fore.LIGHTMAGENTA_EX +
                          "Now choose a new place for your piece."
                          + Style.RESET_ALL + SEPERATOR +
                          "Insert it's index by the format [num_row][num_column]."
                          "\nFor example, if you want to move a piece to a placed in row number 3 and"
                          " column number 1, insert: 31\n📝️ Your Choice 👉🏻:  ")

CHOOSE_NEW_PIECE_PLACEMENT = (
    "Choose a placement for your piece.\nInsert it's index by the format [num_row][num_column]."
    "\nFor example, if you want to place the piece in row number 7 and column number 2, insert: 72\n"
    "📝️ Your Choice 👉🏻:  ")

CHOOSE_OPPONENT_PIECE_TO_REMOVE = (SEPERATOR + Fore.LIGHTYELLOW_EX +
                                   "🚀🚀 Choose an index of opponent's piece to remove! 🚀🚀"
                                   + Style.RESET_ALL + SEPERATOR +
                                   "Insert the index by the format [num_row][num_column]."
                                   "\nFor example, if you want to remove a piece from row number 2 and"
                                   " column number 1, insert: 21\n📝️ Your Choice 👉🏻:  ")

INVALID_INPUT_FORMAT = (SEPERATOR + Fore.LIGHTCYAN_EX + "You have entered an invalid index format. Try again!" +
                        Style.RESET_ALL + SEPERATOR)

INVALID_INDEX = (SEPERATOR + Fore.LIGHTCYAN_EX + "The index you've entered is invalid. Try again!" +
                 Style.RESET_ALL + SEPERATOR)

PLAYER_TURN_GREETING_TEMPLATE = "{color}\n{name} {reset}it's your turn! 😎\n"

RANDOM_PLAYER = "Random Player"

SMART_PLAYER = "Smart Player"

MCTS_PLAYER = "MCTS Player"

MINIMAX_PLAYER = "Minimax Player"

EXPECTIMAX_PLAYER = "Expectimax Player"

ALPHA_BETA_PLAYER = "AlphaBeta Player"

PLAYER2 = "Player 2"

PLAYER1 = "Player 1"
