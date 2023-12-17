

#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
chopper = DigitalOut(brain.three_wire_port.a)
poker = DigitalOut(brain.three_wire_port.b)
#camera_base = Servo(brain.three_wire_port.c)


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
#chopper = Pneumatics('A')

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


def when_started1():
    while(True):
        lower_chopper()
        wait(3, SECONDS)
        extend_jabber()
        wait(3, SECONDS)

when_started1()

