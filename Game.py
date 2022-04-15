from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
import time
from random import random

from Grid import Grid

# This class inherits from Grid class  
class Game(Grid):

    def __init__(self,master,width,height):
        # This class inherits width and height properties from Grid class 
        super().__init__(master,width, height)
        # Parameters of the Main Window (root in main.py)
        self.Parent = master
        # change background color to white
        master.configure(background = 'white')

        # Create a Frame that will be used to contain the buttons
        self.frame_control = ttk.Frame()
        self.frame_control.pack()
        # Create  Buttons
        ttk.Button(self.frame_control, text = 'Run Manual',
                   command = self.start).pack(side = LEFT)
        ttk.Button(self.frame_control, text = 'Run Random',
                   command = self.random_start).pack(side = LEFT)
        ttk.Button(self.frame_control, text = 'Stop',
                   command = self.stop).pack(side = LEFT)        
        ttk.Button(self.frame_control, text = 'Reset Board',
                   command = self.reset_board).pack(side = LEFT)

        # Empty Arrays will be used to save the grid values
        self.board = []
        self.board_digit = []

        self.init_board()

        # Link the mouse Button click with the method get_loc
        # to change the cell value/color
        self.window.bind("<Button 1>",self.get_loc)

        # Attibutes to save the status of the game
        self.game_end = False
        self.threadStart = False

    # fill board and board_digit array
    def init_board(self):
        for i in range(10,self.width-10,10):
            temp = []
            temp1 = []
            for j in range(10,self.width-10,10):
                # To start, the board array is filled with hollow squares and the board_digit array is filled with zero
                # creat_square method call from parent (Grid class)
                temp.append(self.create_square(i,j))
                temp1.append(0)
            self.board.append(temp)
            self.board_digit.append(temp1)
            
    # The color of the squares is drawn based on the values of the board array 
    def draw_board(self):
        # number of vertical and horizental cell
        number_v_cell=int(self.width/10)-2
        number_h_cell=int(self.height/10)-2
        for row in range(number_h_cell):
            for col in range(number_v_cell):
                # If the value of the array is 1, the square is brown, otherwise it is white.
                if self.board_digit[row][col] == 1:
                    self.window.itemconfig(self.board[row][col], fill="brown")
                else:
                    self.window.itemconfig(self.board[row][col], fill="white")

    # fill board_digit array
    def fill_random_array(self,status="begin"):
        
        self.board_digit = []
        for column in range(10,self.width-10,10):
            # reset row
            nextRow = []
            for row in range(10,self.height-10,10):
                # if status is random, with call chance method fill array with 0 or 1 
                if status=="random":
                    nextRow.append(self.chance())
                # if begin status fill array with zero
                else:
                    nextRow.append(0)
            # putt a row in array
            self.board_digit.append(nextRow)
    # select 0 or 1 randomly
    def chance(self):
        if random() < 0.3:
            return 1
        else:
            return 0
    

    # Method to change the cell value/color after click event
    def get_loc(self, event):
        # if click on board coordinate
        if 10 < event.x < self.width-10 and 10 < event.y < self.height-10 :
            # if this cell dead
            if self.board_digit[event.x//10-1][event.y//10-1] == 0:
                # change color to alive (brown)
                self.window.itemconfig(self.board[event.x//10-1][event.y//10-1], fill="brown")
                # change status to 1 (alive)
                self.board_digit[event.x//10-1][event.y//10-1] = 1
            else:
                # change color to dead (white)
                self.window.itemconfig(self.board[event.x//10-1][event.y//10-1], fill="white")
                # change status to 0 (dead)
                self.board_digit[event.x//10-1][event.y//10-1] = 0 

    def new_board(self):
        # Get the size of the input array
        rows = len(self.board_digit)
        cols = len(self.board_digit[0])
        regenerate = []
        # Loop cell by cell within the input array
        for row in range(rows):
            temp = []
            for col in range(cols):
                # Count the total number of live neighbors
                neighbors = 0
                status = 0
                if row+1 <= rows-1:
                    if self.board_digit[row+1][col]==1:
                        neighbors += 1
                    if col+1 <= cols-1:
                        if self.board_digit[row+1][col+1]==1:
                            neighbors += 1
                        if self.board_digit[row][col+1]==1:
                            neighbors += 1
                    if col-1 >= 0:
                        if self.board_digit[row+1][col-1]==1:
                            neighbors += 1
                        if self.board_digit[row][col-1]==1:
                            neighbors += 1
                if  row-1 >= 0:
                    if self.board_digit[row-1][col]==1:
                        neighbors += 1
                    if col+1 <= cols-1:
                        if self.board_digit[row-1][col+1]==1:
                            neighbors += 1
                    if col-1 >= 0:
                        if self.board_digit[row-1][col-1]==1:
                            neighbors += 1
                # Change the status of the current cell based on Game of Life rules
                if self.board_digit[row][col] == 1 and 2<=neighbors<=3:
                    status = 1
                elif self.board_digit[row][col] == 0 and neighbors==3:
                    status = 1
                else:
                    status = 0
                temp.append(status)
            regenerate.append(temp)
        # Return the output array which represents the next generation 
        return regenerate

    # start game in manully mode with execute run method
    def start(self):
        if not self.threadStart:
            # flag for start and stop status
            self.threadStart = True
            self.game_end = False
            self.run()
    
    # start game in random mode
    def random_start(self):
        if not self.threadStart:
             # flag for start and stop status
            self.threadStart = True
            self.game_end = False
            # fill board_digit array with random number (0 or 1)
            self.fill_random_array("random")
            self.run()
    # reset board
    def reset_board(self):
        # fill board_digit array with 0
        self.fill_random_array()
        # draw board
        self.draw_board()

    # End method      
    def stop(self):
        self.threadStart = False
        self.game_end = True

    # Run Method:
    # will load the array to board_digit to get the next generation  and draw it
    def run(self):
        while not self.game_end:
            # save old board
            old_board = self.board_digit
            # regenerate bord wit call new_board method
            self.board_digit = self.new_board()
            # If there is no difference in the board, a message will be sent and end game
            if old_board == self.board_digit:
                messagebox.showinfo("Finish", "No changes from the last generation") 
                # end game
                self.stop()
                # end loop
                break
            self.draw_board()
            # create wait (0.1 secend) 
            time.sleep(0.1)
            # update gui
            self.Parent.update()


            
        


