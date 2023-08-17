from turtle import Turtle, Screen
import time,math
from djitellopy import Tello


"""
********************************** INFORMATION ************************************************************************
According to the drone's docs, the speed is 10 cm/s.

The given distance is in pixels, so we can create a conversion rate. For this case:

If the distance is 100 pixeles the given speed to the drone will be 50 cm/s. 

Each iteration will have a time.sleep(seg) to wait the other instruction be done.
So the drone will travelled and the following instruction will not be given. 

More than 7 seconds with no commands, lands the drone.

NOTE: the real scale between px and cm is: 1cm -> 37,78 px
*********************************************************************************************************************"""




# Given Path
example_path = [{"motion": "Forward", "distance": 200}, 'rotate_left',
                {"motion": "Left", "distance": -50}, 'rotate_right',
                {"motion": "Backward", "distance": 50},
                {"motion":"rotate_left", "rotation": -90}]



#tello = Tello()

ratio = 0.5  # This ratio can be change according your needs


def pixels_to_cm(distance_px):

    """ 100px = 50cm """

    distance_cm = math.ceil(distance_px * ratio)

    return distance_cm


def set_seconds(distance_cm):

    """moves 10cm in 1 seg"""

    seg = abs(math.ceil(distance_cm / 10))

    return seg


def path_to_commands(path):
    rotation_speed = 90
    fb, lr, yd = 0, 0, 0
    for item in path:
        if isinstance(item, dict):
            if item["motion"] == "Forward":
                fb = pixels_to_cm(item["distance"])
            elif item["motion"] == "Backward":
                fb = pixels_to_cm(item["distance"])

            elif item["motion"] == "Left":
                lr = pixels_to_cm(item["distance"])
            elif item["motion"] == "Right":
                lr = pixels_to_cm(item["distance"])

        elif isinstance(item, str):
            if item == "rotate_right":
                yd = rotation_speed
            elif item == "rotate_left":
                yd = -rotation_speed
        example_path.pop(0)
        return [fb, lr, yd]


def main():
    turtle = Turtle()
    turtle.shapesize(2)
    turtle.left(90)

    screen = Screen()
    screen.setup(width=800, height=700)
    screen.tracer(0)

    #tello.connect()
    #tello.takeoff()

    in_flying = True

    while in_flying:

        try:
            values = path_to_commands(example_path)
            print(values[0], values[1], values[2])
            #tello.send_rc_control(forward_backward_velocity=values[0], left_right_velocity=values[1],
            #                      yaw_velocity=values[2], up_down_velocity=0)
            time.sleep(2)

            screen.update()

        except TypeError:
            pass
            #tello.land()

    screen.exitonclick()


main()
