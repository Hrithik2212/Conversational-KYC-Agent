import numpy as np
import matplotlib.pyplot as plt 
import mtcnn 
import time 
from PIL import Image 
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import Normalizer
import pickle 
# from FaceNet.architecture import * 

confidence_t=0.99
recognition_t=0.5
required_size = (160,160)
l2_normalizer = Normalizer("l2")
# face_encoder = InceptionResNetV2()
path_m = "FaceNet/facenet_keras_weights.h5"
# face_encoder.load_weights(path_m)



model = VGGFace(model='resnet50')




face_img = "obama.jpeg"
aadhar_image = "aadhar.jpg"
detector = mtcnn.MTCNN() 

# def cosine_similarity(vec1, vec2):
#     dot_product = np.dot(vec1, vec2)
#     norm_vec1 = np.linalg.norm(vec1)
#     norm_vec2 = np.linalg.norm(vec2)
#     return dot_product / (norm_vec1 * norm_vec2)

def detect_faces(img : np.array ) : 
    res = detector.detect_faces(img) 
    return res 

def plot_face_box(img:np.array , save_path : str ):
    res = detect_faces(img) 
    x1, y1, width, height = res[0]['box']
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    # plt.imshow(face)
    plt.axis('off') 
    plt.imsave(save_path , face)
    # plt.show()

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

def is_match(known_embedding, candidate_embedding, thresh=0.3)->bool:
        score = cosine_similarity(known_embedding.reshape(1,-1), candidate_embedding.reshape(1,-1))[0][0]
        if score <= thresh:
            print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
            return True 
        else:
            print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))
            return False
            
def is_match1(known_embedding, candidate_embedding, thresh=0.5) -> bool:
    # Normalize embeddings
    known_embedding = known_embedding / np.linalg.norm(known_embedding)
    candidate_embedding = candidate_embedding / np.linalg.norm(candidate_embedding)
    
    score = cosine_similarity(known_embedding.reshape(1, -1), candidate_embedding.reshape(1, -1))[0][0]
    if score >= thresh:
        print('>face is a Match (%.3f >= %.3f)' % (score, thresh))
        return True
    else:
        print('>face is NOT a Match (%.3f < %.3f)' % (score, thresh))
        return False
########################################################################################################################3
    

def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)


def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / std

def get_encode(face_encoder, face, size):
    face = normalize(face)
    face = Image.fromarray(face)
    face.resize(size)
    face = np.asarray(face)
    encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
    return encode


def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict



def main() : 
    
    face = plt.imread(face_img)
    aadhar = plt.imread(aadhar_image)
    print(aadhar.shape)
    # plt.imsave("aadhar.jpg" , aadhar)
    plot_face_box(face , "test1.jpg")
    plot_face_box(aadhar , "test2.jpg")
    start_time = time.time()

    filenames = [face_img , aadhar_image]
    yhat = get_embeddings(filenames) 
    # print(f"Shape : {yhat.shape}")
    is_match(yhat[0] , yhat[1])
    print(yhat[0])
    print(yhat[1])

    end_time = time.time()

    duration = end_time - start_time  # Time in seconds
    # print(res)
    print(f"Time taken: {duration} seconds")



if __name__ == "__main__" : 
    main()
