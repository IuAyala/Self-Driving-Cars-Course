import os
import cv2
import random
import json
from functools import partial
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
import utils


def load_dataset(dataset_folder, shuffle=True):
    X = []
    y = []
    json_files = [el for el in dataset_folder.iterdir() if el.suffix == ".json"]

    if shuffle:
        random.shuffle(json_files)

    for json_file in json_files:
        with open(json_file) as f:
            sample = json.load(f)

        X.append(cv2.imread(sample["image"]))
        y.append([sample["angle"]])

    # Convert to np arrays & process images
    X = np.asarray(X)
    X = utils.preprocess_images(X)
    y = np.asarray(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    current_folder = Path(__file__).parent
    dataset_folder = current_folder / "dataset"
    images_folder = dataset_folder / "images"
    models_folder = current_folder / "models"
    logs_folder = current_folder / "logs"

    print("Loading dataset ...")
    X_train, X_test, y_train, y_test = load_dataset(dataset_folder)

    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train, y_train, test_size=0.25, random_state=54
    )

    # Keras model
    DefaultConv2D = partial(
        keras.layers.Conv2D, kernel_size=3, activation="relu", padding="SAME"
    )

    model = keras.Sequential(
        [
            DefaultConv2D(filters=64, kernel_size=7, input_shape=[64, 128, 3]),
            keras.layers.MaxPooling2D(pool_size=2),
            DefaultConv2D(filters=128),
            DefaultConv2D(filters=128),
            keras.layers.MaxPooling2D(pool_size=2),
            DefaultConv2D(filters=256),
            DefaultConv2D(filters=256),
            keras.layers.MaxPooling2D(pool_size=2),
            keras.layers.Flatten(),
            keras.layers.Dense(units=128, activation="relu"),
            keras.layers.Dropout(0.2),  # lower less regularization
            keras.layers.Dense(units=64, activation="relu"),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(units=1),  # check if softmax?
        ]
    )

    model.compile(loss="mean_squared_error", optimizer="SGD")

    # loss
    # sparse_categorical_crossentropy used for sparse labels (target class index)
    # categorial_cross_entropy would yield a one-hot vector (only one positive label)
    # mean_squared_error for regression

    tensorboard_cb = tf.keras.callbacks.TensorBoard(
        log_dir=logs_folder,
        histogram_freq=1,
    )
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=False,
    )

    history = model.fit(
        X_train,
        y_train,
        epochs=500,
        batch_size=32,  # 32
        validation_data=(X_valid, y_valid),
        callbacks=[tensorboard_cb, early_stopping_cb],
    )
    mse_test = model.evaluate(X_test, y_test)
    print(f"Test Data - MSE: {mse_test}")

    # Save model
    os.makedirs(models_folder, exist_ok=True)
    model.save(models_folder / "model2.h5")
