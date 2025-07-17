## R6 AFK Bot
- What is this?
    - This is an application for Rainbow Six Siege to farm levels, renown, improve reputation, or remove reputation related penalties.
- How do I start using this?
    - Follow the steps outlined in the "Quick Setup" section down below, or to compile it from source follow the "Advanced Setup" section.

## Quick Setup
1. Download the most latest release from [here](https://github.com/grenade-inspector0/R6-AFK-Bot/releases "Latest Releases Page").
2. Move the .exe to it's own folder, you can name it whatever you want, but make sure it's in its own folder.
3. Edit your in-game **DISPLAY** settings to be the following:
   - Set your resolution to 1920x1080 (See "IMPORTANT" section below)
   - Set your game to windowed mode.
   - Set your "Menu Display Area" setting to 100
4. Run the compiled .exe, which is called, "R6_AFK_Bot.exe".
   - **NOTES**:
        - You may have to run it twice due to the config being generated on the first run.
        - When it asks you to select "RainbowSix.exe" you must navigate to your siege install, then select the .exe for Siege, which will be called "RainbowSix.exe". This is for the crash detected, which will restart your game if it detects a crash while you're AFK Botting, this prevent sanctions and other things.
5. While the game is running, press F2 and the R6 AFK Bot should start queueing.
   - **NOTE**: If you press F2 a 2nd time while the R6 AFK Bot is started, it will deactivate the bot and print "Deactivated" to the CMD Prompt Window.

## Advanced Setup
1. Make sure you have [Python](https://www.python.org/) installed.
2. Download the [.zip](https://github.com/grenade-inspector0/R6-AFK-Bot/archive/refs/heads/main.zip) that has the source code in it.
3. Unzip the .zip file.
4. Open a CMD (Command Prompt Window) in the folder that contains the source code.
5. Run the following two commands: (**IN ORDER** excluding the "")
   - "pip install -r requirements.txt"
   - "python compile.py"
6. Follow steps 2-5 outlined in the Quick Setup section.

## IMPORTANT
1. Widescreen monitors are **NOT** supported. The only way to use a widescreen monitor with my program is to open Nvidia Control Panel and set your resolution to 1920x1080. 
2. Botting bans happen a lot than they used to, so to avoid this do the following:
    - Have a **HIGH** starting k/d ***BEFORE*** you start AFK Botting, this goes for whichever gamemode you decide to bot in. 
    - The goal is to end with a k/d of **AT LEAST** 0.20 in the specific gamemode you decide upon.
3. By default the R6 AFK Bot queues for standard, but you can make it queue any gamemode by:
    1. Making sure to clear any "new gamemodes" in the **MAIN MENU** essentially move your mouse over every gamemode that has yellow dot in the top right corner of it.
    2. Queue for your target gamemode, then stop the queue.
    3. Follow step 5 of the Quick Setup section.
4. I probably won't provide any support here, but if you need support then join our [Discord](https://discord.gg/banworld "Banworld") and @ grenade_inspector.

## FAQ
- Why isn't there a wide variety of messages that the R6 AFK Bot will type?
     - Ubisoft has changed how positive reputation units are awarded with the full release of the reputation system. (As of Y10 S1)
     - Meaning, that's it's not efficient for the R6 AFK Bot to type messages like this. While I haven't figured out how it works 100%, it seems that they've changed it to only whitelist a few certain messages.
     - So, if you want a wider variety of messages then enable, "use_old_messages", but be warned you **PROBABLY WON'T** earn positive units with the old system.

## Credits
- [Verybannable](https://github.com/VeryBannable)
    - The original code that this project was based upon. I ended up editing / removing most of his code, but it's his base code at the heart, so he deserves some credit. 
- [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
    - The backbone of this project, used for the state detection of the R6 AFK Bot.
- Bobby (Member in the Discord)
    - Fixed a few things, and got me to provide another update.
- TeamHelper (Member in the Discord)
    - Helped me fix a bug.
