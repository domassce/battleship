# Coursework Report: Single-Player Battleship Game

## 1. Introduction

In this coursework, I developed a single-player Battleship game run entirely within the terminal. The game leverages configuration files to allow for customizable settings such as board size, ship types, and ship sizes. The objective of the game is for the player to sink all the randomly placed ships within the specified board size.

## 2. Game Mechanics

The game follows traditional Battleship rules, with the following mechanics:

- **Board Generation**: The game generates a board of a specified size and randomly places ships of varying sizes on the board.
- **Guessing**: The player guesses coordinates on the board to determine if they hit or miss a ship.
- **Win Condition**: The player wins the game by sinking all ships on the board.
## 2. 4 OOP Pillars

1. **Encapsulation**:
    
    Encapsulation involves bundling the data (attributes) and methods (functions) that operate on the data into a single unit, which is called a class. Here's an example of encapsulation in my code:
    
    `class Board:`\
	    `def __init__(self, rows, columns):`  
		    `self.rows = int(rows)`\
		    `self.columns = int(columns)`\
		    `self.board = ["O"] * (self.rows * self.columns)`\
    `...`
    
    In this snippet, the `Board` class encapsulates attributes like `rows`, `columns`, and `board`, along with methods like `print_board` and `shoot`.
    
2. **Abstraction**:
    
    Abstraction involves hiding the complex implementation details and showing only the essential features of the object. Here's an example of abstraction in my code:\
    `class Ships(Board):`\
	    `def __init__(self, rows, columns):`         
		    `super().__init__(rows, columns)`\
		    `self.board = ["~"] * (self.rows * self.columns)`       
		    `self.ship_list = []    ...`
    
    In this snippet, the `Ships` class abstracts the concept of ships within the game. It inherits from the `Board` class, representing a relationship where `Ships` is a specialized version of `Board` with additional ship-related functionality.
    
3. **Inheritance**:
    
    Inheritance allows a new class to inherit attributes and methods from an existing class. Here's an example of inheritance in my code:
    
    `class Ships(Board):...`
    
    In this snippet, the `Ships` class inherits from the `Board` class using the syntax `class Ships(Board):`. This means that `Ships` inherits attributes and methods from `Board` and can also extend or override them as needed.
    
4. **Polymorphism**:
    
    Polymorphism allows objects of different classes to be treated as objects of a common superclass. In my code polymorphism appears in the form of method overriding. Here's the forementioned code:  
       `class Board:`  
	  `...`  
	     `@log_method_call`     
	     `def print_board(self, ship_list):`   
		     `logging.info("Printing game board.") # Printing the game board`    
     `...`  
     `Ships(Board):`  
     `...`  
     `@log_method_call`  
	     `def print_board(self):`  
		     `logging.info("Printing game board with ships.")`  
     `...`  

## 3. Design Patterns

1. **Decorator Pattern**:

 `# Decorator for logging method calls`
`def log_method_call(func):`     
`@wraps(func)`     
	`def wrapper(*args, **kwargs):`         
	`logging.info(f"Calling method: {func.__name__}")`         
	`return func(*args, **kwargs)`    
`return wrapper`

In this snippet, `log_method_call` is a decorator function. It takes another function `func` as its argument and returns a new function `wrapper` that wraps around `func`. Inside `wrapper`, it logs a message indicating that the decorated method is being called, and then it calls the original function `func`.

2. **Singleton Pattern**:

`def singleton(cls):`
	`instances = {}`     
	`@wraps(cls)`     
	`def get_instance(*args, **kwargs):`         
		`if cls not in instances:`             
		`instances[cls] = cls(*args, **kwargs)`        
		`return instances[cls]`      
	`return get_instance`  
`@singleton` 
`class Board:     ...`

In this snippet, `singleton` is a decorator function that takes a class `cls` as its argument and returns a wrapper function `get_instance`. This wrapper function maintains a dictionary `instances` to store instances of classes. When `get_instance` is called, it checks if an instance of `cls` exists in `instances`. If not, it creates a new instance and stores it in `instances`. Finally, it returns the instance. By decorating a class with `@singleton`, you ensure that only one instance of that class exists throughout the program. In this case, the `Board` class is decorated with `@singleton`, making it a singleton class.

## 4. Reading from file & writing to file

1. **Reading from File**:
   
    `def read_board_config():`
         `try:`         
	         `with open("board_config.txt", "r") as file:`             
	         `rows, columns = file.readline().strip().split(" x ")`            
	         `rows = int(rows)`             
	         `columns = int(columns)`             
	         `if not MIN_SIZE <= rows <= MAX_SIZE or not MIN_SIZE <= columns <= MAX_SIZE:`                 
		         `raise ValueError("Board dimensions are out of range.")`             
	         `return rows, columns`     
         `except FileNotFoundError:`         
	         `print("Board config file not found.")`         
	         `logging.error("Board config file not found.")`    
	     `except ValueError as e:`         
		     `print("Invalid board dimensions in config file:",e)`
		     `logging.error("Invalid board dimensions in config file:",e)` 
    
    In this code snippet, the function `read_board_config()` reads from the file `"board_config.txt"`. It opens the file in read mode (`"r"`) and reads the first line. It then processes the data to extract rows and columns information for the game board configuration.
    
3. **Writing to File**:
    `logging.basicConfig(filename='battleship.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')`
    
    In this snippet, the `logging.basicConfig()` function is used to configure logging for the program. It specifies the filename (`'battleship.log'`) to which log messages will be written. Log messages, including timestamps, log levels, and the actual messages, are formatted according to the specified format (`'%(asctime)s - %(levelname)s - %(message)s'`). The logging level is set to `INFO`, indicating that log messages with severity level `INFO` and higher will be recorded in the log file.

## 5. Key Features

- **Customizable Settings**: Configuration files allow for flexible customization of game settings.
- **Randomized Gameplay**: Both the board layout and ship placements are randomized, providing unique gameplay experiences.
- **Terminal Interface**: The game is played entirely within the terminal, making it accessible across different platforms.

## 6. Libraries Used
- **Libraries**: 
- `logging`: This library is used for logging messages to a file (`battleship.log` in this case) to track the execution flow and events in the program.
- `colorama`: This library provides cross-platform support for colored terminal text output. It's used to display colored text in the terminal.
- `os`: This library provides functions for interacting with the operating system. In this code, it's used to clear the terminal screen (`os.system('cls' if os.name == 'nt' else 'clear')`) for better presentation.
- `random`: This library provides functions for generating random numbers. It's used for random ship placement in the `Ships` class.
- `threading`: This library provides facilities for multi-threading in Python. It's used for asynchronous ship generation in the `Ships` class.
- `functools`: This library provides functions for higher-order functions and operations on callable objects. It's used for the `wraps` decorator in the `log_method_call` decorator.

## 7. Development Process

- **Challenges**: One challenge faced during development was ensuring efficient and fair randomization of ship placements on the board.
- **Testing and Debugging**: Extensive testing was conducted to ensure the game functions correctly under various configurations. Debugging primarily involved identifying issues with randomization and user input handling.

## 8. Reflections and Future Improvements

Overall, developing this single-player Battleship game was a rewarding experience. However, there are areas for improvement:

- **Enhanced User Interface**: Incorporating a graphical user interface (GUI) could improve the user experience.
- **Optimization**: Optimizing the randomization algorithm for ship placements could improve gameplay performance.
- **Additional Features**: Adding features such as multiple difficulty levels or a scoring system could enhance replay value.

## 9. Conclusion

In conclusion, developing this single-player Battleship game provided valuable insights into game development processes, including design, implementation, testing, and debugging. By leveraging configuration files and randomization techniques, the game offers customizable and engaging gameplay experiences within the terminal environment.
