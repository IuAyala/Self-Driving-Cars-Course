import numpy as np
import sklearn
from skimage.feature import hog
from sklearn.base import BaseEstimator, TransformerMixin
import skimage
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import preprocessing


class RGB2GrayTransformer(BaseEstimator, TransformerMixin):
    """
    Convert an array of RGB images to grayscale
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        """returns itself"""
        return self

    def transform(self, X, y=None):
        """perform the transformation and return an array"""
        return np.array([skimage.color.rgb2gray(img) for img in X])


class HogTransformer(BaseEstimator, TransformerMixin):
    """
    Expects an array of 2d arrays (1 channel images)
    Calculates hog features for each img
    """

    def __init__(
        self,
        y=None,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(3, 3),
        block_norm="L2-Hys",
    ):
        self.y = y
        self.orientations = orientations
        self.pixels_per_cell = pixels_per_cell
        self.cells_per_block = cells_per_block
        self.block_norm = block_norm

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        def local_hog(X):
            return hog(
                X,
                orientations=self.orientations,
                pixels_per_cell=self.pixels_per_cell,
                cells_per_block=self.cells_per_block,
                block_norm=self.block_norm,
            )

        return np.array([local_hog(img) for img in X])


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = preprocessing.get_dataset()

    # Pipeline
    HOG_pipeline = Pipeline(
        [
            ("grayify", RGB2GrayTransformer()),
            (
                "hogify",
                HogTransformer(
                    pixels_per_cell=(14, 14),
                    cells_per_block=(2, 2),
                    orientations=9,
                    block_norm="L2-Hys",
                ),
            ),
            ("classify", SVC(kernel="rbf")),
        ]
    )

    # Fit training data
    clf = HOG_pipeline.fit(X_train, y_train)
    percentage_correct_classifications = (
        100 * np.sum(clf.predict(X_test) == y_test) / len(y_test)
    )
    print("Percentage correct classifications: ", percentage_correct_classifications)

    # Data for classification report
    y_pred = clf.predict(X_test)

    # Format data for classification_report (takes label encoded arrays of elements)
    label_enc = sklearn.preprocessing.LabelEncoder()
    y_test_le = label_enc.fit_transform(y_test)
    y_pred_le = label_enc.transform(y_pred)

    print(
        sklearn.metrics.classification_report(
            y_test_le, y_pred_le, target_names=label_enc.classes_
        )
    )
"""
    Percentage correct:  98.55072463768116
              precision    recall  f1-score   support

   crosswalk       1.00      0.93      0.96        29
  speedlimit       1.00      1.00      1.00       130
        stop       1.00      0.93      0.96        14
trafficlight       0.92      1.00      0.96        34

    accuracy                           0.99       207
   macro avg       0.98      0.96      0.97       207
weighted avg       0.99      0.99      0.99       207
"""
