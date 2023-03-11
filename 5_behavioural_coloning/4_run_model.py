"""run_model controller
Uses trained model to drive the vehicle automatically"""

from vehicle import Car
from vehicle import Driver
import tensorflow as tf
import time
from pathlib import Path
import numpy as np
import utils
import driving_inputs

MODEL_ID = "model_sm_1.h5"  # if -1 latest


def image_to_angle(model, image, gain=0.25):
    # Preprocess image
    image = utils.preprocess_images(image)

    # Reshape image to have 4 dimensions
    image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2])

    prediction = np.array(model(image, training=False))[0]
    if len(prediction) == 1:  # regression
        angle = float(prediction)
        print(f"angle {angle:.2f}")
    else:  # classification
        left, straight, right = prediction
        if left > straight and left > right:
            angle = -gain  # left
        elif right > straight and right > left:
            angle = gain  # right
        else:
            angle = 0  # straight
        print(
            f"angle {angle:.2f} - left {left:.2f} - straight {straight:.2f} - right {right:.2f}"
        )

    return angle


# @utils.profile
def main():
    # Create the Robot instance.
    robot = Car()
    driver = Driver()

    # Get the time step of the current vworld.
    timestep = int(robot.getBasicTimeStep())

    # Create camear instance
    camera = robot.getDevice("camera")
    camera.enable(timestep)  # timestep

    # Controller
    controller = driving_inputs.XboxOrKeyboardController()

    # Load model
    current_folder = Path(__file__).parent
    models_folder = current_folder / "models"
    if not models_folder.exists():
        raise Exception("Missing models foler")

    model = utils.get_model(models_folder, MODEL_ID)

    step = 0
    while robot.step() != -1:
        # Get image from camera
        image = utils.get_image_rgb(camera)

        angle = image_to_angle(model, image)

        leftY, rightX = controller.y_x()

        # Use user controller if set
        if leftY != 0:
            speed = leftY * 40
        else:
            speed = 35  # 45 same as create_dataset

        if rightX != 0:
            angle = rightX * 0.25

        driver.setSteeringAngle(angle)
        driver.setCruisingSpeed(speed)

        # Increase step
        step += 1


if __name__ == "__main__":
    main()
