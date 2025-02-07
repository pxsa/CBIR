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
        self.model = VGG16(weights=self.weight, input_shape=self.input_shape, pooling=self.pooling, include_top=False)

        # Corrected input shape to include the channel dimension
        self.model.predict(np.zeros((1, 224, 224, 3)))

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
        root_path = os.path.join(settings.STATICFILES_DIRS[0], 'msrcorid')
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
        full_file_name = os.path.join('model', file_name)
        file = os.path.join(settings.STATICFILES_DIRS[0], full_file_name) # TODO static path
        h5f = h5py.File(file, 'w')
        if h5f is None:
            print('NOT FOUNDED!')
        h5f.create_dataset('dataset_1', data=self.feats)
        h5f.create_dataset('dataset_2', data=np.bytes_(self.names))
        h5f.close()

    
    def read_h5f_file(self):
        file_name = "VGG16Features.h5"
        full_file_name = os.path.join('model', file_name)
        file = os.path.join(settings.STATICFILES_DIRS[0],  full_file_name)# TODO static path
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
        matched_images_scores = []

        for idx in indices:
            matched_images.append(self.names[idx].decode('utf-8')[42:])
            matched_images_scores.append(round(scores[idx], 3))
        return matched_images, matched_images_scores
    

    def image_process(self, image_name):
        # image_path = "/home/parsa/code/master/image/cbir/media/" + str(image_path)
        image_path = os.path.join(settings.MEDIA_ROOT, str(image_name))
        
        # extract features
        input_img_feat = self.extract_feat(image_path)

        # model
        # IN THIS STEP THE h5f FILE MUST EXSIST.
        self.read_h5f_file()

        # Search
        scores = self.calculate_similarity(input_img_feat)
        matched_images, matched_images_scores = self.match_images(scores)
        return matched_images, matched_images_scores
    

    def image_feedback_process(self, selected_images, query_image_path, alpha=1, beta=0.75):
        # calculate a list of features of selected images
        relevant_features = [self.extract_feat(img) for img in selected_images]

        # original feature
        original_feature = self.extract_feat(query_image_path)

        # updated results
        relevant_mean = np.mean(relevant_features, axis=0)
        updated_query = alpha * original_feature + beta * relevant_mean
        
        # model
        # IN THIS STEP THE h5f FILE MUST EXSIST.
        self.read_h5f_file()

        # compute similarities
        scores = self.calculate_similarity(updated_query)
        matched_images, matched_images_scores = self.match_images(scores)
        return matched_images, matched_images_scores
    