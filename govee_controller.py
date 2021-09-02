""" Govee light controller"""

from ppadb.client import Client as AdbClient
import time
from pathlib import Path
import sys

def connect(host = 'localhost', port = 5037):
    """
    Connects to the device. If using BlueStacks android emulator, the host should be 
    'localhost' (at least that's what it was for me). If you are using an android phone,
    use '127.0.0.1' instead.
    Arguments:
        host = device host name
        port = port to connect through
    Returns: 
        device = connected device
        client = honestly not really sure what this is lol
    """
    client = AdbClient(host = host,port = port)
    
    devices = client.devices()
    if len(devices) == 0 :
        print('No Devices')
        sys.exit()
        
    device = devices[0]
    print('Connected to {}'.format(device))
    return device, client


def open_govee_lights(device):
    """
    While the device is on, open_govee_lights will open the govee app
    until it reaches the DIY screen so that the light mode is ready to be changed.
    Arguments:
        device = connected device 
    Returns:
        None
    """
    current_activity = device.shell('dumpsys window windows | grep mCurrentFocus') #checks what screen is open
    is_govee_open = 'com.govee.home'
    main_govee_screen = 'com.govee.home.main.MainTabActivity'
    controller_screen = 'com.govee.dreamcolorlightv1.adjust.AdjustAcV2'
    if is_govee_open not in current_activity:
        print('opening govee')
        device.shell('monkey -p com.govee.home -c android.intent.category.LAUNCHER 1') #opens the govee app
        time.sleep(4)
        current_activity = device.shell('dumpsys window windows | grep -E mCurrentFocus')
    
    if main_govee_screen in current_activity:
        print('govee in main screen, going to controller')
        device.shell('input tap 300 920') #selects the light
        time.sleep(4) 
        current_activity = device.shell('dumpsys window windows | grep -E mCurrentFocus')
        
    if controller_screen in current_activity:
        print('govee in controller, setting up for light adjusts')
        device.shell('input touchscreen swipe 600 1160 600 400') #swipes up so that the modes can be selected
        current_activity = device.shell('dumpsys window windows | grep -E mCurrentFocus')


def govee_grid(light_list,start_x = 200,start_y = 1300,x_step = 225,y_step = 200):
    """
    Set up the DIY tab grid so that each preset can be selected on command. Defaults
    based on the Bluestacks 5 emulator in 1920x1080. Values can be determined by hand by
    turning on the pointer in the device to view the x-y position.
    Arguments:
        light_list = list of all preset modes in the DIY tab. length should equal # of possible modes
        start_x = x-position of the first mode. default set to 200
        start_y = y-position of the first mode. default set top 1300
        x_step = x distance between each mode.
        y_step = y distance between each mode.
    Returns:
        dictionary = x-y coordinate for each mode with the entries in light_list as keys.
    """
    dictionary = {}
    row = -1
    for i in range(len(light_list)):
        name = Path(light_list[i]).stem
        delta_x = x_step * (i % 4)
        if (i % 4 == 0):
            row += 1
        delta_y = row * y_step 
        dictionary[name] = [start_x+delta_x,start_y+delta_y]

    return dictionary


def toggle_lights(device):
    """
    Presses the power button in govee.
    Arguments:
        device = connected device
    Returns:
        None
    """
    open_govee_lights(device)
    device.shell('input tap 910 275')


def select_lights(device,grid,mode):
    """
    Selects the light mode in the DIY tab
    Arguments:
        device = connected device
        grid = dictionary, x-y coordinate for each mode with the modes as keys.
        mode = string, desired selection
    Returns:
        None
    """
    open_govee_lights(device)
    time.sleep(1)
    device.shell('input tap {} {}'.format(grid[mode][0],grid[mode][1]))


def timed_light(device,grid,current_mode,timed_mode,set_time = 3):
    """
    Turns on a selected mode for a desired amount of time, in seconds. Useful for follower or subscriber 
    notifications. Currently, there's no way to go back to a previous mode, so 'current_mode' must
    be defined.
    Arguments:
        device = connected device
        grid = dictionary, x-y coordinate for each mode with the modes as keys.
        current_mode = light mode that will the lights will be set to after set_time has passed
        timed_mode = light mode that will be active for a length of time.
        set_time = desired length of time before the lights change from timed_mode to current_mode. default set to 3 seconds
    Returns:
        None
    """
    select_lights(device,grid,timed_mode)
    time.sleep(set_time)
    select_lights(device,grid,current_mode)


if __name__ == "__main__":
    device, client = connect()
    open_govee_lights(device)

