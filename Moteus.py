import asyncio
import math
import moteus
import os
from sshkeyboard import listen_keyboard_manual

velocity = 0
def on_press(key):
    try:
        global velocity
        if(key.upper() == 'W'):
            velocity += 0.5
        if(key.upper() == "S"):
            velocity -= 0.5
        if(key in ["1","2","3","4","5","6","7","8","9"]):
            velocity = -10 * int(key)
        if(key.upper() == "SPACE"):
            velocity = 0
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

async def on_release(key):
    print('{0} released'.format(
        key))
    if key == "space":
        # Stop listener
        return False

async def MotorTelemetry():

    # By default, Controller connects to id 1, and picks an arbitrary
    # CAN-FD transport, prefering an attached fdcanusb if available.
    c = moteus.Controller()

    # In case the controller had faulted previously, at the start ofaas
    # this script we send the stop command in order to clear it.
    ##await c.set_stop()


    while True:

        # `set_position` accepts an optional keyword argument for each
        # possible position mode register as described in the moteus
        # reference manual.  If a given register is omitted, then that
        # register is omitted from the command itself, with semantics
        # as described in the reference manual.
        #
        # The return type of 'set_position' is a moteus.Result type.
        # It has a __repr__ method, and has a 'values' field which can
        # be used to examine individual result registers.
        state = await c.set_position(position=math.nan, velocity=velocity, query=True)

        # Print out everything.
        # print(state)

        # Print out just the position register.

        print()
        
        print("Position:", state.values[moteus.Register.POSITION])
        print("Velocity:", state.values[moteus.Register.VELOCITY])
        print("Velocity var:", velocity)
        print("Torque:", state.values[moteus.Register.TORQUE])
        print("Voltage:", state.values[moteus.Register.VOLTAGE])
        #print("Q_current:", state.values[moteus.Register.])
        print("Temp:", state.values[moteus.Register.TEMPERATURE])

        # Wait 20ms between iterations.  By default, when commanded
        # over CAN, there is a watchdog which requires commands to be
        # sent at least every 100ms or the controller will enter a
        # latched fault state.
        await asyncio.sleep(0.02)

def main():
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(listen_keyboard_manual(on_press=on_press, on_release=on_release))
        asyncio.ensure_future(MotorTelemetry())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("closing loop")
        loop.close()


if __name__ == '__main__':
    asyncio.run(main())

