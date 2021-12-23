import os
import cv2
import numpy as np
from pathlib import Path
import cProfile
import io
import pstats
import tensorflow as tf
import time


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


def get_image_rgb(camera):
    raw_image = camera.getImage()  # This function takes most of the CPU time
    image = np.frombuffer(raw_image, np.uint8).reshape(
        (camera.getHeight(), camera.getWidth(), 4)
    )
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    return image


def get_latest_file_path(folder):
    file_paths = [f for f in folder.iterdir() if os.path.isfile(f)]

    file_paths_sorted = sorted(
        file_paths, key=lambda t: -os.stat(t).st_mtime
    )  # descending, latests to earliest modified

    latests_file_path = file_paths_sorted[0]

    return latests_file_path


def get_model(folder, model_id, verbose=True):
    if isinstance(model_id, str):
        model_path = folder / model_id
    else:
        if model_id != -1:
            model_path = folder / f"model{model_id}.h5"
        else:  # latest model
            model_path = get_latest_file_path(folder)

    if not folder.exists():
        raise Exception("Model does NOT exist")

    if verbose:
        print("--------------------------------------------------")
        print(f"Model used: {model_path.name}")
        print("--------------------------------------------------")

    model = tf.keras.models.load_model(model_path)
    return model


def preprocess_images(images):
    # Convert from integers to floats
    images_norm = images.astype("float32")
    # Normalize
    images_norm = images_norm / 255.0

    return images_norm


if __name__ == "__main__":
    current_folder = Path(__file__).parent
    images_folder = current_folder / "dataset" / "images"
    models_folder = current_folder / "models"
    latest_image_path = get_latest_file_path(images_folder)

    model = get_model(models_folder, -1)  # latest

    image = cv2.imread(str(latest_image_path))
    image = preprocess_images(image)
    # Reshape image to have 4 dimensions
    image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2])

    n_exec = 100
    start = time.time()
    for it in range(n_exec):
        left, straight, right = model.predict(image)[0]
    print(f"Encapsulated {time.time()-start}")

    start = time.time()
    for it in range(n_exec):
        left, straight, right = np.array(model(image, training=False))[0]
    print(f"Encapsulated {time.time()-start}")
