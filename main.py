from turtle import Turtle
from turtle import Screen
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from grid import Grid
import json


GREY="#d3d3d3"
DARK_GREY = "#949494"
GREEN ="#b7d5ac"
START_POSITION = (-0,0) #Drone start position
screen = Screen()
screen.setup(width=800, height=700)
screen.title("DRAWING PATH")
now = datetime.now()

check_list=[False]
tracking_coordinates = [START_POSITION]
position_list = []

rotation = ""
fw_bw = ""
distance = 0

path_list = []

grid = False
show_grid = None



def rotate_left():

    """
    It totates 90º the turtle head and store the rotations in a list.
    :return: list with the rotation
    """

    t.left(90)
    path_list.append("Rotate Left")

def rotate_right():

    """
    It totates 90º the turtle head and store the rotations in a list.
    :return: list with the rotation
    """
    t.right(90)
    path_list.append("Rotate Right")




"""Initializing start position"""
t = Turtle()

t.pensize(width=4)
t.shapesize(2)
t.penup()
t.setheading(90)
t.goto(START_POSITION)

start_pos = t.position()
t.pendown()
"""######################"""

def tracking(coordinates):
    global path_list

    position_dict = {"motion":"","distance":0}
    tracking_coordinates.append(coordinates)
    distance = ((tracking_coordinates[-1][0]))-(tracking_coordinates[-2][0]) , ((tracking_coordinates[-1][1])-(tracking_coordinates[-2][1]))

    if distance[0] == 0: #I'm moving over y coordinate
        if distance[1] > 0: # I'm moving Forward
            position_dict["motion"] = "Forward"
            position_dict["distance"] = distance[1]
            path_list.append(position_dict)
        else:
            position_dict["motion"] = "Backward"
            position_dict["distance"] = distance[1]
            path_list.append(position_dict)
    else:
        if distance[0] > 0: #I'm Moving left
            position_dict["motion"] = "Left"
            position_dict["distance"] = distance[0]
            path_list.append(position_dict)

        else:
            position_dict["motion"] = "Right"
            position_dict["distance"] = distance[0]
            path_list.append(position_dict)


"""Button Pressed Logic"""
def move_on_x():

    move_x = True
    check_list.append((move_x))

    if check_list[-1]:
        button_x.config(bg=GREEN)
        button_y.config(bg=GREY)

def move_on_y():

    move_x = False
    check_list.append((move_x))

    if not check_list[-1]:
        button_y.config(bg=GREEN)
        button_x.config(bg=GREY)

"""######################################"""
def mouse_draw(x,y):

    if check_list[-1] == True:
        t.setx(x)
        tracking(t.pos())

    else:
        t.sety(y)
        tracking(t.pos())

def to_restart():
    global position_dict, tracking_coordinates,path_list
    t.clear()
    t.penup()
    t.goto(START_POSITION)
    t.pendown()

    tracking_coordinates=[START_POSITION]
    path_list = []
    position_dict = {"motion": "", "distance": 0}
def make_grid():
    global grid, show_grid

    if not grid:
        button_create_grid.configure(bg=GREEN)
        show_grid=Grid()
        grid = True

    else:
        button_create_grid.configure(bg=DARK_GREY)
        show_grid.clear_grid()
        grid = False

def movement_mark(coordinate_list):


    from_pos = tracking_coordinates[-2]
    to_pos = tracking_coordinates[-1]
    moving = to_pos - from_pos

    if moving[0] == 0 and moving[-1]<0:
        mark = "negative"
     #moving on y positive axis
        mark = "positive"
    elif moving[1] == 0 and moving[-0]<0:
        mark = "negative"   #moving on x negative axis
    elif moving[1] == 0 and moving[-0]>0: #moving on x positive axis
        mark = "positive"
    print(moving)
    return mark

def erase():
    global tracking_coordinates
    """
    Erase the drawn line
    """
    try:
        x = tracking_coordinates[-2][0]
        y = tracking_coordinates[-2][1]
        t.pendown()
        t.pencolor("white")
        t.goto(x, y)
        tracking_coordinates.pop()
        t.pendown()
        t.pencolor("black")
    except IndexError:
        messagebox.showwarning(title="CAUTION!", message="You've not done more steps in memory")
def last_pos():
    global tracking_coordinates
    try:
        x = tracking_coordinates[-2][0]
        y = tracking_coordinates[-2][1]
        t.goto(x, y)
        tracking_coordinates.pop()
        t.pendown()
    except IndexError:
        messagebox.showwarning(title="CAUTION!", message="You've not done more steps in memory")
def undo():
    global tracking_coordinates, check_list

    try:
        tracking_coordinates = tracking_coordinates
        from_pos = tracking_coordinates[-2]
        to_pos = tracking_coordinates[-1]
        moving = to_pos - from_pos

        if moving[0] == 0 and moving[-1] > 0 :  # moving on y positive axis
            if tracking_coordinates[-1][-1] > 0: #checking if positive
                if tracking_coordinates[-2][-1] < tracking_coordinates[-1][-1]:
                   erase()
                else:
                    last_pos()
            else:
                if tracking_coordinates[-2][-1] > tracking_coordinates[-1][-1]:
                    erase()
                else:
                    last_pos()

        elif moving[0] == 0 and moving[-1] < 0:  # moving on y negative axis
            if tracking_coordinates[-1][-1] < 0:  # checking if negative
                if tracking_coordinates[-2][-1] > tracking_coordinates[-1][-1]:
                    erase()
                else:
                    last_pos()
            else:
                if tracking_coordinates[-2][-1] > tracking_coordinates[-1][-1]:
                    last_pos()

                else:
                    erase()

        elif moving[1] == 0 and moving[0] > 0: # moving on x positive axis
            if tracking_coordinates[-1][0] > 0:  # checking if positive
                if tracking_coordinates[-2][0] < tracking_coordinates[-1][0]:
                    erase()
                else:
                    last_pos()
            else:
                if tracking_coordinates[-2][0] > tracking_coordinates[-1][0]:
                    erase()
                else:
                    last_pos()

        elif moving[1] == 0 and moving[0] < 0: # moving on x negative axis
            if tracking_coordinates[-1][0] < 0:  # checking if negative
                if tracking_coordinates[-2][0] > tracking_coordinates[-1][0]:
                    erase()
                else:
                    last_pos()
            else:
                if tracking_coordinates[-2][0] > tracking_coordinates[-1][0]:
                    last_pos()

                else:
                    erase()


    except IndexError:
        messagebox.showwarning(title="CAUTION!", message="You've not done more steps in memory")

def to_export():
    global path_list
    yes_no_popup = messagebox.askyesno(title="Export Path", message="Do you want export the drawn path?")
    messagebox.showinfo(title="Your Path will be exported", message=f"{path_list}")

    date_time = now.strftime("%Y-%m-%d")
    date_time = date_time.replace("-","_")
    if yes_no_popup:
        with open(f"path_list_{date_time}" ,"w") as path_file:
            json.dump(path_list,path_file)

def actualpos():
    global tracking_coordinates
    # messagebox.showinfo(title="Actual Position",message=f"{tracking_coordinates[-1]}")
    tracking_coordinates = tracking_coordinates
    from_pos = tracking_coordinates[-2]
    to_pos = tracking_coordinates[-1]
    moving = to_pos - from_pos
    print(moving)
    print(tracking_coordinates)


"""Buttons"""
canvas = screen.getcanvas()

button_create_grid = Button(canvas.master, text="SHOW GRID", command=make_grid, bg=DARK_GREY,font=("Arial", 12, "bold"))
button_create_grid.pack()
button_create_grid.place(x=670, y=50)


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

button_y = Button(canvas.master, text="Y Axis", command=move_on_y, bg=GREEN)
button_y.pack()
button_y.place(x=670, y=250)

button_undo = Button(canvas.master, text="Undo", command=undo, bg=GREY)
button_undo.pack()
button_undo.place(x=670, y=300)


button_restart = Button(canvas.master, text="RESTART", command=to_restart, bg=DARK_GREY,font=("Arial", 12, "bold"))
button_restart.pack()
button_restart.place(x=670, y=450)

button_export_path = Button(canvas.master, text="EXPORT", command=to_export, bg=DARK_GREY,font=("Arial", 12, "bold"))
button_export_path.pack()
button_export_path.place(x=670, y=500)

actual_pos= Button(canvas.master, text="Show Pos", command=actualpos, bg=DARK_GREY,font=("Arial", 12, "bold"))
actual_pos.pack()
actual_pos.place(x=670, y=370)


screen.onclick(mouse_draw,btn=1)

screen.mainloop()
