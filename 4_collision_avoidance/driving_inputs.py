from inputs import get_gamepad
import math
import threading
from pynput.keyboard import Key, Listener
import pynput.keyboard as keyboard


def sign(value):
    if value >= 0:
        return 1
    else:
        return -1


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(
            target=self._monitor_controller, args=()
        )
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def h(self):  # return the buttons/triggers that you care about in this methode
        x = self.LeftJoystickX
        y = self.LeftJoystickY
        a = self.A
        b = self.X  # b=1, x=2
        rb = self.RightBumper
        return [x, y, a, b, rb]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == "ABS_Y":
                    self.LeftJoystickY = (
                        event.state / XboxController.MAX_JOY_VAL
                    )  # normalize between -1 and 1
                elif event.code == "ABS_X":
                    self.LeftJoystickX = (
                        event.state / XboxController.MAX_JOY_VAL
                    )  # normalize between -1 and 1
                elif event.code == "ABS_RY":
                    self.RightJoystickY = (
                        event.state / XboxController.MAX_JOY_VAL
                    )  # normalize between -1 and 1
                elif event.code == "ABS_RX":
                    self.RightJoystickX = (
                        event.state / XboxController.MAX_JOY_VAL
                    )  # normalize between -1 and 1
                elif event.code == "ABS_Z":
                    self.LeftTrigger = (
                        event.state / XboxController.MAX_TRIG_VAL
                    )  # normalize between 0 and 1
                elif event.code == "ABS_RZ":
                    self.RightTrigger = (
                        event.state / XboxController.MAX_TRIG_VAL
                    )  # normalize between 0 and 1
                elif event.code == "BTN_TL":
                    self.LeftBumper = event.state
                elif event.code == "BTN_TR":
                    self.RightBumper = event.state
                elif event.code == "BTN_SOUTH":
                    self.A = event.state
                elif event.code == "BTN_NORTH":
                    self.X = event.state
                elif event.code == "BTN_WEST":
                    self.Y = event.state
                elif event.code == "BTN_EAST":
                    self.B = event.state
                elif event.code == "BTN_THUMBL":
                    self.LeftThumb = event.state
                elif event.code == "BTN_THUMBR":
                    self.RightThumb = event.state
                elif event.code == "BTN_SELECT":
                    self.Back = event.state
                elif event.code == "BTN_START":
                    self.Start = event.state
                elif event.code == "BTN_TRIGGER_HAPPY1":
                    self.LeftDPad = event.state
                elif event.code == "BTN_TRIGGER_HAPPY2":
                    self.RightDPad = event.state
                elif event.code == "BTN_TRIGGER_HAPPY3":
                    self.UpDPad = event.state
                elif event.code == "BTN_TRIGGER_HAPPY4":
                    self.DownDPad = event.state

    def y_x(self, threshold=0.1):
        output = [self.LeftJoystickY, self.RightJoystickX]
        # Dead zone fix
        for i in range(len(output)):
            if abs(output[i]) < threshold:
                output[i] = 0

        return output


class KeyboardController(object):
    def __init__(self, y_limits=[-1, 1], x_limits=[-1, 1], debug=False):
        self.currently_pressed_key = None
        self.y_limits = y_limits
        self.x_limits = x_limits
        self.increments = {"x": 1.0, "y": 1.0}
        self.debug = debug

        self.x_control = False
        self.y_control = False

        self.y = 0  # forward
        self.x = 0  # right

        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        if self.debug:
            if key == self.currently_pressed_key:
                print(f"{key} repeated")
            else:
                print(f"{key} pressed")
                self.currently_pressed_key = key

        # Up
        if hasattr(key, "name"):
            if key.name == "up":
                self.up_pressed()
        else:
            if key == "w" or key == "W":
                self.up_pressed()

        # Down
        if hasattr(key, "name"):
            if key.name == "down":
                self.down_pressed()
        else:
            if key == "s" or key == "S":
                self.down_pressed()

        # Left
        if hasattr(key, "name"):
            if key.name == "left":
                self.left_pressed()
        else:
            if key == "a" or key == "A":
                self.left_pressed()

        # Right
        if hasattr(key, "name"):
            if key.name == "right":
                self.right_pressed()
        else:
            if key == "d" or key == "D":
                self.right_pressed()

    def on_release(self, key):
        if self.debug:
            print(f"{key} release")
            self.currently_pressed_key = None
            if key == Key.esc:
                # Stop listener
                return False

        # Up
        if hasattr(key, "name"):
            if key.name == "up":
                self.up_released()
        else:
            if key == "w" or key == "W":
                self.up_released()

        # Down
        if hasattr(key, "name"):
            if key.name == "down":
                self.down_released()
        else:
            if key == "s" or key == "S":
                self.down_released()

        # Left
        if hasattr(key, "name"):
            if key.name == "left":
                self.left_released()
        else:
            if key == "a" or key == "A":
                self.left_released()

        # Right
        if hasattr(key, "name"):
            if key.name == "right":
                self.right_released()
        else:
            if key == "d" or key == "D":
                self.right_released()

    def up_pressed(self):
        self.y = min(self.y + self.increments["y"], self.y_limits[1])
        self.y_control = True

    def up_released(self):
        self.y_control = False

    def down_pressed(self):
        self.y = max(self.y - self.increments["y"], self.y_limits[0])
        self.y_control = True

    def down_released(self):
        self.y_control = False

    def left_pressed(self):
        self.x = max(self.x - self.increments["x"], self.x_limits[0])
        self.x_control = True

    def left_released(self):
        self.x_control = False

    def right_pressed(self):
        self.x = min(self.x + self.increments["x"], self.x_limits[1])
        self.x_control = True

    def right_released(self):
        self.x_control = False

    def y_x(self):
        if not self.y_control:
            y_sign = sign(self.y)
            self.y = y_sign * max(abs(self.y) - self.increments["y"], 0)

        if not self.x_control:
            x_sign = sign(self.x)
            self.x = x_sign * max(abs(self.x) - self.increments["x"], 0)

        return self.y, self.x


class XboxOrKeyboardController(object):
    def __init__(self):
        try:
            get_gamepad()
        except:
            print("Using KEYBOARD! - Gamepad NOT found!")
            self.controller = KeyboardController()
        else:
            print("Using GAMEPAD!")
            self.controller = XboxController()

    def y_x(self):
        return self.controller.y_x()


if __name__ == "__main__":
    import time

    """
    joy = XboxController()
    while True:
        leftY, rightX = joy.y_x()

        print(f"leftY {leftY:.2f} - rightX {rightX:.2f}")
    """

    """
    kc = KeyboardController()
    while True:
        y, x = kc.y_x()
        print(f"y {y:.2f} - x {x:.2f}")

        time.sleep(0.1)
    """

    xokc = XboxOrKeyboardController()
    while True:
        y, x = xokc.y_x()
        print(f"y {y:.2f} - x {x:.2f}")

        time.sleep(0.1)
