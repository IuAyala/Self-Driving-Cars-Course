"""camera_pid controller."""

from controller import Display
from vehicle import Car
from vehicle import Driver
import utils
import numpy as np


# @utils.profile
def main():
    # Create the Robot instance.
    robot = Car()
    driver = Driver()

    # Get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())

    # Create camera instance
    camera = robot.getDevice("camera")
    camera.enable(timestep)  # timestep

    # Threshold display
    display_th = Display("display_th")

    # yellow_pixel = np.array([95, 187, 203])  # road yellow (BGR format)
    yellow_pixel = np.array([25, 127, 127])  # HSV
    error = np.array([8, 80, 80])  # value error over 80 (detects bush)

    while robot.step() != -1:
        # Get image from camera
        image = utils.get_image(camera)

        # Process image (obtain binary image)
        binary_image = utils.colour_threshold_cv2(image, yellow_pixel, error)

        # Column normalized [-0.5, 0.5]
        normalized_column, average_column = utils.calculate_normalized_average_col(
            binary_image
        )
        angle = normalized_column * 1.0  # TODO: needs tunning

        print(f"INFO: normalized column {normalized_column:.2f}")
        print(f"INFO: angle {angle:.2f}")

        utils.display_binary_image(display_th, binary_image, average_column)

        driver.setSteeringAngle(angle)
        driver.setCruisingSpeed(50)


if __name__ == "__main__":
    main()
