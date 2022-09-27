import numpy as np
import cv2


# capture the webcam
vid1 = cv2.VideoCapture(6)
vid2 = cv2.VideoCapture(0)



while True:  # while true, read the camera
    ret, frame = vid1.read()
    ret1, frame1 = vid2.read()
    

    if ret:
        cv2.imshow("cam0", frame)  # frame with name and variable of the camera
    if ret1:
        cv2.imshow("cam1", frame1)
       
    # to break the loop and terminate the program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid1.release()
vid2.release()
