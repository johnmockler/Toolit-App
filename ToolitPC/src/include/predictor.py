# make a prediction for a new image.
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

class Predictor():
    
    model_path = "models/final_model.h5"
        
    def __init__(self):
      
        self.model = load_model(self.model_path)
    
    def load_image(self, filename):
        # load the image
        img = load_img(filename, grayscale=True, target_size=(28, 28))
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 1 channel
        img = img.reshape(1, 28, 28, 1)
        # prepare pixel data
        img = img.astype('float32')
        img = img / 255.0
        return img

    def predict(self, image_path):

        image = self.load_image(image_path)
        output = self.model.predict_classes(image)
        return output[0]

