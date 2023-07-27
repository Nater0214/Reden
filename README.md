# Reden
A cool project.
## What is this?
Reden is a project I've been working on for a while. It is a LAN messaging app that uses p2p. If you have no idea how this works, then go to the [How it works](#How-it-works:) section. It is very bare at this point, so don't expect much out of it.
## Getting Started:
Here is the steps required to getting started.  
1. Download the most recent release from the releases tab, or [here](https://github.com/Nater0214/Reden/releases/)
2. Unzip the file to where you want it installed.
3. Run reden.exe
4. Connect to your first node:
    1. Click the add node button under the nodes tab
    2. Get a friend running the app to give you their IP and Port
    3. Click add
    4. Yay!
## How it works:
This app works without any central server. When you send a message to another person, your copy of a special file is updated. This file contains messages from everyone on the network. You will then send the updated part, called a block, to other computers connected to you. Every computer on the network that is running this app is a node.s The connected nodes will do the same, until every computer has the message. Don't worry though, it is encrypted, and only the intended recipient can decrypt it.