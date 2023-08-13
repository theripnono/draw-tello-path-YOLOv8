from turtle import Turtle
from turtle import Screen
from tkinter import *
from grid import Grid
GREY="#d3d3d3"
DARK_GREY = "#949494"
GREEN ="#b7d5ac"
START_POSITION = (-370,300) #Drone start position
screen = Screen()
screen.setup(width=800, height=700)
screen.title("DRAWING PATH")

rotate_list=[]



check_x_list=[False]

tracking_coordinates = [START_POSITION]
position_coordinates = [(0,0)]


path_list = [{"rotation":None,"motion": {
            "fw_bw":None,"distance":()
            }
        }
    ]
def rotate_left():

    """
    It totates 90º the turtle head and store the rotations in a list.
    :return: list with the rotation
    """

    t.left(90)

    rotate_list.append("Rotate Left")

def rotate_right():

    """
    It totates 90º the turtle head and store the rotations in a list.
    :return: list with the rotation
    """

    t.right(90)
    rotate_list.append("Rotate Right")





"""Initializing start position"""
t = Turtle()
#grid = Grid()
t.pensize(width=3)
t.penup()
t.setheading(270)
t.goto(START_POSITION)

start_pos = t.position()
t.pendown()
"""######################"""

def tracking(coordinates):


    tracking_coordinates.append(coordinates)
    distance = (int((abs((tracking_coordinates[-1][0])))-int(abs((tracking_coordinates[-2][0])))) , int((abs((tracking_coordinates[-1][1])))-int(abs((tracking_coordinates[-2][1])))))

    position_coordinates.append(distance)

    print("las coordenadas son: ", tracking_coordinates)
    print("Se ha movido = ", position_coordinates)



    if tracking_coordinates[-2][0] == tracking_coordinates[-1][0]:
        print("se mueve en el eje y ")

        if tracking_coordinates[-1][1] < 0:
            print("me muevo haci alante")
        else:
            print("me muevo atras")


    else:
        print("se mueve en el eje x ")



"""Button Pressed Logic"""
def move_on_x():
    move_x = True
    check_x_list.append((move_x))



def move_on_y():
    move_x = False
    check_x_list.append((move_x))


def mouse_draw(x,y):

    if check_x_list[-1] == True:
        t.setx(x)
        tracking(t.pos())
    else:
        t.sety(y)
        tracking(t.pos())

def to_restart():
    global position_coordinates, tracking_coordinates
    t.clear()
    t.penup()
    t.goto(START_POSITION)
    t.pendown()
    position_coordinates=[(0,0)]
    tracking_coordinates=[START_POSITION]

"""##########################"""

# def mouse_draw(x, y):
#   global step
#
#   t.goto(x, y)
#   end_pos = (t.position())
#
#   print("the end pos is",end_pos)
#
#
#
#   result = ((end_pos[0]-start_pos[0]),(end_pos[1]-start_pos[1])) #vector
#   step += 1
#
#   path_dict = [{
#       "step": step,
#       "result": result }]  # Records Steps and result of each drawn line
#   path_list.append(path_dict[0])
#   print(path_list)
#   t.write(result)
#





"""Buttons"""
canvas = screen.getcanvas()
#Right
button_right = Button(canvas.master, text="Rotate Right", command=rotate_right,bg=GREY)
button_right.pack()
button_right.place(x=670, y=100)
#Left
button_left = Button(canvas.master, text="Rotate Left", command=rotate_left,bg=GREY)
button_left.pack()
button_left.place(x=670, y=150)

button_x = Button(canvas.master, text="X Axis", command=move_on_x, bg=GREY)
button_x.pack()
button_x.place(x=670, y=200)

button_y = Button(canvas.master, text="Y Axis", command=move_on_y, bg=GREY)
button_y.pack()
button_y.place(x=670, y=250)

button_restart = Button(canvas.master, text="RESTART", command=to_restart, bg=GREY,font=("Arial", 12, "bold"))
button_restart.pack()
button_restart.place(x=670, y=300)

screen.onclick(mouse_draw,btn=1)

screen.mainloop()
