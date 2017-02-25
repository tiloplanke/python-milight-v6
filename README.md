# python-milight-v6

A simple library for milight/limitless/easybulb LED in python.
Supports one Wifi Controller bridge with version v6, as defined by limitless (http://www.limitlessled.com/dev/).

The library was written as a part of my home automation project which is why it's very basic. But it works pretty well.
I found the command values from limitless' dev-page and UDP Packet Captures.
I struggled with the checksum-part, but it seems to work now. 

-Not all available commands are implemented.
-Error-handling isn't perfect.