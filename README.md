# Ataxx

This project is an object-oriented Python implementation of the classic board game Ataxx, designed with UML modeling and supporting remote two-player matches using the [DOG (Doing Online Games)](https://www.inf.ufsc.br/~ricardo.silva/dog/)  framework. The project features a GUI built with Tkinter, allowing players to compete online in real-time.


## About the Game
Ataxx is a strategy board game where two players compete to dominate the board. On their turn, a player can:

- **Clone** a piece to an adjacent empty square, creating a new piece.
- **Jump** a piece two squares away, leaving the original square empty.

Any opponent pieces adjacent to the destination **change to the player's color**. The game ends when the board is full or one of the players has no pieces left. The player with the most pieces wins.


## Setup and Usage

These instructions will help you get the game running on your machine.

### Prerequisites

- Python 3.10 or higher
- `virtualenv` for running the game in an isolated environment

### Installation & Execution

#### On Windows

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    
2. Create a virtual environment:  
   ```bash
   virtualenv venv

3. Activate the virtual environment:
   ```bash
    venv\Scripts\activate

4. Install the dependencies:
   ```bash
    pip install -r requirements.txt

5. Run the program:
   ```bash
    python src/ataxx.py

#### On Linux/macOS

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    
2. Create a virtual environment:
   ```bash
    python3 -m venv venv

3. Activate the virtual environment:
   ```bash
    source venv/bin/activate

4. Install the dependencies:
   ```bash
    pip install -r requirements.txt

5. Run the program:
   ```bash
    python src/ataxx.py

