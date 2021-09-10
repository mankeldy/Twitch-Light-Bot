"""" Light Bot """

import os
from ppadb.command import transport # for importing env vars for the bot to use
#import twitchio
from twitchio.ext import commands
import govee_controller as gv
from dotenv import load_dotenv
import socketio
import time
from storage import *
from datetime import datetime

load_dotenv()
device,client = gv.connect() #connects to android phone or emulator

sio = socketio.Client()
sio.connect('https://sockets.streamlabs.com?token=' + os.environ['STREAMLABS_SOCKET_API_TOKEN']) #connects to Streamlabs

@sio.on("connect")
def on_connect():
    print("Connected to Streamlabs, Wait for Events")

#coordinates = gv.govee_grid(device,lights) #sets up grid
print("Lights shown to users are {}".format(user_lights))

#Actions
gv.select_lights(device,lights, lights[-1]) #initial setting

# set up the bot with the proper environment tokens and information
bot = commands.Bot(
    token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)
list_of_keys = ['rgb','event']
wait_time = dict.fromkeys(list_of_keys,0)
time_to_wait =15.
count = []
current_light = [0]
current_light[0] = 'rainbow_light'

@sio.on("event")
def on_message(data):
    while datetime.now().timestamp()-wait_time['rgb'] < 2.:
        None #Waiting loop to spool notifications
    if wait_time['event'] == 0 or datetime.now().timestamp()-wait_time['event'] > 10.:
        if data['type'] == 'follow':
            count.append(1)
            print(len(count))
            wait_time['event'] = datetime.now().timestamp()
            gv.timed_light(device,lights,current_light[0],'new_follower')

@bot.event()
async def event_ready():
    'Called once when the bot goes online.'
    print("{} is online!".format(os.environ['BOT_NICK']))

@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

@bot.command(name='rgb')
async def test(ctx,arg=None):
    if arg == None:
        await ctx.send(str(user_lights))
    elif wait_time['rgb'] == 0 or (datetime.now().timestamp()-wait_time['rgb'] > time_to_wait and datetime.now().timestamp()-wait_time['event'] > time_to_wait):
        if arg in lights:
            wait_time['rgb'] = datetime.now().timestamp()
            await ctx.send('Changing to {}'.format(arg))
            gv.select_lights(device,lights, arg)
            current_light[0] = arg
    else:
        await ctx.send('please wait your turn')



if __name__ == "__main__":
    bot.run()
