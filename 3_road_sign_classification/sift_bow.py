from math import dist
import numpy as np
import cv2
import skimage
from sklearn.cluster import KMeans
from scipy.spatial import distance
import pickle
import preprocessing


def sift_features(images):
    sift_vectors = {}
    descriptor_list = []
    sift = cv2.SIFT_create()
    for key, value in images.items():
        features = []
        for img in value:
            img = skimage.img_as_ubyte(img)
            kp, des = sift.detectAndCompute(img, None)
            if des is None:
                continue

            descriptor_list.extend(des)
            features.append(des)

        sift_vectors[key] = features

    return [descriptor_list, sift_vectors]


def kmeans(k, descriptor_list):
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(descriptor_list)
    visual_words = kmeans.cluster_centers_
    return visual_words


def find_index(instance, main_list):
    min_dist = 10e50
    min_idx = -1
    for idx, el in enumerate(main_list):
        dist = distance.euclidean(instance, el)
        if dist < min_dist:
            min_dist = dist
            min_idx = idx

    return min_idx


def image_class(all_bovw, centers):
    dict_feature = {}
    for key, value in all_bovw.items():
        category = []
        for img in value:
            histogram = np.zeros(len(centers))
            for each_feature in img:
                ind = find_index(each_feature, centers)
                histogram[ind] += 1
            category.append(histogram)
        dict_feature[key] = category
    return dict_feature


def knn(images, tests):
    num_test = 0
    correct_predict = 0
    class_based = {}

    for test_key, test_val in tests.items():
        class_based[test_key] = [0, 0]  # [correct, all]
        for tst in test_val:
            predict_start = 0
            # print(test_key)
            minimum = 0
            key = "a"  # predicted
            for train_key, train_val in images.items():
                for train in train_val:
                    if predict_start == 0:
                        minimum = distance.euclidean(tst, train)
                        # minimum = L1_dist(tst,train)
                        key = train_key
                        predict_start += 1
                    else:
                        dist = distance.euclidean(tst, train)
                        # dist = L1_dist(tst,train)
                        if dist < minimum:
                            minimum = dist
                            key = train_key

            if test_key == key:
                correct_predict += 1
                class_based[test_key][0] += 1
            num_test += 1
            class_based[test_key][1] += 1
            # print(minimum)
    return [num_test, correct_predict, class_based]


def accuracy(results):
    avg_accuracy = (results[1] / results[0]) * 100
    print("Average accuracy: %" + str(avg_accuracy))
    print("Class based accuracies:")
    for key, value in results[2].items():
        acc = (value[0] / value[1]) * 100
        print(key + " : %" + str(acc))


if __name__ == "__main__":
    # Parameters
    n_visual_words = 150

    # Pre-processing
    print("Getting dataset")
    X_train, X_test, y_train, y_test = preprocessing.get_dataset()

    print("Sorting dataset")
    train_classes = preprocessing.dict_of_classes(X_train, y_train)
    test_classes = preprocessing.dict_of_classes(X_test, y_test)

    # Feature Extraciton
    print("Extracting features")
    descriptor_list, all_bovw_feature = sift_features(train_classes)
    _, test_bovw_feature = sift_features(test_classes)

    print("Calculating visual words")
    visual_words = kmeans(n_visual_words, descriptor_list)
    # with open("features/visual_words.pickle", "rb") as f:
    #     visual_words = pickle.load(f)

    print("Creating histograms")
    # Creates histograms for train data
    bovw_train = image_class(all_bovw_feature, visual_words)
    # Creates histograms for test data
    bovw_test = image_class(test_bovw_feature, visual_words)

    # Predict
    print("Predicting")
    results_bowl = knn(bovw_train, bovw_test)

    # Performance evaluation
    accuracy(results_bowl)

"""
Average accuracy: %91.2621359223301

Class based accuracies:
speedlimit : %99.2248062015504
trafficlight : %67.64705882352942
stop : %100.0
crosswalk : %79.3103448275862
"""
