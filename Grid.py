from tkinter import *
class Grid():
    
    def __init__(self, master, width, height):
        # Create a Canvas window that will be used to draw the grid
        self.width = width
        self.height = height
        self.master = master
        self.window = Canvas(self.master, width=self.width, height=self.height, bg='white')
        self.window.pack()
    # create a rectangle in this coordinate (i,j)
    def create_square(self,i,j):
        return self.window.create_rectangle(i,j,i+10,j+10)
    # getter for width
    @property
    def width(self):
        return self._width
    # setter for width
    # Width must be greater than 100 and smaller than 600
    @width.setter
    def width(self, width):
        if width<=100 or width>600:
            raise ValueError("Width must be greater than 100 and smaller than 600")
        self._width = width
    @property
    def height(self):
        return self._width
        
    # setter for height
    # height must be greater than 100 and smaller than 600
    @height.setter
    def height(self, height):
        if height<=100 or height>600:
            raise ValueError("height must be greater than 100")
        self._height = height