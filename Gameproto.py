
from colorama import Fore, Back, Style
from colorama import init
import random
from multiprocessing import process
import time
import os
class Board:
    def __init__(self, rows, columns):
        
        self.rows = int(rows)
        self.columns = int(columns)
        self.board = list([])
        for i in range(rows * columns):
           self.board.append("O")
    def PrintBoard(self, shipList):
        init()
        print("  ", end= " ")
        for i in range(self.columns):
            print(Fore.MAGENTA + chr(97 + i), end=" ")
        print(Style.RESET_ALL, end="")
        print("   ", end="")
        print("Ships: ", end="\n")
        for j in range(self.rows):
            print(Fore.YELLOW + f"{j + 1}", end = " ")
            if j < 9:
                print(" ", end="")
            print(Style.RESET_ALL, end="")
            for i in range(self.columns):
                print(Back.BLUE+ self.board[i + j * self.columns], end=" ")
                print(Style.RESET_ALL, end="")
            print("   ", end="")
            if j < len(shipList):
                for i in range(shipList[j][1]):
                    print(shipList[j][0], end="")
            print("\n", end="")
    def Shoot(self, playboard):
        while True:
            try:
                coord = input("Choose a coordinate to shoot(ex. a1): ")
                ycoord = ord(coord[0]) - 97
                coord = coord[1:]
                xcoord = int(coord) - 1
                if ycoord <= self.rows  and xcoord <= self.columns and playboard[xcoord + ycoord * self.columns] != "X":
                   if(playboard[xcoord + ycoord * self.columns] != "~"):
                       print("Hit!")
                       self.board[xcoord + ycoord * self.columns] = playboard[xcoord + ycoord * self.columns]
                       return 1
                   else:
                       print("Miss!")
                       self.board[xcoord + ycoord * self.columns] = "X"
                       return 0
                else:
                    raise ValueError
            except:
                print("Invalid input detected, please use the given format (ex. a1)")
class Ships(Board):
   def __init__(self, rows, columns):
      self.rows = int(rows)
      self.columns = int(columns)
      self.board= list([])
      for i in range(rows * columns):
        self.board.append("~")
      self.shipList = list([])
   def generateShip(self, shipLength, shipTexture):
      #choose random square and one of two directions (up)
      #ships: AA, BBB, CCC, DDDD, GGGGG, HHHHHH.
       #determine if ship is vertical or not
      flag = 0 #flag to check if ship is successfuly placed
       #flag to check for ship collision
      while flag == 0:
        collisionFlag = 0
        direction = random.randint(0,1)
        randomSquare = random.randint(0, self.rows * self.columns - 1) #choose random square on board
        if direction == 0: #check for horizontal space
            if(randomSquare  % self.columns + (shipLength - 1) < self.columns):
                for i in range(shipLength):
                    if(self.board[randomSquare + i] != "~" ): #check for ship collsion first
                       collisionFlag = 1
                if collisionFlag == 1:
                   continue
                flag = 1
                self.shipList.append((shipTexture, shipLength))
                for i in range(shipLength):
                    self.board[randomSquare + i] = shipTexture
        if direction == 1: #check for vertical space
            if(randomSquare + self.columns * (shipLength - 1) < self.rows * self.columns):
                for i in range(shipLength):
                    if(self.board[randomSquare + i * self.columns] != "~" ): #check for ship collsion first
                                collisionFlag = 1
                if collisionFlag == 1:
                        continue
                flag = 1
                self.shipList.append((shipTexture, shipLength))
                for i in range(shipLength):
                    self.board[randomSquare + i * self.columns] = shipTexture
            
                

            
         
    
    
       

  
# lent = Board(rows, columns)
# lent.PrintBoard()
# lent.Shoot()
# lent.PrintBoard()
def main():
    print("      ___       __   __         ___    ___  __     \n\
    |  | |__  |    /  ` /  \  |\/| |__      |  /  \    \n\
    |/\| |___ |___ \__, \__/  |  | |___     |  \__/    \n\
        __       ___ ___       ___  __          __     \n\
    |__)  /\   |   |  |    |__  /__` |__| | |__)    \n\
    |__) /~~\  |   |  |___ |___ .__/ |  | | |    \n")    
    while True:
        try:
            rows, columns = input("Choose the dimensions of the playboard(format: rows x columns, ex. 10 x 10):").split(" x ")
            rows = int(rows)
            columns = int(columns)
        except:
            print("Invalid input detected. Please type in the following format: rows x columns" )
        else:
            if( rows > 9 and columns > 9 and rows < 26 and columns < 26):
                break
            else:
                print("The board dimension restrictions are between 10 - 25")
                continue
    playerBoard = Board(rows, columns)
    shipGen = Ships(rows, columns)
    shipGen.generateShip(5, "A")
    shipGen.generateShip(4, "G")
    shipGen.generateShip(3, "B")
    shipGen.generateShip(3, "H")
    shipGen.generateShip(2, "C")
    lengthSum = 0
    shipsHit = 0
    for i in shipGen.shipList:
        lengthSum+= i[1]
    while shipsHit < lengthSum:
        os.system('cls')
        playerBoard.PrintBoard(shipGen.shipList)
        shipsHit += playerBoard.Shoot(shipGen.board) #shoot returns 1 if hit, 0 if miss
    print("You have sunk all the ships!")
if __name__ == "__main__":
    main()