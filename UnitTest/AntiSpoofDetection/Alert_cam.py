# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
# Define constants
EYE_AR_THRESH = 0.2  # Eye aspect ratio threshold
EYE_AR_CONSEC_FRAMES = 3  # Minimum consecutive frames for blink detection
NO_BLINK_ALERT_THRESHOLD = 10  # Seconds without blinking to trigger alert
FONT_SCALE = 0.7
FONT_THICKNESS = 2
TOTAL = 0 

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear


# Load facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Define facial landmark indices for eyes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Start video stream (modify for file or live stream)
# vs = FileVideoStream(args["video"]).start()  # for file video
vs = FileVideoStream("Video6.wmv").start()
fileStream = True  # for file video
vs = VideoStream(src=0).start()  # FOR LIVE STREAM (uncomment for live stream)
fileStream = False  # use FOR LIVE STREAM (set to True for live stream)
time.sleep(2.0)  # Allow time for camera warmup

# Initialize variables
last_blink_time = time.time()  # Track time of last detected blink

# Loop over frames from the video stream
while True:
    # Check if stream has ended (for file video)
    if fileStream and not vs.more():
        break

    # Read frame, resize, and convert to grayscale
    frame = vs.read()
    (h, w, c) = frame.shape
    frame = cv2.resize(frame, (700, h))  # Resize for better visibility
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # Loop over the face detections
    for rect in rects:
        # Detect facial landmarks for the face region
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Extract left and right eye coordinates, compute eye aspect ratio
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # Check for blink based on eye aspect ratio and consecutive frames
        if ear < EYE_AR_THRESH:
            last_blink_time = time.time()  # Update last blink time
            TOTAL +=1 
        else:
            elapsed_time = time.time() - last_blink_time
            if elapsed_time >= NO_BLINK_ALERT_THRESHOLD:
                print("[ALERT] No blinking detected for", NO_BLINK_ALERT_THRESHOLD, "seconds!")
                # Optionally add visual or audio alert here (e.g., play a sound)
                last_blink_time = time.time()  # Reset last blink time after alert

        # Draw eye contours and blink count/EAR
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),  # Removed as TOTAL is not defined
                    cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, (0, 0, 255), FONT_THICKNESS)
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):        
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
