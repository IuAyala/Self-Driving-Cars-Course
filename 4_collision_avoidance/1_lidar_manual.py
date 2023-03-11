"""radar controller."""

from controller import Display
from vehicle import Car
from vehicle import Driver
import numpy as np
import driving_inputs


# @utils.profile
def main():
    # Create the Robot instance.
    robot = Car()
    driver = Driver()

    # Get the time step of the current vworld.
    timestep = int(robot.getBasicTimeStep())

    # 2D Lidar, horizontal resolution 180, fov 3.14, max range 80,
    lidar = robot.getDevice("Sick LMS 291")
    lidar.enable(timestep)

    # Controller
    controller = driving_inputs.XboxOrKeyboardController()

    # Threshold display
    display_th = Display("display_th")

    while robot.step() != -1:
        # Get point cloud
        raw_range_image = lidar.getRangeImage()  # only one layer

        range_image = np.zeros((64, 128), dtype=np.uint8)
        for i, range in enumerate(raw_range_image):
            azimuth = np.pi - i * np.pi / len(raw_range_image)  # 0 pointing left
            if range == np.inf:
                continue
            scaled_range = range / lidar.getMaxRange() * 64
            x_vehicle = scaled_range * np.cos(azimuth)
            y_vehicle = scaled_range * np.sin(azimuth)
            r_image = range_image.shape[0] - y_vehicle
            c_image = x_vehicle + range_image.shape[1] / 2
            # Limit index values to be inside the image
            r_image = max(0, r_image)
            r_image = min(63, r_image)
            c_image = max(0, c_image)
            c_image = min(127, c_image)
            range_image[int(r_image)][int(c_image)] = 255

        # Image to display
        range_image_rgb = np.dstack(
            (
                range_image,
                range_image,
                range_image,
            )
        )

        # Display threshold image
        image_ref = display_th.imageNew(
            range_image_rgb.tobytes(),
            Display.RGB,
            width=range_image_rgb.shape[1],
            height=range_image_rgb.shape[0],
        )
        display_th.imagePaste(image_ref, 0, 0, False)

        leftY, rightX = controller.y_x()

        speed = leftY * 45  # max speed
        angle = rightX * 0.25

        driver.setSteeringAngle(angle)
        driver.setCruisingSpeed(speed)


if __name__ == "__main__":
    main()
