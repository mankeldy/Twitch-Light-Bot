![Github Release](https://img.shields.io/github/v/release/mankeldy/govee-stream-controller?color=blue&label=Release)

Feel free to use this for your own stream (if you could credit me, I'd really appreciate it. Either linking the repository or twitch.tv/MuffinMan031 would suffice). If you have any ideas for things to add, let me know! I built this on my own so be nice :)  And if you have any trouble setting it up, feel free to reach out.

This is not the first time anyone has made scripts to control the Govee LED lights. Typically, these involved using the Govee API to control the lights via wifi directly from the computer. However, it was unclear to me whether the DIY modes could be changed using the API. To avoid this issue, I created the script `govee_controller` to interface directly with the Govee Home App through your phone or emulator and send direct RGB commands via the API. `bot.py` is a simple bot that interfaces with Streamlabs and Twitch.tv to allow notifications and twitch chat commands to control the lights. 

Known Compatible Configurations -<br />
Phone: Samsung Galaxy S10 <br />
Emulator: Bluestacks 5 <br />
Govee Product: H6117

Setting up the Twitch Bot would not have been possible without: https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8

# Getting started:

Download Bluestacks 5 or similar emulator if not interfacing with your phone and download the Govee Home App

## Update the .env with your tokens and storage.py with your DIY light settings
Get your `Streamlabs Socket API Token` : https://streamlabs.com/dashboard#/settings/api-settings (This connects the bot to streamlabs for their notifications)<br />
Get your `TMI Token`:  https://twitchapps.com/tmi/ (Connects your acccount/bot account to twitch)<br />
Get your `Client ID`: https://dev.twitch.tv/console/apps/create (Honestly, not sure what this does. Seems to run without it just fine, but I followed the guide above to the letter)<br />
Get your `Govee API key`: request a key via the Govee Home app (needed to send commands via the Govee API)<br />
Get your `Mac Address` and `Product Model`: you'll find it in the settings of the device<br />


## Starting the virtual environment:
 - Install python 3.6 or 3.7
 - Navigate to the working directory in CMD
 - pipenv --python 3.6 or 3.7
 - pipenv install pure-python-adb
 - pipenv install twitchio
 - pipenv install dotenv
 
## Add light configuration:
  - Add the names of the light modes lists in `storage.py` (these do not have to be the same names in the Govee app, but will be the commands used to change the lights)
 
## Run the bot:
  - pipenv run python `bot.py`
  
  OR 
  
  - In Visual Studio Code, select the interpreter as your virtual environment and run the code.

  OR 
  
  - Follow the instructions in the Twitch Light Bot.bat file to run the code on its own. A shortcut can be made on the desktop for an easier startup

