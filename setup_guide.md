# Setup Guide

How to set up and play a Banished manual Archipelago. For more general setup information on Archipelago and/or manual AP worlds, see [here](https://github.com/ManualForArchipelago/Manual/blob/main/docs/play/get-apworld.md).

## Required Software:
- [Archipelago Latest Release](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [Manual Client Latest Release](https://github.com/ManualForArchipelago/Manual/releases/latest)
- A legal copy of Banished by Shining Rock Software (heads up - the AP world has only been tested for Banished on Steam)

## Instructions:
1. Download manual_banished_nutmegs.apworld from the [releases page]([link TODO](https://github.com/megangraft/BanishedManual/releases/tag/Latest)) and save it in your Archipelago/custom_worlds folder
2. Create your Banished YAML. You have a few options for this:
   * From the Archipelago Launcher, open "Options Creator." Find "Manual Banished Nutmegs" in the leftside menu, then fill out your options in the UI. Add your player name at the top then click "Export Options."
   * From the Archipelago Launcher, open "Generate Template Options" to generate a default YAML, and edit the options to your liking.
   * Download the template YAML, Manual_Banished_Nutmegs.yaml, directly from this repo, and edit the options to your liking.
3. Place the YAML in your Archipelago/Players folder
4. From the Archipelago Launcher, open "Generate". You will get a console popup. After it completes, find the generated game in your Archipelago/output folder
5. Upload the generated game to archipelago.gg/uploads to host it on the website, or, extract the output zip file and run the Archipelago Server Data file to host it locally
6. From the Archipelago Launcher, open "Manual Client" (you may need to scroll down). Enter your server and port info in the bar at the top. If my player name is Glenwoody and port is 50000, this is what it should look like:
   * Hosting on the website: `Glenwoody:None@archipelago.gg:50000`
   * Hosting locally: `Glenwoody:None@localhost:50000` (you can find your localhost port number on the console window running the Archipelago Server)
7. In the Manual Client, make sure your "Manual Game ID" is set to "Manual_Banished_Nutmegs." It should show up as an option in a drop down menu. If not, type that in. Then click "Connect".
8. Once connected, go to the Manual tab, then boot your game. From the Banished main menu, open the "Mods" option, then tab to "Browse Workshop" and search for "Debug Menu." Subscribe to the Debug Menu mod. Tab back to "Installed Mods" and make sure that Debug Menu is set to "Enable."
   * When you start your game, a new option "Show debug options" should be available in the Tools and Reports menu. This is how you will redeem certain AP items like livestock, crop/orchard seeds, and filler resources.
9. Optional step, but I **highly** recommend you review the [README](https://github.com/megangraft/BanishedManual/blob/main/README.md) to understand the items you start/don't start with, how progression works, and how to use Debug Mod the intended way.
10. Have fun!
