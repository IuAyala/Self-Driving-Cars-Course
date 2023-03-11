"""radar automated controller."""

from controller import Display
from vehicle import Car
from vehicle import Driver
import numpy as np

ROW_HIT = 32

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

    # Threshold display
    display_th = Display("display_th")

    while robot.step() != -1:
        # Get point cloud
        raw_range_image = lidar.getRangeImage()  # only one layer

        # TODO: remove everything between START & END: YOUR CODE
        # TODO: use the "raw_range_image" which contains a list of collision
        # distance for each angle (i.e. [1.0, 2.0, 3.0]) would say:
        # there is an object 1.0 meters to the left of the vehicle (-90º)
        # there is an object 2.0 meters in front of the vehicle (0º)
        # there is an object 1.0 meters to the right of the vehicle (90º)
        # there are more values in actual variable but split the reading from -90º to +90º degrees
        # if 0º is going forward, those will be evently spaced
        # TODO: create a variable "angle" which defines the direction that the car
        # should follow, 0 --> straight, -0.1 --> a bit to the left, 0.1 a bit to the right
        # ---------------------- START: YOUR CODE ----------------------------

        # Create range image
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

        # Find collision
        collision_index = np.where(range_image[ROW_HIT][:] == 255)[0]
        # Highlight collisions
        range_image_rgb[ROW_HIT][collision_index] = np.array([255, 0, 0])  # red
        if len(collision_index) > 2:
            new_collision_index = np.array([])
            diff_array = np.abs(collision_index - 64)
            idx = diff_array.argmin()
            np.append(new_collision_index, collision_index[idx])
            # Remove this element
            diff_array = np.delete(diff_array, idx)
            collision_index = np.delete(collision_index, idx)  # to keep indexes right
            idx = diff_array.argmin()
            np.append(new_collision_index, collision_index[idx])
            collision_index = new_collision_index

        if len(collision_index) < 2:
            collision_index = np.array([64, 64])  # to go straight
            print("WARNIG: less that two hit points")

        # Calculate waypoint
        waypoint_col = int(np.average(collision_index))
        range_image_rgb[ROW_HIT][waypoint_col] = np.array([0, 255, 0])  # green
        angle = (waypoint_col - 64) * 0.1

        # Display threshold image
        image_ref = display_th.imageNew(
            range_image_rgb.tobytes(),
            Display.RGB,
            width=range_image_rgb.shape[1],
            height=range_image_rgb.shape[0],
        )
        display_th.imagePaste(image_ref, 0, 0, False)

        # ---------------------- END: YOUR CODE ----------------------------

        driver.setSteeringAngle(angle)
        driver.setCruisingSpeed(40)


if __name__ == "__main__":
    main()
