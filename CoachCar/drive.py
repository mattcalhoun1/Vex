#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
chopper = DigitalOut(brain.three_wire_port.a)
poker = DigitalOut(brain.three_wire_port.b)
camera_base = Servo(brain.three_wire_port.c)
controller_1 = Controller(PRIMARY)
motor_rear_l = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
motor_rear_r = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motor_front_l = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
motor_front_r = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
 
import time

# define variables used for controlling motors based on controller inputs
controller_1_up_down_buttons_control_motors_stopped = True

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global controller_1_up_down_buttons_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # check the buttonUp/buttonDown status
            # to control motor_rear_l
            if controller_1.buttonUp.pressing():
                motor_rear_l.spin(FORWARD)
                controller_1_up_down_buttons_control_motors_stopped = False
            elif controller_1.buttonDown.pressing():
                motor_rear_l.spin(REVERSE)
                controller_1_up_down_buttons_control_motors_stopped = False
            elif not controller_1_up_down_buttons_control_motors_stopped:
                motor_rear_l.stop()

                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_up_down_buttons_control_motors_stopped = True

        # wait before repeating the process
        wait(20, MSEC)

 
# define variable for remote controller enable/disable
remote_control_code_enabled = True
rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

# motors are:
# motor_front_l, motor_front_r
# motor_rear_l, motor_rear_r

# nice diagram showing mecanum motion:
# https://robotics.stackexchange.com/questions/21303/rotate-while-strafing-with-mecanum-wheels

 

def move_timed (move_method, velocity: int, seconds: float):
    start = time.time()
    move_method(velocity)

    while (time.time() - seconds) < start:
        time.sleep(0.25)

    stop_moving()

def go_forward (velocity: int):
    for m in [motor_front_l, motor_rear_l, motor_front_r, motor_rear_r]:
        m.set_velocity(velocity, PERCENT)
        m.spin(FORWARD)

def go_backward (velocity: int):
    for m in [motor_front_l, motor_rear_l, motor_front_r, motor_rear_r]:
        m.set_velocity(velocity, PERCENT)
        m.spin(REVERSE)

def strafe_left (velocity: int):
    for m in [motor_front_l,  motor_rear_r]:
        m.set_velocity(velocity, PERCENT)
        m.spin(REVERSE)

    for m in [motor_front_r,  motor_rear_l]:
        m.set_velocity(velocity, PERCENT)
        m.spin(FORWARD)

def strafe_right (velocity: int):
    for m in [motor_front_l,  motor_rear_r]:
        m.set_velocity(velocity, PERCENT)
        m.spin(FORWARD)

    for m in [motor_front_r,  motor_rear_l]:
        m.set_velocity(velocity, PERCENT)
        m.spin(REVERSE)

def rotate_left (velocity: int):
    for m in [motor_front_l,  motor_rear_l]:
        m.set_velocity(velocity, PERCENT)
        m.spin(REVERSE)

    for m in [motor_front_r,  motor_rear_r]:
        m.set_velocity(velocity, PERCENT)
        m.spin(FORWARD)

def rotate_right (velocity: int):
    for m in [motor_front_l,  motor_rear_l]:
        m.set_velocity(velocity, PERCENT)
        m.spin(FORWARD)

    for m in [motor_front_r,  motor_rear_r]:
        m.set_velocity(velocity, PERCENT)
        m.spin(REVERSE)

def stop_moving ():
    for m in [motor_front_l, motor_rear_l, motor_front_r, motor_rear_r]:
        m.stop()

def lower_chopper ():
    # Turns pneumatic on for one second
    chopper.set(True)
    wait(1, SECONDS)
    chopper.set(False)

def extend_jabber ():
    # Turns pneumatic on for one second
    poker.set(True)
    wait(1, SECONDS)
    poker.set(False)

def get_velocity_for_position (axis_pos : int):
    if axis_pos == 0:
        return 0
    elif axis_pos < -50:
        return -100
    elif axis_pos < 0:
        return -50
    elif axis_pos > 50:
        return 100

    return 50

# looks at one of the axis buttons the user is holding
# and returns appropriate velocity based on that
def get_desired_velocity ():
    # choose a random axis that is non-zero and that will be the velocity
    # for now. this should be fixed somehow
    for ax in [controller_1.axis1, controller_1.axis2, controller_1.axis3, controller_1.axis4]:
        this_ax_velocity = get_velocity_for_position(ax.position())
        if this_ax_velocity != 0:
            return abs(this_ax_velocity)

    return 0

# returns the appropriate drive method, based on what
# the driver is doing with the axis buttons on the controller
def get_drive_method ():
    # axis3 = left up/down
    # axis4 = left left/right
    # axis1 = right up/down
    # axis2 = right left/right

    if controller_1.axis2.position() > 0 and controller_1.axis3.position() > 0:
        return go_forward

    elif controller_1.axis2.position() < 0 and controller_1.axis3.position() < 0:
        return go_backward

    elif controller_1.axis2.position() > 0 and controller_1.axis3.position() < 0:
        return rotate_left

    elif controller_1.axis2.position() < 0 and controller_1.axis3.position() > 0:
        return rotate_right

    elif controller_1.axis1.position() < 0 and controller_1.axis4.position() < 0:
        return strafe_left

    elif controller_1.axis1.position() > 0 and controller_1.axis4.position() > 0:
        return strafe_right

    return None

 

def switching_to_autonomous ():

    return controller_1.buttonA.pressing()

 

def switching_to_controlled ():

    return controller_1.buttonB.pressing()

 

# causes the vehicle to enter controller-based driving

def start_controlled():
    while(False):
        drive_method = get_drive_method()
        if drive_method is not None:
            drive_method(get_desired_velocity())
        elif switching_to_autonomous():
            break

        else:
            stop_moving()

        time.sleep(0.25)

    start_autonomous()

 

# causes the vehicle to enter autonomous driving

def start_autonomous():
    while(True):
        for m in [go_forward, go_backward, strafe_left, strafe_right, rotate_left, rotate_right]:
            move_timed(m, 50, 1.0)

            if switching_to_controlled():
                break

        if switching_to_controlled():
            break

        time.sleep(1.0)

        lower_chopper()
        extend_jabber()

    start_controlled()

start_controlled()

 

 