import logging
from colorama import Fore, Back, Style
import os
import random
import threading
from functools import wraps
import time
MIN_SIZE = 10
MAX_SIZE = 25

logging.basicConfig(filename='battleship.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Decorator for logging method calls
def log_method_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling method: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
# Decorator for singleton pattern
def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
class Board:
    def __init__(self, rows, columns):
        self.rows = int(rows)
        self.columns = int(columns)
        self.board = ["O"] * (self.rows * self.columns)
        logging.info(f"Board initialized with {self.rows} rows and {self.columns} columns.")
    @log_method_call
    def print_board(self, ship_list):
        logging.info("Printing game board.")
        print("  ", end=" ")
        for i in range(self.columns):
            print(Fore.MAGENTA + chr(97 + i), end=" ")
        print(Style.RESET_ALL, end="")
        print("   ", end="")
        print("Ships: ", end="\n")
        for j in range(self.rows):
            logging.info(f"Printing row {j+1}.")
            print(Fore.YELLOW + f"{j + 1}", end=" ")
            if j < 9:
                print(" ", end="")
            print(Style.RESET_ALL, end="")
            for i in range(self.columns):
                print(Back.BLUE + self.board[i + j * self.columns], end=" ")
                print(Style.RESET_ALL, end="")
            print("   ", end="")
            if j < len(ship_list):
                for _ in range(ship_list[j][1]):
                    print(ship_list[j][0], end="")
            print("\n", end="")
    @log_method_call
    def shoot(self, playboard):
        while True:
            try:
                coord = input("Choose a coordinate to shoot (ex. a1) (press enter to quit): ")
                if not coord:
                    return -1
                logging.info(f"Player chose coordinate {coord}.")
                x_coord = ord(coord[0]) - 97
                coord = coord[1:]
                y_coord = int(coord) - 1
                if (0 <= y_coord < self.rows) and (0 <= x_coord < self.columns) and (playboard[x_coord + y_coord * self.columns] != "X"):
                    if playboard[x_coord + y_coord * self.columns] != "~":
                        print("Hit!")
                        logging.info("Player hit a ship.")
                        self.board[x_coord + y_coord * self.columns] = playboard[x_coord + y_coord * self.columns]
                        return 1
                    else:
                        print("Miss!")
                        logging.info("Player missed.")
                        self.board[x_coord + y_coord * self.columns] = "X"
                        return 0
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input detected, please use the given format (ex. a1)")
                logging.error("Invalid input format.")
@singleton
class Ships(Board):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.board = ["~"] * (self.rows * self.columns)
        self.ship_list = []
        logging.info("Ships initialized.")
    @log_method_call
    def load_ships_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    ship_length, ship_texture = line.strip().split(',')
                    self.generate_ship(int(ship_length), ship_texture)
        except FileNotFoundError:
            logging.error("Ship configuration file not found.")
            print("Ship configuration file not found.")
    @log_method_call
    def generate_ship(self, ship_length, ship_texture, timeout=5):
        flag = 0
        lock = threading.Lock()

        def generate():
            nonlocal flag
            while flag == 0:
                collision_flag = 0
                direction = random.randint(0, 1)
                random_square = random.randint(0, self.rows * self.columns - 1)
                if direction == 0:
                    if (random_square % self.columns) + (ship_length - 1) < self.columns:
                        for i in range(ship_length):
                            if self.board[random_square + i] != "~":
                                collision_flag = 1
                        if collision_flag == 1:
                            continue
                        with lock:
                            flag = 1
                            self.ship_list.append((ship_texture, ship_length))
                            for i in range(ship_length):
                                self.board[random_square + i] = ship_texture
                if direction == 1:
                    if (random_square + self.columns * (ship_length - 1)) < (self.rows * self.columns):
                        for i in range(ship_length):
                            if self.board[random_square + i * self.columns] != "~":
                                collision_flag = 1
                        if collision_flag == 1:
                            continue
                        with lock:
                            flag = 1
                            self.ship_list.append((ship_texture, ship_length))
                            for i in range(ship_length):
                                self.board[random_square + i * self.columns] = ship_texture

        thread = threading.Thread(target=generate)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            
            logging.error("Ship generation timed out.")
            raise TimeoutError("Ship generation timed out. Check your ship configuration file.")
    @log_method_call
    def print_board(self):
        logging.info("Printing game board with ships.")
        print("  ", end=" ")
        for i in range(self.columns):
            print(Fore.MAGENTA + chr(97 + i), end=" ")
        print(Style.RESET_ALL, end="")
        print("   ", end="")
        print("Ships: ", end="\n")
        for j in range(self.rows):
            logging.info(f"Printing row {j+1}.")
            print(Fore.YELLOW + f"{j + 1}", end=" ")
            if j < 9:
                print(" ", end="")
            print(Style.RESET_ALL, end="")
            for i in range(self.columns):
                print(Back.BLUE + self.board[i + j * self.columns], end=" ")
                print(Style.RESET_ALL, end="")
            print("   ", end="")
            if j < len(self.ship_list):
                for _ in range(self.ship_list[j][1]):
                    print(self.ship_list[j][0], end="")
            print("\n", end="")
def read_board_config():
    try:
        with open("board_config.txt", "r") as file:
            rows, columns = file.readline().strip().split(" x ")
            rows = int(rows)
            columns = int(columns)
            if not MIN_SIZE <= rows <= MAX_SIZE or not MIN_SIZE <= columns <= MAX_SIZE:
                raise ValueError("Board dimensions are out of range.")
            return rows, columns
    except FileNotFoundError:
        print("Board config file not found.")
        logging.error("Board config file not found.")
    except ValueError as e:
        print("Invalid board dimensions in config file:", e)
        logging.error("Invalid board dimensions in config file:", e)
def main():
    print("""
           ___       __   __         ___    ___  __     
     |  | |__  |    /  ` /  \  |\/| |__      |  /  \    
     |/\| |___ |___ \__, \__/  |  | |___     |  \__/    
      __       ___ ___       ___  __          __     
     |__)  /\   |   |  |    |__  /__` |__| | |__)    
     |__) /~~\  |   |  |___ |___ .__/ |  | | |    
    
    """)
    time.sleep(2)
    logging.info("Game started.")
    board_config = read_board_config()
    if board_config:
        rows, columns = board_config
    else:
        return
    player_board = Board(rows, columns)
    ship_gen = Ships(rows, columns)
    ship_gen.load_ships_from_file("ship_config.txt")  # Modify this line to specify the ship configuration file
    length_sum = sum(ship[1] for ship in ship_gen.ship_list)
    os.system('cls' if os.name == 'nt' else 'clear')
    player_board.print_board(ship_gen.ship_list)
    logging.info("Board printed.")
    ships_hit = 0
    while ships_hit < length_sum:
        flag = player_board.shoot(ship_gen.board)
        if flag == 1:
            os.system('cls')
            player_board.print_board(ship_gen.ship_list)
            print("Hit!")
            logging.info("Player hit a ship.")
            ships_hit += 1
        elif flag == -1:
            print("Quitting....")
            ship_gen.print_board()
            logging.info("Player quit the game.")
            return
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            player_board.print_board(ship_gen.ship_list)
            print("Miss!")
            logging.info("Player missed.")
    print("You have sunk all the ships!")
    logging.info("All ships sunk. Game over.")

if __name__ == "__main__":
    main()