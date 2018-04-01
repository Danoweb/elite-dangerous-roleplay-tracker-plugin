# elite-dangerous-roleplay-tracker-plugin
A plugin for EDMC and Elite Dangerous for tracking CMDRs on the ED RP private group.

## Installation
* Follow the Steps below to install the Plugin for EDMC.
    * This guide expects that you already have Elite Dangerous installed.
    * This guide expects that you already have EDMC installed.

#### Automated Installation
1. Right click the following link, and click `Save link as...` : \[[EDRP_Setup.exe](../master/latest/EDRP_Setup.exe)\]
2. Run the installer.
<br><br>
**Note:** *This is an unsigned installer and therefore may be flagged by your anti-virus. If you do not feel comfortable with this, please proceed to the **Manual Installation** section below.*

#### Manual Installation
1. Click the green `Clone or Download`
2. Click the `Download Zip`
3. Copy and Paste the `.zip` file into your EDMC `plugins` directory.
4. Extract the Zip file into a new folder in the `plugins` directory.
    1. For Windows: `%LOCALAPPDATA%\EDMarketConnector\plugins`
    2. For Mac: `~/Library/Application Support/EDMarketConnector/plugins`
    3. You should now have an `elite-dangerous-roleplay-tracker-plugin-master` folder inside your plugins directory.
5. Restart EDMC.

## Expected Functionality
* Listen for Logon / Logoff Events for a CMDR (Via EDMC)
* Send Logon events to EDRP API (see API below)
* Send Logoff events to EDRP API (See API below)
* Send Player Location events (System change, docking/undocking, etc.) to EDRP API (see API section below)
* PING the EDRP API approximately once every 5 mins while the CMDR is logged in to the EDRP Private Group.

## EDRP API

* Current API is an open JSON API which can be accessed at:<br>
https://edrp-api.danowebstudios.com/
* List of CMDRs that are currently active on EDRP:<br>
https://edrp-api.danowebstudios.com/web/active-list

## Elite Dangerous Market Connector - Plugin
* Documentation about Elite Dangerous Market Connector and writing plugins for it can be found at:<br>
https://github.com/Marginal/EDMarketConnector/blob/master/PLUGINS.md
