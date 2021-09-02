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

load_dotenv()
device,client = gv.connect() #connects to android phone or emulator

sio = socketio.Client()
sio.connect('https://sockets.streamlabs.com?token=' + os.environ['STREAMLABS_SOCKET_API_TOKEN']) #connects to Streamlabs

@sio.on("connect")
def on_connect():
    print("Connected to Streamlabs, Wait for Events")

coordinates = gv.govee_grid(lights) #sets up grid

print("Lights shown to users are {}".format(user_lights))

#Actions
gv.select_lights(device,coordinates, lights[-1]) #initial setting

# set up the bot with the proper environment tokens and information
bot = commands.Bot(
    token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

@sio.on("event")
def on_message(data):
    print((data['type']))
    print(data['type'] == 'follow')
    if data['type'] == 'follow':
        gv.timed_light(device,coordinates,'rainbow_light','new_follower')
 
@bot.event()
async def event_ready():
    'Called once when the bot goes online.'
    print("{} is online!".format(os.environ['BOT_NICK']))

@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

@bot.command(name='rgb_list')
async def test(ctx):
    await ctx.send(str(user_lights))

@bot.command(name='rgb')
async def test(ctx,arg):
    gv.select_lights(device,coordinates, arg)
    await ctx.send('Changing to {}'.format(arg))

if __name__ == "__main__":
    bot.run()
