import numpy as np
import numpy as np
import os
import h5py
from django.conf import settings

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from scipy import spatial


class VGGModel():
    def __init__(self):
        # weights: 'imagenet'
        # pooling: 'max' or 'avg'
        # input_shape: (width, height, 3), width and height should >= 48
        self.input_shape = (224, 224, 3)
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model = VGG16(weights = self.weight, input_shape = (self.input_shape[0], self.input_shape[1], self.input_shape[2]), pooling = self.pooling, include_top = False)
        self.model.predict(np.zeros((1, 224, 224 )))

    '''
    Use vgg16 model to extract features
    Output normalized feature vector
    '''
    def extract_feat(self, img_path):
        img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        feat = self.model.predict(img)
        norm_feat = feat[0]/np.linalg.norm(feat[0])
        return norm_feat
    

    def extract_all_features(self):
        root_path = os.path.join(settings.STATIC_ROOT, 'msrcorid')
        feats = []
        self.names = []
        for dirpath, _, filenames in os.walk(root_path):
            for file in filenames:
                if file.lower().endswith(('png', 'jpg', 'jpeg')):
                    path = os.path.join(dirpath, file)
                    self.names.append(path)
                    feats.append(self.extract_feat(path))
        self.feats = np.array(feats)


    def make_h5f_file(self, file_name="VGG16Features.h5"):
        file = os.path.join(settings.STATIC_URL, file_name) # TODO static path
        h5f = h5py.File(file, 'w')
        h5f.create_dataset('dataset_1', data=self.feats)
        h5f.create_dataset('dataset_2', data=np.bytes_(self.names))
        h5f.close()

    
    def read_h5f_file(self):
        file = os.path.join(settings.STATIC_URL, "VGG16Features.h5") # TODO static path
        h5f = h5py.File(file,'r')
        self.feats = h5f['dataset_1'][:]
        self.names = h5f['dataset_2'][:]
        h5f.close()


    def calculate_similarity(self, input_img_feat):
        scores = []
        for i in range(self.feats.shape[0]):
            score = 1-spatial.distance.cosine(input_img_feat, self.feats[i])
            scores.append(score)
        scores = np.array(scores)   
        return scores
    

    def match_images(self, scores, top_n=10):
        indices = np.argsort(scores)[::-1][:top_n]
        matched_images = []
        for idx in indices:
            matched_images.append(self.names[idx].decode('utf-8')[43:])

        return matched_images
    