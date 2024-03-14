import numpy as np
import matplotlib.pyplot as plt 
import mtcnn 
import time 
from PIL import Image 
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import base64
import io


detector = mtcnn.MTCNN() 
model = VGGFace(model='resnet50')


"""
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

def get_embeddings(filenames):
	# extract faces
	faces = [extract_face(f) for f in filenames]
	# convert into an array of samples
	samples = np.asarray(faces, 'float32')
	# prepare the face for the model, e.g. center pixels
	samples = preprocess_input(samples, version=2)
	# create a vggface model
	# perform prediction
	yhat = model.predict(samples)
	return yhat
"""

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

def get_embeddings_from_base64(base64_strings):
    # extract faces
    faces = [extract_face_from_base64(b) for b in base64_strings]
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
            print('>face is not a Match (%.3f <= %.3f)' % (score, thresh))
            return False  
        else:
            print('>face is a Match (%.3f > %.3f)' % (score, thresh))
            return True