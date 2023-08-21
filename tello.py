import cv2
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


class Fly(Turtle):

    def __init__(self, exported_path):
        super().__init__()

        #self.Screen()
        #self.setup(width=800, height=700)
        self.shapesize(2)
        self.left(90)


        # Given Path
        #self.tello = Tello()
        #self.tello.connect()


        # recorder = Thread(target=video_recorder, daemon=True)
        # recorder.start()

        self.path = exported_path

        self.path_to_commands(self.path)

    def draw_turtle(self, coordinates_list):

        coordinates_list = coordinates_list[-1]

        for l in coordinates_list:
            x = l[0]
            y = l[1]
            coordinates_list.pop(0)
            return x, y


    def to_travel(self, dist_px):
        """
        speed = 15cm/s
        1px -> 1 cm si le mando 100px me devolverá 50 cm
        speed = 20cm -> 1s

        return the seconds that  will be used to know the time interval between commands.

    """

        if dist_px < 0:

            cm = abs(dist_px)

        elif dist_px > 100:  # I put this max value because testing at home. Outside max value = 500

            cm = 100

        else:
            cm = dist_px

        return round((cm / 15), 2)


    def path_to_commands(self,full_path):

        #self.tello.takeoff()

        speed = 20

        path = full_path[:-1]

        for item in path:

            if item["motion"] == "forward":

                seconds = self.to_travel(item["distance"])

                # self.tello.send_rc_control(0, speed, 0, 0)

                print("SENCONDS: ############", seconds)
                sleep(seconds)

            elif item["motion"] == "backward":

                seconds = self.to_travel(item["distance"])

                # self.tello.send_rc_control(0, -speed, 0, 0)

                print("SENCONDS: ############", seconds)
                sleep(seconds)

            elif item["motion"] == "left":

                seconds = self.to_travel(item["distance"])

                # self.tello.send_rc_control(speed, 0, 0, 0)

                print("SENCONDS: ############", seconds)
                sleep(seconds)

            elif item["motion"] == "right":

                seconds = self.to_travel(item["distance"])

                # self.tello.send_rc_control(-speed, 0, 0, 0)

                print("SENCONDS: ############", seconds)
                sleep(seconds)

            elif item["motion"] == "rotate_right":

                yw = 90
                seconds = 1

                # self.tello.send_rc_control(0, 0, 0, yw)

                print("SENCONDS: ############", seconds)
                self.right(90)
                sleep(seconds)

            elif item["motion"] == "rotate_left":

                yw = 90
                seconds = 1

                # tello.send_rc_control(0, 0, 0, yw)
                print("SENCONDS: ############", seconds)
                self.left(90)
                sleep(seconds)  # As it is in other thread it keeps flying

            # tello.send_rc_control(0, 0, 0, 0)

            try:

                x, y = self.draw_turtle(self.path)
                self.goto(x, y)
            except TypeError:
                pass

        print("*************** LAND ********************")

        #self.tello.land()
        #self.tello.streamoff()
        #self.exitonclick()

    def video_recorder(self):

        keep_recording = True

        #self.tello.streamon()

        while keep_recording:

            frame_read = self.tello.get_frame_read().frame
            frame_read = cv2.resize(frame_read, (640, 640))

            cv2.imshow("drone", frame_read)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break









