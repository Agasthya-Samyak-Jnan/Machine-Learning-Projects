# Dependencies
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Lambda
from tensorflow.keras.models import Model, load_model

def build_siamese(input_shape=(512,512,1)):
    # Shared CNN Encoder
    input_layer = Input(shape=input_shape)
    x = Conv2D(64, (3,3), activation='relu')(input_layer)
    x = MaxPooling2D()(x)
    x = Conv2D(128, (3,3), activation='relu')(x)
    x = MaxPooling2D()(x)
    x = Conv2D(256, (3,3), activation='relu')(x)
    x = MaxPooling2D()(x)
    x = Flatten()(x)
    embedding = Dense(256, activation='relu')(x)

    encoder = Model(input_layer, embedding)

    # Siamese inputs
    input_A = Input(shape=input_shape)
    input_B = Input(shape=input_shape)

    emb_A = encoder(input_A)
    emb_B = encoder(input_B)

    distance = Lambda(lambda t: tf.abs(t[0] - t[1]), output_shape=(256,))([emb_A, emb_B])

    output = Dense(1, activation='sigmoid')(distance)

    model = Model([input_A, input_B], output)
    return model


IMAGE_X = 512
IMAGE_Y = 512
loaded_model = build_siamese()
loaded_model.load_weights("model.h5")

# Defining Required Preprocessing per Image

def preprocess (img) :
  
  img = np.array(img)
  img = tf.convert_to_tensor(img, dtype=tf.uint8)
  img = tf.image.crop_to_bounding_box(img, offset_height=800, offset_width=100, target_height=2200, target_width=2300) # cut out unwanted parts of image
  img = tf.image.rgb_to_grayscale(img) # convert to grayscale (color not needed)
  img = tf.image.resize(img, [IMAGE_X, IMAGE_Y]) # Resize (to save memory)
  img = tf.cast(img, tf.float32) / 255.0 # normalize (to keep values with 0.0-1.0)
  img = tf.clip_by_value(img, 0.0, 1.0) # clip values (to ensure they are in 0.0-1.0)
  return img

# Model Definition
# Siamese CNN Model Object Class
class SiameseCNN :
  def __init__(self, input_shape):
    self.input_shape = input_shape
    self.model = self.build()
    self.model.compile(optimizer=tf.keras.optimizers.Adam(),loss='binary_crossentropy',metrics=['accuracy'])

  def build (self) :
    # Shared CNN Encoder
    input_layer = Input(shape=self.input_shape)
    conv1 = Conv2D(64, (3,3), activation='relu')(input_layer)
    pool1 = MaxPooling2D()(conv1)
    conv2 = Conv2D(128, (3,3), activation='relu')(pool1)
    pool2 = MaxPooling2D()(conv2)
    conv3 = Conv2D(256, (3,3), activation='relu')(pool2)
    pool3 = MaxPooling2D()(conv3)
    flat_layer = Flatten()(pool3)
    output_layer = Dense(256, activation='relu')(flat_layer)
    CNNencoder = Model(input_layer,output_layer)

    # Siamese Architecture
    input_A = Input(shape=self.input_shape)
    input_B = Input(shape=self.input_shape)
    encoder_A = CNNencoder(input_A) # Get embeddings for first input image
    encoder_B = CNNencoder(input_B) # Get embeddings for second input image
    distance = Lambda(lambda tensors: tf.abs(tensors[0]-tensors[1]))([encoder_A,encoder_B]) # Compute distance (L1) between embeddings
    output = Dense(1, activation='sigmoid')(distance) # Classwise probability output
    siamese_model = Model(inputs=[input_A,input_B],outputs=output)

    return siamese_model

  # Train the model on Training Data
  def fit (self, train_generator, val_generator, epochs) :
    return self.model.fit(train_generator, validation_data=val_generator, epochs=epochs)

  # Predict output for Input Pair of Images
  def predict (self, X) :
    return self.model.predict(X)

  def summary (self) :
    self.model.summary()

  def save (self, filename) :
    self.model.save(filename)

# Load model and weights and predict
def predict (img1, img2) :

    processed_img1 = tf.expand_dims(preprocess(img1), axis=0)   # → (1,512,512,1)
    processed_img2 = tf.expand_dims(preprocess(img2), axis=0)

    score = loaded_model.predict([processed_img1,processed_img2])

    print(score)

    return "Same Writer" if score > 0.5 else "Different Writers"


