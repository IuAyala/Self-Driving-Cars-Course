import os
from pathlib import Path
import xml.dom.minidom
import cv2
from skimage.transform import rescale, resize
from sklearn.model_selection import train_test_split
from PIL import Image
import numpy as np
import pickle

# Dataset --> https://www.kaggle.com/andrewmvd/road-sign-detection
# Classes (4) --> speedlimit, trafficlight, crosswalk, stop

# Prameters
SEED = 123  # for reprducibility
ANNOTATIONS_FOLDER = Path("original_dataset/annotations")
IMAGES_FOLDER = Path("original_dataset/images")
FEATURES_FOLDER = Path("features")
MODIFIED_DATASET_FOLDER = Path("modified_dataset")
STANDARD_SHAPE = (100, 100)
MIN_SIDE = 20  # if one side is smaller than this, the image will be discarded


def crop_image(image, x_min, x_max, y_min, y_max):
    """Crops a square shaped part of the image, ensuring that the image is centered as long as the image is big enough for the square crop

    Args:
        image (np.ndarray): image as a 3D numpy array
        x_min (int): initial column of the crop
        x_max (int): final column of the crop
        y_min (int): initial row of the crop
        y_max (int): final row of the crop

    Raises:
        Exception: if the image is not big enough raises an exception

    Returns:
        np.ndarray: square crop of the input image
    """
    x_range = x_max - x_min  # width axis
    y_range = y_max - y_min  # height axis

    rows, cols = image.shape[:2]
    while x_range >= rows or y_range >= cols:
        if x_range >= rows:
            x_range -= 1
            x_max -= 1
        if y_range >= cols:
            y_range -= 1
            y_max -= 1

    if y_range > x_range:  # y_range greater
        x_middle = (x_min + x_max) / 2
        x_min = int(x_middle - y_range / 2)
        x_max = int(x_min + y_range)
    elif y_range < x_range:  # x_range greater
        y_middle = (y_min + y_max) / 2
        y_min = int(y_middle - x_range / 2)
        y_max = int(y_min + x_range)

    count = 0
    while (
        x_min < 0
        or y_min < 0
        or x_max > image.shape[1] - 1
        or y_max > image.shape[0] - 1
    ):
        if x_min < 0:
            x_min += 1
            x_max += 1
        if y_min < 0:
            y_min += 1
            y_max += 1
        if x_max > image.shape[1] - 1:
            x_min -= 1
            x_max -= 1
        if y_max > image.shape[0] - 1:
            y_min -= 1
            y_max -= 1

        count += 1
        if count > 1000:
            raise Exception(
                "Stuck in while loop!!"
            )  # TODO: needs improving - smarter behaviour

    new_image = image[y_min:y_max, x_min:x_max, :]

    return new_image


def read_dataset(overwrite=False, standar_size=True, store_images=True):
    # Annotation files list
    annotation_files = [f for f in ANNOTATIONS_FOLDER.iterdir() if f.is_file()]

    if overwrite:
        os.remove(FEATURES_FOLDER)

    # Create features folder if doesn't exist
    FEATURES_FOLDER.mkdir(parents=True, exist_ok=True)
    cropped_images_folder = MODIFIED_DATASET_FOLDER / "cropped_images"
    cropped_images_folder.mkdir(parents=True, exist_ok=True)

    X = []
    y = []
    too_small_count = 0
    # Create features for each element
    count = 0
    for annotation_file in annotation_files:
        doc = xml.dom.minidom.parse(str(annotation_file))
        folder = doc.getElementsByTagName("folder")[0].firstChild.nodeValue
        # Image name
        filename = doc.getElementsByTagName("filename")[0].firstChild.nodeValue

        # Load image
        image_path = IMAGES_FOLDER / filename
        image_uint8 = cv2.imread(str(image_path))  # range 0-255, encoded in uint8
        image_uint8 = cv2.cvtColor(image_uint8, cv2.COLOR_BGR2RGB)

        # Normalize image
        image = image_uint8 / 255  # range 0-1, encoded float64

        # Get element name and bounding box
        names = doc.getElementsByTagName("name")
        bndboxs = doc.getElementsByTagName("bndbox")
        label = doc.getElementsByTagName("name")[0].firstChild.nodeValue

        for name, bndbox in zip(names, bndboxs):
            label = name.firstChild.nodeValue
            xmin = int(bndbox.getElementsByTagName("xmin")[0].firstChild.nodeValue)
            ymin = int(bndbox.getElementsByTagName("ymin")[0].firstChild.nodeValue)
            xmax = int(bndbox.getElementsByTagName("xmax")[0].firstChild.nodeValue)
            ymax = int(bndbox.getElementsByTagName("ymax")[0].firstChild.nodeValue)

            if min(xmax - xmin, ymax - ymin) < MIN_SIDE:
                too_small_count += 1
                continue

            #  Crop image
            new_image = crop_image(image, xmin, xmax, ymin, ymax)
            # new_image = image[ymin:ymax, xmin:xmax, :]
            if standar_size:
                new_image = resize(new_image, STANDARD_SHAPE, anti_aliasing=False)

            # Add elements to dataset
            X.append(new_image)
            y.append(label)

            # Save image
            if store_images:
                im = Image.fromarray((new_image * 255).astype(np.uint8))
                image_path = cropped_images_folder / f"image_{count}.png"
                im.save(image_path)

            count += 1

    print("Number images skipped - too small:", too_small_count)

    return X, y


def get_dataset(recompute=False):
    # Check if already has been generated
    dataset_file = "modified_dataset/dataset.pickle"
    if Path(dataset_file).exists() and not recompute:
        print("INFO: modified dataset already created")
        with open(dataset_file, "rb") as file:
            X, y = pickle.load(file)
    else:
        X, y = read_dataset()
        # Save dataset
        with open(dataset_file, "wb") as file:
            # A new file will be created
            pickle.dump([X, y], file)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=True,
        random_state=SEED,
    )

    return X_train, X_test, y_train, y_test


def dict_of_classes(X_train, y_train):
    output = {}

    for img, label in zip(X_train, y_train):
        if label not in output:
            output[label] = []

        output[label].append(img)

    return output


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_dataset(recompute=True)

    print("Classes", set(y_train))
