""" Govee light controller"""

from os import startfile
from ppadb.client import Client as AdbClient
import time
from pathlib import Path
import sys
import re

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
        resource_id,bounds = pull_ui(device)
        x1,y1,x2,y2 = bounds[resource_id.index('com.govee.home:id/controller')]
        light_selector_position = find_position(int(x1),int(y1),int(x2),int(y2))
        print('govee in main screen, going to controller')
        device.shell('input tap {} {}'.format(light_selector_position[0],light_selector_position[1])) #selects the light
        time.sleep(6) 
        current_activity = device.shell('dumpsys window windows | grep -E mCurrentFocus')
    
    ui = govee_ui(device)[0]
    if controller_screen in current_activity and ui['com.govee.home:id/bg_view']['y1'] != ui['com.govee.home:id/content']['y1'] and ui['com.govee.home:id/bg_view']['y2']==phone_res_y:
        print('moving into position')
        top_bar = ui['com.govee.home:id/content']['y1']
        top_of_selections = ui['com.govee.home:id/bg_view']['y1']
        swipe_time = int(((top_of_selections-top_bar)/0.25)/(phone_res_y/1280)) #Sets swipe speed to 0.25 if the phone were in 1280x720
        device.shell('input touchscreen swipe {} {} {} {} {}'.format(phone_res_x/2,top_of_selections,phone_res_x/2,top_bar,swipe_time)) #swipes up so that the modes can be selected
        current_activity = device.shell('dumpsys window windows | grep -E mCurrentFocus')


def govee_grid(device,light_list):
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
    ui, light_positions = govee_ui(device)
    dictionary = {}
    if len(light_positions) != len(light_list):
        print('Warning: number of lights detected ({}) does not match the number of lights provided ({})'.format(len(light_positions),len(light_list)))
    for i in range(len(light_list)):
        dictionary[light_list[i]] = light_positions[i]
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


def select_lights(device,light_list,mode):
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
    grid = govee_grid(device,light_list)
    time.sleep(1)
    device.shell('input tap {} {}'.format(grid[mode][0],grid[mode][1]))


def timed_light(device,light_list,current_mode,timed_mode,set_time = 1):
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
    select_lights(device,light_list,timed_mode)
    time.sleep(set_time)
    select_lights(device,light_list,current_mode)


def find_position(x1,y1,x2,y2):
    """
    Finds the middle position of the four corners of an object on screen
    Arguments:
        x1,y1,x2,y2 = bounds of the object
    Returns:
        [x,y] = array of midpoint position
    """
    x = int((x2-x1)/2+x1)
    y = int((y2-y1)/2+y1)
    return [x,y]


def govee_ui(device):
    """
    Determines the positions of the lights and the other components of the Govee app 
    Arguments:
        device = connected device
    Returns:
        info = dictionary for graphical information used to maneuver the app into position
        light_list = array of button positions in DIY selection
    """
    info = {}
    light_list = []
    while len(info) == 0 or len(light_list) == 0:
        resource_id,bounds = pull_ui(device)
        
        while len(resource_id) == 0 or len(bounds) == 0 or len(resource_id) != len(bounds):
            resource_id,bounds = pull_ui(device)

        x1,y1,x2,y2 = zip(*bounds)
        x1 = list(map(int,x1))
        y1 = list(map(int,y1))
        x2 = list(map(int,x2))
        y2 = list(map(int,y2))
        for id in range(len(resource_id)):
            if resource_id[id] == 'com.govee.home:id/img_icon':
                position = find_position(x1[id],y1[id],x2[id],y2[id])
                light_list.append(position)
            if resource_id[id] == 'com.govee.home:id/bg_view' or resource_id[id] =='com.govee.home:id/content':
                info[resource_id[id]] = {"x1" : x1[id],"y1": y1[id],"x2":x2[id],"y2":y2[id]}

    return info, light_list


def pull_ui(device):
        """
        Pulls general UI information currently being displayed
        Arguments:
            device = connected device
        Returns:
            resource_id = object names of the various graphics (some return as empty strings)
            bounds = array of positions for each resource_id
    """
        ui_dump = device.shell('uiautomator dump /dev/tty')
        #text = re.findall('text="(.*?)"',ui_dump)
        resource_id = (re.findall('resource-id="(.*?)"',ui_dump))
        bounds = re.findall('bounds="\[(.*?),(.*?)\]\[(.*?),(.*?)\]',ui_dump)
        return resource_id,bounds

device, client = connect()
resolution = device.shell('wm size')
resolution_array = re.findall('Physical size: (.*)x(.*)',resolution)
phone_res_y, phone_res_x = zip(*resolution_array)
phone_res_y = int(phone_res_y[0])
phone_res_x = int(phone_res_x[0])

if __name__ == "__main__":
    open_govee_lights(device)

