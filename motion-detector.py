"""
                                                   
   Name: Benedek Balazs (blasio99)                         
   Date: 2020, Fall                                
                                                   
          Motion detection and tracking            
             with Python and OpenCV                
                                                   
       Technical University of Cluj-Napoca         
    Faculty of Automation and Computer Science     
          Structure of Computer Systems            
            Group 30434 - Semigroup 1              


     _     _            _        ____   ____
    | |__ | | ___  ___ |_| ___  /    \ /    \ 
    |    \| |/__ \| __|| |/   \ \__'  |\__'  |
    |  .  | |  .  |__ || |  .  | __|  | __|  |
    \____/|_|\___/|___||_|\___/ |____/ |____/

    ------------------------------------------
                github.com/blasio99

"""


# import required librarires
from   cv2      import cv2
from   datetime import datetime

# variable
first_frame =  None

# capturing the video frames using webcam
video = cv2.VideoCapture (0, cv2.CAP_DSHOW)
# video = cv2.VideoCapture ('frozen.mp4')
# video = cv2.VideoCapture ('papaUT.mp4')
# having built-in functions, the camera will be opened
# '0' denotes the camera at the harware port number 0

print(" ____________________________________________________________________" )
print("|                                                                    |")
print("|   Motion detection and tracking using Python and OpenCV Contours   |")
print("|    ----------------------------------------------------------      |")
print("|   To exit the program, press the escape (Esc) or the 'Q' button.   |")
print("|____________________________________________________________________|")
print()

while True:
    check, color_frame = video.read()
    status = 0
    current_time = datetime.now()
    text = "... No detection ..."
    # converting the captured frame to gray-scale and applying Gaussian Blur to remove noise:
    gray_frame = cv2.cvtColor (color_frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur (gray_frame, (21, 21), 0)

    # capturing only the first gray frame
    if first_frame is None:
        first_frame = gray_frame
        continue

    # creating a delta frame and a threshold frame
    delta_frame     = cv2.absdiff (first_frame, gray_frame)
    threshold_frame = cv2.threshold (delta_frame, 25, 255, cv2.THRESH_BINARY)[1]

    #dilating the threshold frame and finding pixel contours in it
    threshold_frame = cv2.dilate (threshold_frame, None, iterations=3)
    (cnts,_) = cv2.findContours (threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    

    # finding the contour area and bounding the end points in a rectangle
    for contour in cnts:
        if cv2.contourArea (contour) < 2000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect (contour)
        cv2.rectangle (color_frame, (x,y), (x + w, y + h), (11, 255, 1), 3)
        text = "... Motion ..."
    # --------------------- for loop ends here -----------------------

    # drawing the text and the current time on the frame
    ct = current_time.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(color_frame, 'Detection: {}'.format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (25, 25, 255), 2)
    cv2.putText(color_frame, ct, (10,  color_frame.shape[0]  -  10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (25, 25, 255), 1)


    # displaying all 4 different frames
    cv2.imshow("Grey Frame"     , gray_frame)
    cv2.imshow("Delta Frame"    , delta_frame)
    cv2.imshow("Threshold Frame", threshold_frame)
    cv2.imshow("Color Frame"    , color_frame)

    key = cv2.waitKey (33)
    if key == 27 or key == ord ('q'):
        break
# ------------------- while True loop ends here ----------------------



video.release()
cv2.destroyAllWindows()

