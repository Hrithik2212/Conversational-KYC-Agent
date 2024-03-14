import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Input, Flatten, SeparableConv2D
from tensorflow.keras.layers import GlobalAveragePooling2D, BatchNormalization, Concatenate
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.models import Sequential, Model

img_width = 224
img_height = 224


def return_model():
    pretrain_net = mobilenet_v2.MobileNetV2(input_shape = (img_width, img_height, 3),
                                            include_top = False,
                                            weights = 'imagenet')

    # load_param_path = '../input/mobilenet_v2/xception_weights_tf_dim_ordering_tf_kernels_notop.h5'  # Offline alternative
    # pretrain_net.load_weights(load_param_path)  # Manually load the weights from the input directory

    # ------ Freezing layer(s) up to a specific layer ------
    freeze_before = None  #"block_16_expand"  # use None to train, use "all" to freeze all the layers

    if freeze_before:
        for layer in pretrain_net.layers:
            if layer.name == freeze_before:
                break
            else:
                layer.trainable = False


    x = pretrain_net.output
    x = Conv2D(32, (3, 3), activation='relu')(x)
    x = Dropout(rate=0.2, name='extra_dropout1')(x)
    x = GlobalAveragePooling2D()(x)
    # x = Dense(units=128, activation='relu', name='extra_fc1')(x)
    # x = Dropout(rate=0.2, name='extra_dropout1')(x)
    x = Dense(1, activation='sigmoid', name='classifier')(x)

    model = Model(inputs=pretrain_net.input, outputs=x, name='mobilenetv2_spoof')
    print(model.summary())
    return model 

def main() : 
    model = return_model()

    # Path to the saved model
    model_path = 'spoof_detection_model.hdf5'
    # Load the modelUnitTest/AntiSpoofDetection/spoof_detection_model.hdf5

    model.load_weights(model_path)
    # Path to the image you want to predict on
    image_path = 'spoof_1001.png'

    # Load and preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet.preprocess_input(img_array)  # Assuming ResNet preprocessing

    # Make predictions
    predictions = model.predict(img_array)

    # Assuming the model predicts classes (change as needed)
    predicted_class = predictions[0]
    print(f"Predicted class: {predicted_class}")

if __name__ == "__main__" : 
    main() 
