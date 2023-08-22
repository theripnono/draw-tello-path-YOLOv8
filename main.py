from turtle import Turtle
from turtle import Screen
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from grid import Grid
import json, os
from tello import Fly



GREY = "#d3d3d3"
DARK_GREY = "#949494"
GREEN = "#b7d5ac"
START_POSITION = (-0, 0)  # Drone start position


"""Screen setup"""

BGPIC ="images/floorplans.gif"
DRON_ICON = "/images/drone_icon.png"

screen = Screen()
screen.setup(width=800, height=700)
screen.bgpic(BGPIC)

# Or, set the shape of a turtle

screen.title("DRAWING PATH")
now = datetime.now()

check_list = [False]
tracking_coordinates = [START_POSITION]
position_list = []

rotation = ""
fw_bw = ""
distance = 0

path_list = []

grid = False
show_grid = None
count_rotation = 0


"""Initializing start position"""
t = Turtle()
#t.shape(DRON_ICON)
t.pensize(width=4)
t.shapesize(2)
t.penup()
t.setheading(90)
t.goto(START_POSITION)

start_pos = t.position()
t.pendown()
"""######################"""

path = None

fly = Fly(path)

path_str = "path_commands"
date_time = now.strftime("%Y-%m-%d")
date_time = date_time.replace("-", "_")

def tracking(coordinates):
    global path_list, count_rotation

    """
    If the arrow rotate it means the drone will rotate so the cardinal axis change.
    Positive rotation count +1 when right click is pressed, negative count -1 when left click is pressed
    4 times rotating it means a complete rotation, so the axis are in the initial pos.
    """

    position_dict = {"motion": "", "distance": 0}
    tracking_coordinates.append(coordinates)
    distance = (tracking_coordinates[-1][0]) - (tracking_coordinates[-2][0]), (
                (tracking_coordinates[-1][1]) - (tracking_coordinates[-2][1]))

    if count_rotation == 0:  # standard cardinal axis position.
        if distance[0] == 0:  # I'm moving over y coordinate
            if distance[1] > 0:  # I'm moving Forward
                position_dict["motion"] = "forward"
                position_dict["distance"] = distance[1]
                path_list.append(position_dict)
            else:
                position_dict["motion"] = "backward"
                position_dict["distance"] = distance[1]
                path_list.append(position_dict)
        elif distance[0] != 0:
            if distance[0] > 0:  # I'm Moving left
                position_dict["motion"] = "right"
                position_dict["distance"] = distance[0]
                path_list.append(position_dict)
            else:
                position_dict["motion"] = "left"
                position_dict["distance"] = distance[0]
                path_list.append(position_dict)

    elif count_rotation == 1 or count_rotation == -3:

        """
        Cardinal axis have change it because the drone it has rotated
               -x 
                |
                |
        -y------------> y
                |
                |
                v
                x 
        """
        if distance[0] == 0:  # Now; Y axis is -X and so on
            if distance[1] > 0:
                position_dict["motion"] = "left"
                position_dict["distance"] = distance[1]
                path_list.append(position_dict)
            else:
                position_dict["motion"] = "right"
                position_dict["distance"] = distance[1]
                path_list.append(position_dict)

        elif distance[0] != 0:
            if distance[0] > 0:  # I'm Moving left
                position_dict["motion"] = "forward"
                position_dict["distance"] = distance[0]
                path_list.append(position_dict)
            else:
                position_dict["motion"] = "backward"
                position_dict["distance"] = distance[0]
                path_list.append(position_dict)

    elif count_rotation == 2 or count_rotation == -2:
        """
              -y 
                |
                |
        x <----------- x
                |
                |
                v
              y 
        """
        if distance[0] == 0:
            if distance[1] > 0:
                position_dict["motion"] = "backward"
                position_dict["distance"] = distance[1]
                path_list.append(position_dict)
            else:
                position_dict["motion"] = "forward"
                position_dict["distance"] = distance[1]
                path_list.append(position_dict)

        elif distance[0] != 0:
            if distance[0] > 0:
                position_dict["motion"] = "left"
                position_dict["distance"] = distance[0]
                path_list.append(position_dict)
            else:
                position_dict["motion"] = "right"
                position_dict["distance"] = distance[0]
                path_list.append(position_dict)

    elif count_rotation == 3 or count_rotation == -1:
        """
              x 
                ^
                |
                |
        y <----------- -y
                |
                |
                
              -x 
        """
        if distance[0] == 0:
            if distance[1] > 0:
                position_dict["motion"] = "right"
                position_dict["distance"] = distance[1]
                path_list.append(position_dict)
            else:
                position_dict["motion"] = "left"
                position_dict["distance"] = distance[1]
                path_list.append(position_dict)
        elif distance[0] != 0:
            if distance[0] > 0:
                position_dict["motion"] = "backward"
                position_dict["distance"] = distance[0]
                path_list.append(position_dict)
            else:
                position_dict["motion"] = "forward"
                position_dict["distance"] = distance[0]
                path_list.append(position_dict)


"""Button Logic"""
def move_on_x():
    global path_list
    move_x = True
    check_list.append(move_x)

    if check_list[-1]:
        button_x.config(bg=GREEN)
        button_y.config(bg=GREY)


def move_on_y():
    global path_list

    move_x = False
    check_list.append(move_x)

    if not check_list[-1]:
        button_y.config(bg=GREEN)
        button_x.config(bg=GREY)


def rotate_left():
    global count_rotation
    """
    It totates 90º the turtle head and store the rotation in a list.
    """
    if button_left:
        t.left(90)
        path_list.append({"motion": "rotate_left", "distance": 90})
        count_rotation -= 1
        if count_rotation < -3:
            count_rotation = 0
        return count_rotation


def rotate_right():
    global count_rotation
    """
    It totates 90º the turtle head and store the rotation in a list.
    """
    if button_right:
        t.right(90)
        path_list.append({"motion": "rotate_right", "distance": 90})

        count_rotation += 1
        if count_rotation > 3:
            count_rotation = 0
        return count_rotation


"""######################################"""


def mouse_draw(x, y):

    if check_list[-1]:
        t.setx(x)
        tracking(t.pos())

    else:
        t.sety(y)
        tracking(t.pos())


def to_restart():
    global position_dict, tracking_coordinates, path_list
    t.clear()
    t.penup()
    t.goto(START_POSITION)
    t.home()
    t.left(90)
    t.pendown()

    #Reset list and dict
    tracking_coordinates = [START_POSITION]
    path_list = []
    position_dict = {"motion": "", "distance": 0}


def make_grid():
    global grid, show_grid

    if not grid:
        button_create_grid.configure(bg=GREEN)
        show_grid = Grid()
        grid = True

    else:
        button_create_grid.configure(bg=DARK_GREY)
        show_grid.clear_grid()
        grid = False


def erase():
    global tracking_coordinates, path_list
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
        path_list = path_list[:-1]  # update the dictionary list discard the last dictionary
        t.pendown()
        t.pencolor("black")
    except IndexError:
        messagebox.showwarning(title="CAUTION!", message="You've not done more steps in memory")


def last_pos():
    global tracking_coordinates, path_list
    try:
        x = tracking_coordinates[-2][0]
        y = tracking_coordinates[-2][1]
        t.goto(x, y)
        tracking_coordinates.pop()
        path_list = path_list[:-1]  # update the dictionary list discard the last dictonard
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

        if moving[0] == 0 and moving[-1] > 0:  # moving on y positive axis
            if tracking_coordinates[-1][-1] > 0:  # checking if positive
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

        elif moving[1] == 0 and moving[0] > 0:  # moving on x positive axis
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

        elif moving[1] == 0 and moving[0] < 0:  # moving on x negative axis
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
    global path_list,tracking_coordinates
    path_list.append(tracking_coordinates[1:])
    yes_no_popup = messagebox.askyesno(title="Export Path", message="Do you want export the drawned path?")
    messagebox.showinfo(title="Your Path will be exported", message=f"{path_list}")



    if yes_no_popup:

        with open(f"{path_str}_{date_time}", "w") as path_file:
            json.dump(path_list, path_file)



def actualpos():
    global tracking_coordinates, path_list
    # messagebox.showinfo(title="Actual Position",message=f"{tracking_coordinates[-1]}")
    messagebox.showinfo(title="Travelled Coordinates", message=f"{tracking_coordinates}")


def to_fly():
    global path

    t.reset()
    t.hideturtle()
    filename = f"{path_str}_{date_time}"

    if not os.path.isfile(filename):
        messagebox.showinfo(title="REMEMBER!", message="Remember to export path before start flying")

    else:
        messagebox.showinfo(title="REMEMBER!", message="Connect to your drone")

        with open(filename, 'r') as json_file:
            path = json.loads(json_file.read())

        start_flying = True

        fly.start_flying(start_flying, path)


"""Buttons"""
canvas = screen.getcanvas()

button_create_grid = Button(canvas.master, text="SHOW GRID", command=make_grid, bg=DARK_GREY,
                            font=("Arial", 12, "bold"))
button_create_grid.pack()
button_create_grid.place(x=670, y=50)

# Right
button_right = Button(canvas.master, text="Rotate Right", command=rotate_right, bg=GREY)
button_right.pack()
button_right.place(x=670, y=100)
# Left
button_left = Button(canvas.master, text="Rotate Left", command=rotate_left, bg=GREY)
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

actual_pos = Button(canvas.master, text="Show Pos", command=actualpos, bg=DARK_GREY, font=("Arial", 12, "bold"))
actual_pos.pack()
actual_pos.place(x=670, y=370)

button_restart = Button(canvas.master, text="RESTART", command=to_restart, bg=DARK_GREY, font=("Arial", 12, "bold"))
button_restart.pack()
button_restart.place(x=670, y=450)

button_export_path = Button(canvas.master, text="SAVE PATH", command=to_export, bg=DARK_GREY, font=("Arial", 12, "bold"))
button_export_path.pack()
button_export_path.place(x=670, y=500)

start_flying = Button(canvas.master, text="START FLYING", command=to_fly, bg=DARK_GREY, font=("Arial", 12, "bold"))
start_flying.pack()
start_flying.place(x=650, y=550)

abort_mission = Button(canvas.master, text="EMERGENCY", command=fly.abort_mission, bg=DARK_GREY, font=("Arial", 12, "bold"))
abort_mission.pack()
abort_mission.place(x=350, y=620)

screen.onclick(mouse_draw, btn=1)

screen.mainloop()
