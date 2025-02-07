import numpy as np
import h5py
from skimage import io
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
import cv2
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.filters import roberts, sobel
import os
from django.conf import settings


def extract_features(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("ERROR: IMAGE NOT LOADED, CHECK THE PATH.")

    image = cv2.resize(image, (256, 256))
    # hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    # hist = cv2.normalize(hist, hist).flatten()

    # LAB color feature
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)
    l_feature = round(l.mean(), 2)
    a_feature = round(a.mean(), 2)
    b_feature = round(b.mean(), 2)

    # Textural features based on the gray image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Entropy
    entropy_image = entropy(gray_image, disk(3))
    entropy_mean = round(entropy_image.mean(), 2)
    entropy_std = round(entropy_image.std(), 2)

    # Edge
    sobel_image = sobel(gray_image)
    sobel_feature = round(sobel_image.mean(), 2)
    robert_image = roberts(gray_image)
    robert_feature = round(robert_image.mean(), 2)
    canny_image = cv2.Canny(gray_image, 100, 200)
    canny_feature = round(canny_image.mean(), 2)

    features = np.array([a_feature, b_feature, l_feature, entropy_mean, entropy_std, sobel_feature, canny_feature, robert_feature])
    return features


def search(database_features, query_features, top_n=10):
    similarities = cosine_similarity([query_features], database_features)
    indices = np.argsort(similarities[0])[::-1][:top_n]
    return indices


def search2(database_features, image_features, top_n=5):
    scores = []
    for i in range(database_features.shape[0]):
        score = 1 - spatial.distance.cosine(image_features, database_features[i])
        scores.append(score)
    indices = np.argsort(scores)[::-1][:top_n]
    return indices


def match_images(indices, paths):
    matched_images = []
    for idx in indices:
        matched_images.append(paths[idx].decode('utf-8')[43:])
    return matched_images


# Read features database from h5 file
def read_model():
    h5f = h5py.File('/home/parsa/code/master/image/cbir/static/model/features.h5', 'r')
    features = h5f['dataset_features'][:]
    paths = h5f['dataset_file_paths'][:]
    h5f.close()
    return features, paths


def refine_search_with_feedback(original_feature, relevant_features, image_paths, features, alpha=1, beta=0.75):
    relevant_mean = np.mean(relevant_features, axis=0)
    updated_query = alpha * original_feature + beta * relevant_mean
    # compute similarities
    indices = search(features, updated_query)
    # return n nearest images
    matched_images = match_images(indices, image_paths)
    return matched_images


def image_process(image_path):
    image_path = "/home/parsa/code/master/image/cbir/media/" + str(image_path)
    
    # extract features
    image_features = extract_features(image_path)

    # model
    features, paths = read_model()

    # Search
    indices = search(features, image_features)
    return match_images(indices, paths)


def image_feedback_process(selected_images, query_image_path):
    # read database -> features, paths
    features, paths = read_model()

    # calculate a list of features of selected images
    relevant_features = [extract_features(os.path.join(settings.MEDIA_ROOT, img)) for img in selected_images]

    # original feature
    original_features = extract_features(query_image_path)

    # updated results
    updated_matched_images = refine_search_with_feedback(original_features, relevant_features, paths, features)
    return updated_matched_images

