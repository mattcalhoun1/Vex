# A simple example of going in hardcoded directions and
# distances that might score a goal.
# This example requires NO sensors, just a basic drivetrain.

# this example was made for vexcode VR, so it might need
# to be slightly modified (dont import vexcode_vrc libraries maybe?)
from vexcode_vrc import *
from vexcode_vrc.events import get_Task_func

# your initialization code will probably be different
brain=Brain()
drivetrain = Drivetrain("drivetrain", 0)

# this auto_score_once method is what you want to call during autonomous mode
def auto_score_once ():
    # go get behind the ball in the center
    drivetrain.drive_for(FORWARD, 1000, MM)
    drivetrain.turn_for(RIGHT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 600, MM)
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 400, MM)
    drivetrain.turn_for(LEFT, 90, DEGREES)

    # push the ball into the goal
    drivetrain.drive_for(FORWARD, 800, MM)

    wait(500, MSEC)

    # reverse and push from a few different angles
    # in case the ball didn't get in
    for reverse_angle in [20, 40]:
        for rotate_order in [(LEFT,RIGHT),(RIGHT,LEFT)]:
            drivetrain.turn_for(rotate_order[0], reverse_angle, DEGREES)
            drivetrain.drive_for(REVERSE, 200, MM)
            drivetrain.turn_for(rotate_order[1], reverse_angle, DEGREES)
            drivetrain.drive_for(FORWARD, 220, MM)
    wait(500, MSEC)

    # celebrate
    drivetrain.drive_for(REVERSE, 400, MM)
    while (True):
        drivetrain.turn_for(RIGHT, 360, DEGREES)
        drivetrain.turn_for(LEFT, 360, DEGREES)


# this call to vr_thread might not apply outside vex vr (?)
vr_thread(auto_score_once)