import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
from anti_spoof_test import return_model

model = return_model()
# Load the model
model_path = 'spoof_detection_model.hdf5'
model.load_weights(model_path)

# Function to preprocess the frame
def preprocess_frame(frame):
    frame = cv2.resize(frame, (224, 224))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.expand_dims(frame, axis=0)
    frame = preprocess_input(frame)
    return frame

# Function to predict on a frame
def predict_frame(frame, model):
    frame = preprocess_frame(frame)
    prediction = model.predict(frame)
    return prediction[0]

def main() :
    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Make prediction
        prediction = predict_frame(frame, model)

        # Display the frame
        cv2.putText(frame, f"Predicted class: {prediction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()
