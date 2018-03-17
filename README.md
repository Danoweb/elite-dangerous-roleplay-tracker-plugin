# elite-dangerous-roleplay-tracker-plugin
A plugin for EDMC and Elite dangerous for Tracking EDRP Players

## Installation
* Follow the Steps below to install the Plugin for EDMC
    * This guide expects that you already have Elite Dangerous installed
    * This guide expects that you already have EDMC installed 
1. Click the green `Clone or Download`
2. Click the `Download Zip`
3. Copy and Paste the `.zip` file into your EDMC Plugins Directory
4. Extract the Zip file into a new folder in the Plugins Directory
    1. For Windows: `%LOCALAPPDATA%\EDMarketConnector\plugins`
    2. For Mac: `~/Library/Application Support/EDMarketConnector/plugins`
    3. You should now have a `elite-dangerous-roleplay-tracker-plugin-master` fodler inside your plugins directory
6. Restart EDMC

## Expected functionality:
* Listen for Logon / Logoff Events for a CMDR (Via EDMC)
* Send Logon events to WEB Api (see api below)
* Send Logoff events to WEB Api (See api below)
* Send Player Location events (System change, docking/undocking, etc.) to WEB Api (see api below)

## API

* Current api is an open JSON api which can be accessed at:  http://edrp-api.danowebstudios.com/

## Elite Dangerous Market Connector - Plugin
* Documentation about Elite Dangerous Market Connector and writing plugins for it can be found at:
* https://github.com/Marginal/EDMarketConnector/blob/master/PLUGINS.md