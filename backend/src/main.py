# main.py

from fastapi import FastAPI,HTTPException,WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
import time
import dlib
import cv2
from imutils.video import VideoStream
from imutils.face_utils import FACIAL_LANDMARKS_IDXS
from scipy.spatial import distance as dist
from imutils import face_utils


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

EYE_AR_THRESH = 0.2  # Eye aspect ratio threshold
EYE_AR_CONSEC_FRAMES = 3  # Minimum consecutive frames for blink detection
NO_BLINK_ALERT_THRESHOLD = 10  # Seconds without blinking to trigger alert
FONT_SCALE = 0.7
FONT_THICKNESS = 2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = FACIAL_LANDMARKS_IDXS["right_eye"]

last_blink_time = time.time()  # Track time of last detected blink
TOTAL = 0  # Blink counter

@app.get("/getquestions")
async def getQuestions():
    try:
        questions=[{"label":"name","question":"What is your name?","speak":"Spell your name out if your name id raj spell it as R A J"},
                    {"label":"email","question":"What is your email?","speak":"Spell your name out if your name id raj spell it as R A J"},
                   ]
        return {"questions": questions}
    except:
        raise  HTTPException(status_code=400,detail="Invalid Mode type")
    

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

@app.websocket("/blink-detection")
async def blink_detection(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data is None:
                break

            # Decode base64 image
            image_bytes = base64.b64decode(data.encode('utf-8'))
            image_stream = io.BytesIO(image_bytes)
            frame = cv2.imdecode(np.frombuffer(image_stream.getvalue(), np.uint8), cv2.IMREAD_COLOR)

            # Resize for better visibility (optional)
            (h, w, c) = frame.shape
            frame = cv2.resize(frame, (700, h))

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            rects = detector(gray, 0)

            # Process each detected face
            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # Extract eye coordinates and compute EAR
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0

                # Check for blink and update counters
                if ear < EYE_AR_THRESH:
                    last_blink_time = time.time()
                    TOTAL += 1
                else:
                    elapsed_time = time.time() - last_blink_time
                    if elapsed_time >= NO_BLINK_ALERT_THRESHOLD:
                        print("[ALERT] No blinking detected for", NO_BLINK_ALERT_THRESHOLD, "seconds!")
                        # Optionally send an alert message through the websocket (e.g., using JSON)
                        alert_message = {"type": "alert", "message": "No blinking detected for a prolonged period!"}
                        await websocket.send_json(alert_message)
                        last_blink_time = time.time()
    except : 
        print("An error occured")
