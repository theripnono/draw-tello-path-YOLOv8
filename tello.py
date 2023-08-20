import turtle
from turtle import Turtle, Screen
from djitellopy import Tello
from time import sleep
from threading import Thread

"""
********************************** INFORMATION ************************************************************************
According to the drone's docs, the speed is 15 cm/s.

The made distance in is in pixels, so we need to create a conversion rate. 

Each iteration will have a time.sleep(seg) to wait the instruction be done.

*********************************************************************************************************************"""

# Given Path
example_path = [{"motion": "forward", "distance": 184.0},
                {"motion": "rotate_right", "distance": 90},
                {"motion": "backward", "distance": -186.0},
                {"motion": "rotate_right", "distance": 90},
                {"motion": "forward", "distance": -323.0},

                [[0, 184.0], [-186.0, 184.0], [-186.0, -139.0]]
                ]

tello = Tello()


def draw_turtle(coordinates_list):

    coordinates_list = coordinates_list[-1]

    for l in coordinates_list:
        x = l[0]
        y = l[1]
        coordinates_list.pop(0)
        return x, y



def to_travel(dist_px):

    """
    speed = 15cm/s
    1px -> 1 cm si le mando 100px me devolverá 50 cm
    speed = 20cm -> 1s

    return the seconds that  will be used to know the time interval between commands.

    """

    if dist_px < 0:

        cm = abs(dist_px)

    elif dist_px > 500:

        cm = 500
    else:
        cm = dist_px

    return round((cm / 15), 2)


def path_to_commands(path):

    speed = 20

    turtle.shapesize(2)
    turtle.left(90)

    path = example_path[:-1]

    for item in path:

        if item["motion"] == "forward":

            seconds = to_travel(item["distance"])

            #tello.send_rc_control(0, speed, 0, 0)

            print("SENCONDS: ############", seconds)
            sleep(seconds)

        elif item["motion"] == "backward":

            seconds = to_travel(item["distance"])

            #tello.send_rc_control(0, -speed, 0, 0)

            print("SENCONDS: ############", seconds)
            sleep(seconds)

        elif item["motion"] == "left":

            seconds = to_travel(item["distance"])

            #tello.send_rc_control(speed, 0, 0, 0)

            print("SENCONDS: ############", seconds)
            sleep(seconds)

        elif item["motion"] == "right":

            seconds = to_travel(item["distance"])

            #tello.send_rc_control(-speed, 0, 0, 0)

            print("SENCONDS: ############", seconds)
            sleep(seconds)

        elif item["motion"] == "rotate_right":

            yw = 90
            seconds = 1

            #tello.send_rc_control(0, 0, 0, yw)

            print("SENCONDS: ############", seconds)
            turtle.right(90)
            sleep(seconds)

        elif item["motion"] == "rotate_left":

            yw = 90
            seconds = 1

            #tello.send_rc_control(0, 0, 0, yw)
            print("SENCONDS: ############", seconds)
            turtle.left(90)
            sleep(seconds)  # As it is in other thread it keeps flying

        #tello.send_rc_control(0, 0, 0, 0)

        try:

            x, y = draw_turtle(example_path)
            turtle.goto(x, y)
        except TypeError:
            pass
        
    print("LAND")

    #tello.land()

def main():
    screen = Screen()
    screen.setup(width=800, height=700)

    # screen.tracer(0)

    #tello.connect()
    #tello.takeoff()

    path_to_commands(example_path)

    screen.exitonclick()


main()
#tello.land()
