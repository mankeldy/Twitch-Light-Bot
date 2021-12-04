import sys

from _pytest.fixtures import pytestconfig
sys.path.insert(1,'C:/Users/dylan/Documents/Github/govee-stream-controller')
import govee_controller
from storage import *
import pytest
from dotenv import load_dotenv
load_dotenv()
import os

def test_connect():
    device, client = govee_controller.connect()
    assert device is not None and client is not None

device, client = govee_controller.connect()

def test_find_position():
    assert govee_controller.find_position(10,10,20,20) == [15,15]

def test_open_govee_lights():
    govee_controller.open_govee_lights(device)
    current_activity = device.shell('dumpsys window windows | grep -E mCurrentFocus')
    print(current_activity)
    assert 'com.govee.dreamcolorlightv1.adjust.AdjustAcV2' in current_activity

def test_govee_toggle():
    API_QUERY = {'Govee-API-Key':os.environ['GOVEE_API_KEY']}
    res = govee_controller.govee_toggle('on',os.environ['MODEL'],os.environ['DEVICE_MAC_ADDRESS'],API_QUERY)
    
    assert str(res) == '<Response [200]>'

def test_govee_api_rgb():
    API_QUERY = {'Govee-API-Key':os.environ['GOVEE_API_KEY']}
    res = govee_controller.govee_api_rgb(255,255,255,os.environ['MODEL'],os.environ['DEVICE_MAC_ADDRESS'],API_QUERY)
    
    assert str(res) == '<Response [200]>'

def test_select_lights():
    govee_controller.select_lights(device,lights,lights[-1])
    x = input('Did the lights change? (y/n)')
    assert x == 'y'

def test_timed_light():
    govee_controller.timed_light(device,lights,lights[-1],lights[0],2)
    x = input('Did the lights change for a moment then go back? (y/n)')
    assert x == 'y'

