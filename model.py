###############################################################################
##                                  Model                                    ##
##                                                                           ##
##    Classify pictures based on ML model and return predictions as JSON     ##
##    (model defined in config section)                                      ##
##                                                                           ##
##    Two modes :                                                            ##
##                                                                           ##                 
##       'crawl' : Classify up to 5 images from 'data_path'                  ##
##                                                                           ##
##       'upload' : Classify one image uploaded as an argument               ##
##                                                                           ##
###############################################################################

import numpy as np
import pandas as pd
import json
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image


class Model:
    
    ######################
    ####### CONFIG #######
    ######################
    
    model = ResNet50(weights='imagenet')
    mode = ''
    data_path = 'pictures//'
    img_path = ''
    nb_pictures = 0
    
    ######################
    ###### SET MODE ######
    ######################
    
    def set_crawl(self):
        self.mode = 'crawl'
        self.nb_pictures = 5
        
    def set_upload(self, img_path):
        self.mode = 'upload'
        self.img_path = img_path
        self.nb_pictures = 1
    
    ######################
    ###### MODEL RUN #####
    ######################
    
    def run(self):
        results = pd.DataFrame(columns= ['img_path', 'predicted_class', 'predicted_confidence'])
        
        for i in range(self.nb_pictures):
            if self.mode == 'crawl':
                self.img_path = self.data_path + 'picture_' + str(i) +'.png'
  
            # From image to preprocessed array
            img = image.load_img(self.img_path, target_size=(224, 224))
            X = image.img_to_array(img)
            X = np.expand_dims(X, axis=0)
            X = preprocess_input(X)

            # Get model predictions
            predictions = self.model.predict(X)

            # Retrieve the top 1 class and confidence
            predictions = decode_predictions(predictions, top=1) 
            predicted_class = predictions[0][0][1] 
            predicted_confidence = predictions[0][0][2]
            
            # Append result to our dataframe
            results = results.append({'img_path': self.img_path, 'predicted_class': predicted_class, 'predicted_confidence': predicted_confidence}, ignore_index=True)
            
        return results.to_json()
