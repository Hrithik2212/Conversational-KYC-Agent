# main.py

from fastapi import FastAPI,HTTPException,WebSocket, WebSocketDisconnect , UploadFile, File
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
from pdf2image import convert_from_path
import numpy as np
import os
import mtcnn 
import base64 
from PIL import Image 
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input 
import matplotlib.pyplot as plt 
from sklearn.metrics.pairwise import cosine_similarity


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
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = FACIAL_LANDMARKS_IDXS["right_eye"]

last_blink_time = time.time()  # Track time of last detected blink
TOTAL = 0  # Blink counter

detector = mtcnn.MTCNN() 
model = VGGFace(model='resnet50')

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


def pdf_to_image(pdf_path, output_path, dpi=200):
    """
    Convert a PDF file to an image.

    Args:
        pdf_path (str): Path to the PDF file.
        output_path (str): Path to save the output image.
        dpi (int, optional): Resolution of the output image in dots per inch (DPI). Defaults to 200.
    """
    # Convert PDF to image
    images = convert_from_path(pdf_path, dpi=dpi)

    # Save images
    for i, image in enumerate(images):
        image.save(f"{output_path}_{i+1}.jpg", "JPEG")


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file.

    Args:
        file (UploadFile): Uploaded PDF file.

    Returns:
        dict: Response indicating successful upload.
    """
    # Check if the uploaded file is a PDF
    if file.filename.endswith(".pdf"):
        # Process the PDF file (e.g., save to disk, extract text, etc.)
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        
        pdf_to_image(file.filename , "aadhar" )
        os.remove(file.filename)
        return {"message": "PDF uploaded successfully." }
    else:
        return {"message": "Please upload a PDF file."}
    


def extract_face_from_base64(base64_string: str, required_size: tuple = (224, 224)):
    # Decode the base64 string into bytes
    image_data = base64.b64decode(base64_string)
    # Convert bytes to an image
    image = Image.open(io.BytesIO(image_data))
    
    # detect faces in the image
    pixels = np.array(image)
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = np.asarray(image)
    return face_array

def extract_face(file_name :str , required_size:tuple=(224, 224)):
   
    # detect faces in the image
    pixels = plt.imread(file_name)
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = np.asarray(image)
    return face_array


def get_embeddings(faces ):
	# extract faces
	# faces = [extract_face(f) for f in filenames]
	# convert into an array of samples
	samples = np.asarray(faces, 'float32')
	# prepare the face for the model, e.g. center pixels
	samples = preprocess_input(samples, version=2)
	# create a vggface model
	# perform prediction
	yhat = model.predict(samples)
	return yhat


def is_match(known_embedding, candidate_embedding, thresh=0.3)->bool:
        score = cosine_similarity(known_embedding.reshape(1,-1), candidate_embedding.reshape(1,-1))[0][0]
        if score <= thresh:
            print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
            return score , False  
        else:
            print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))
            return score , True 

@app.post("/verify-identity") 
def face_verification(base64_img : str ):
    face = extract_face("./full_face.jpg")# extract_face_from_base64(base64_img ) 
    aadhar = extract_face("./aadhar_1.jpg")
    yhat = get_embeddings(np.array([face , aadhar]))
    score , res = is_match(yhat[0] , yhat[1])
    if res : 
        return {"res":"true" ,  "message" : "verification swuccessful"} 
    else :
        return {"res" : "false" , "message" : "verification  failure"}