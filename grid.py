from turtle import Turtle
from turtle import Screen


WIDTH,HEIGHT=800,700 #Same as main screen.setup()
START_POSITION = (-370,300)

class Grid(Turtle):
    def __init__(self):
        super().__init__()
        self.draw_grid()

    def draw_grid(self):

        self.x=-375
        self.y=300
        self.penup()
        self.pencolor("lightgreen")
        self.speed("fast")
        self.hideturtle()
        # self.hideturtle()
        # #Horizontal
        for grid in range(0,21):
            self.goto(self.x,self.y)
            self.pendown()
            self.forward(600)
            self.y -= 30
            self.penup()
        """reset x and y values"""
        self.x = -375
        self.y = 300
        #Vertical
        self.goto(self.x, self.y)
        self.right(90)
        for grid in range(0,21):
            self.goto(self.x,self.y)
            self.pendown()
            self.forward(600)
            self.x += 30
            self.penup()
        self.hideturtle()

    def clear_grid(self):
        self.clear()