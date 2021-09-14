![Github Release](https://img.shields.io/github/v/release/mankeldy/govee-stream-controller?color=blue&label=Release)

Feel free to use this for your own stream (if you could credit me, I'd really appreciate it). If you have any ideas for things to add, let me know! I built this on my own so be nice :)  And if you have any trouble setting it up, feel free to reach out.

This is not the first time anyone has made scripts to control the Govee LED lights. Typically, these involved using the Govee API to control the lights via wifi directly from the computer. However, it was unclear to me whether or not the RGBIC could be scripted to their full potential using this method. To avoid this issue, I created the script `govee_controller` to interface directly with the Govee Home App through your phone or emulator. `bot.py` is a simple bot that interfaces with streamlabs and twitch to allow notifications and twitch chat commands to control the lights.

Known Compatible Configurations -<br />
Phone: Samsung Galaxy S10 <br />
Emulator: Bluestacks 5 <br />
Govee Product: H6117

Setting up the Twitch Bot would not have been possible without: https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8

# Getting started:

Download Bluestacks 5 or similar emulator if not interfacing with your phone and download the Govee Home App

## Update the .env with your tokens and storage.py with your DIY light settings
Get your `Streamlabs Socket API Token` : https://streamlabs.com/dashboard#/settings/api-settings (This connects the bot to streamlabs for their notifications)
Get your `TMI Token`:  https://twitchapps.com/tmi/ (Connects your acccount/bot account to twitch)
Get your `Client ID`: https://dev.twitch.tv/console/apps/create (Honestly, not sure what this does. Seems to run without it just fine, but I followed the guide above to the letter)

## Starting the virtual environment:
 - Install python 3.6 or 3.7
 - Navigate to the working directory in CMD
 - pipenv --python 3.6 or 3.7
 - pipenv install pure-python-adb
 - pipenv install twitchio
 - pipenv install dotenv
 
## Run the bot:
  - pipenv run python `bot.py`
  
  OR 
  
  - In Visual Studio Code, select the interpreter as your virtual environment and run the code.
