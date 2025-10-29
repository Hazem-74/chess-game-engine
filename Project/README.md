# Chess Game Engine

This project implements a functional Chess Game Engine with a graphical user interface (GUI) using Pygame. It allows two players to play a game of chess, featuring core game logic, move validation, special moves like castling and en passant, and pawn promotion.

## Table of Contents

*   [Features](#features)
*   [Project Structure](#project-structure)
    *   [Engine.py](#enginepy)
    *   [Main.py](#mainpy)
*   [Requirements](#requirements)
*   [Installation](#installation)
*   [How to Run](#how-to-run)
*   [Usage](#usage)
*   [Credits](#credits)

## Features

*   Full chess game logic (move generation, validation, board state management).
*   Graphical user interface using Pygame for interactive gameplay.
*   Handles complex chess rules including:
    *   Pawn promotion (to Queen, Rook, Knight, or Bishop).
    *   En passant captures.
    *   Castling (both kingside and queenside).
*   Accurate detection of check, checkmate, and stalemate game states.
*   Ability to undo the last move for strategic replays or error correction.
*   Clear visual feedback for selected pieces, possible moves, and king in check.
*   Persistence of the current board state by writing to `Board.txt` after each move.

## Project Structure

### `Engine.py`

This file contains the foundational logic for the chess game. It defines the `Game` class, which encapsulates the entire state and rules of the chessboard, and the `Move` class, which represents individual chess moves.

**Main Logic:**

*   **`Game` Class**:
    *   **Initialization (`__init__`)**: Sets up the initial board configuration by reading from `Board_Initial.txt`. It tracks the current player (`white_to_move`), the positions of both kings, a log of all moves made (`moveLog`), and flags for special conditions like `checkmate`, `stalemate`, and the `en_passant_pos` square.
    *   **Move Execution (`make_move`)**: Applies a given `Move` object to the board. It updates the piece positions, handles special move mechanics (pawn promotion with an optional `piece` argument, en passant capture, and rook movement during castling), and records the move in `moveLog`. The updated board state is then written to `Board.txt`.
    *   **Move Reversal (`undo_move`)**: Reverts the last move from `moveLog`, restoring the board to its previous state, and updating the king positions accordingly. It also updates `Board.txt`.
    *   **Move Generation (`all_possible_moves`)**: Generates a dictionary of all pseudo-legal moves for the current player. These are moves that follow the basic movement rules of each piece but do not yet account for whether the king would be left in check.
    *   **Move Validation (`only_valid_moves`)**: Filters the `all_possible_moves` to include only truly legal moves (i.e., those that do not result in the current player's king being in check). This method is crucial for determining checkmate and stalemate conditions.
    *   **Check Detection (`in_check`, `square_threatened`)**:
        *   `in_check()`: Checks if the current player's king is under attack by any opponent piece.
        *   `square_threatened(r, c)`: A helper method that determines if a specific square `(r, c)` is attacked by the opposing player's pieces.
    *   **Piece-Specific Move Functions**: Methods such as `pawn_moves`, `rook_moves`, `knight_moves`, `bishop_moves`, `queen_moves`, and `king_moves` are responsible for calculating all possible moves for their respective piece types from a given position, adhering to standard chess rules.
*   **`Move` Class**:
    *   **Initialization (`__init__`)**: Stores comprehensive details about a move, including the starting and ending row/column, the piece that moved, and the piece (if any) that was captured.
    *   **Special Move Flags**: Includes boolean flags like `pawn_promotion`, `en_passant`, `qside_castle`, and `kside_castle` to indicate specific move types.
    *   **Unique ID (`moveID`)**: Generates a unique integer ID for each move to facilitate comparison.
    *   **Equality (`__eq__`)**: Allows `Move` objects to be compared based on their `moveID`.
    *   **Notation Conversion (`rank_file`, `from_to_notation`)**: Provides utility functions to convert board coordinates to and from standard algebraic chess notation.

### `Main.py`

This file handles the graphical user interface (GUI) and user interaction for the chess game using the Pygame library. It serves as the primary entry point and orchestrates the visual presentation and player input, interacting with the `Engine.py` for game logic.

**Main Logic:**

*   **`main()` Function**:
    *   **Pygame Setup**: Initializes Pygame, configures the display window (512x512 pixels), sets up the game clock, and loads the game window icon (`Icon.png`).
    *   **Game Initialization**: Creates an instance of `Engine.Game` to manage the game state and loads all piece images through `import_pieces()`.
    *   **Main Game Loop**: The central loop continuously processes user input and updates the game display:
        *   **Event Handling**: Monitors for user events, including closing the window (`p.QUIT`), mouse clicks (`p.MOUSEBUTTONDOWN`) for selecting pieces and making moves, and keyboard presses (specifically, the 'Z' key for undoing moves).
        *   **Move Processing**: Interprets mouse clicks to identify selected squares and attempted moves. It validates potential moves using `validate_move()` and, if legal, calls `gs.make_move()` from the `Engine`. Special handling is included for pawn promotion, which triggers `pawn_promotion_menu()`.
        *   **Game State Updates**: After each successful move or undo operation, `gs.only_valid_moves()` is called to re-calculate all legal moves, updating the game's understanding of possible actions and current status (checkmate/stalemate).
        *   **Rendering**: Invokes `draw_game()` to render the board and pieces, and `draw_end()` to display game-over messages.
*   **`import_pieces()`**: Loads all chess piece image files (e.g., `wR.png`, `bp.png`) from the `Pieces/` directory into a global dictionary `pieces_images` for efficient retrieval during drawing.
*   **`draw_board(screen, click_pair, valid_moves, gs)`**: Renders the chessboard's 8x8 grid with alternating colors. It highlights the `selected_square` in yellow and draws indicators for `valid_moves`. If the king is in check, its square is highlighted in red.
*   **`draw_pieces(screen, board)`**: Iterates through the current `board` state and draws the appropriate piece images onto the screen at their correct positions.
*   **`draw_game(screen, gs, click_pair, valid_moves)`**: A wrapper function that orchestrates the drawing process by calling `draw_board()` and `draw_pieces()`.
*   **`validate_move(move, valid_moves, gs)`**: Checks if a `move` proposed by the player is present in the `valid_moves` dictionary provided by the `Engine`, or if it corresponds to a valid castling maneuver by calling `castling()`.
*   **`draw_moves(screen, click_pair, valid_moves)`**: When a piece is selected, this function draws yellow circles on all squares where that piece can legally move, according to `valid_moves`.
*   **`draw_danger(screen, wk, bk, gs)`**: Visually indicates if either king is in check by drawing a red rectangle around its square.
*   **`draw_end(screen, gs)`**: Displays "CHECKMATE!!" or "STALEMATE!!" messages prominently on the screen when the game reaches a terminal state. It uses a custom font defined in `comic-sans-ms/COMIC.ttf`.
*   **`pawn_promotion_menu(gs)`**: Presents a simple graphical menu to the player when a pawn reaches the last rank, allowing them to choose which piece (Queen, Knight, Bishop, or Rook) to promote it to.
*   **`castling(gs, move, valid_moves)`**: A function designed to specifically check the legality of castling moves, verifying king/rook movement history, clear paths, and absence of checks along the castling path. It also sets the appropriate castling flags on the `move` object.
*   **`castling_check(gs, valid_moves, tuple)`**: This helper function dynamically adds legal castling moves to the `valid_moves` dictionary (for the selected king) so they can be highlighted on the board and made by the player.

## Requirements

Before running the project, ensure you have the following installed:

*   **Python 3.x**: The project is written in Python.
*   **Pygame library**: Essential for the graphical user interface.

**Required Assets and Files:**

The project relies on several external files and directories for its functionality and visuals. Ensure these are present in your project directory:

*   `Board_Initial.txt`: This text file defines the starting layout of the chess pieces on the board.
*   `Board.txt`: This file is dynamically created and updated by `Engine.py` during runtime to save the current state of the board after each move. It does not need to exist initially.
*   `Icon.png`: The image file used as the icon for the game window.
*   `Pieces/` directory: This directory must contain PNG image files for all chess pieces (e.g., `wR.png` for white rook, `bK.png` for black king, `wp.png` for white pawn, etc.).
*   `comic-sans-ms/` directory: This directory should contain the `COMIC.ttf` font file, which is used for displaying end-game messages like "CHECKMATE!!".

Ensure all these files and the `Pieces/` and `comic-sans-ms/` directories are located within the `Project` directory alongside `Engine.py` and `Main.py`.

## Installation

To get the Chess Game Engine up and running on your local machine, follow these steps:

1.  **Clone the Repository**:
    Open your terminal or command prompt and clone the GitHub repository:
    ```bash
    git clone https://github.com/Hazem-74/Chess-Game-Engine.git
    cd "Chess Game Engine/Project"
    ```
    This command will download the project files and navigate you into the `Project` directory where the main scripts reside.

2.  **Install Dependencies**:
    Install the Pygame library using pip, Python's package installer:
    ```bash
    pip install pygame
    ```

3.  **Verify Assets**:
    Confirm that all required asset files (`Board_Initial.txt`, `Icon.png`) and directories (`Pieces/`, `comic-sans-ms/` with `COMIC.ttf` inside) are correctly placed within the `Project` directory. If any are missing, the game may not run correctly.

## How to Run

After completing the installation steps, navigate to the `Project` directory (if you're not already there) in your terminal and execute the `Main.py` script:

```bash
python Main.py
```

A Pygame window should open, displaying the chessboard ready for play.

## Usage

*   **Making a Move**: To make a move, first click on the piece you wish to move. If it's a valid piece for the current player's turn, yellow circles will appear on all squares where that piece can legally move. Click on one of these highlighted squares (or an enemy piece on a valid target square) to complete the move.
*   **Undo Last Move**: At any point during the game, you can press the `Z` key on your keyboard to undo the last move made.
*   **Pawn Promotion**: If one of your pawns reaches the opposite end of the board, a promotion menu will automatically appear. Click on the image of the piece (Queen, Rook, Bishop, or Knight) you wish to promote your pawn to.
*   **Game End**: The game will automatically detect and display "CHECKMATE!!" or "STALEMATE!!" messages when a game-ending condition is met.
*   **Exit Game**: Simply close the Pygame window to exit the application.

## Credits

Developed by Hazem-74.