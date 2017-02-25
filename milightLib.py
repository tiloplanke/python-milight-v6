import os, sys
import socket

MILIGHT_IP = '192.168.1.60';
MILIGHT_PORT = 5987;
MILIGHT_IDS=[0,0];

COMMAND_ON='31 00 00 08 04 01 00 00 00';
COMMAND_OFF = '31 00 00 08 04 02 00 00 00'
COMMAND_COLOR_PREFIX = '31 00 00 08 01' #The next 4 are color values
COMMAND_SATURATION_PREFIX = '31 00 00 08 02'
COMMAND_BRIGHTNESS_PREFIX = '31 00 00 08 03'
COMMAND_MODE_PREFIX = '31 00 00 08 06'
COMMAND_SPEED_PREFIX = '31 00 00 08 04' # plus 03 for up, 04 for down
COMMAND_TEMPERATURE_PREFIX = '31 00 00 08 05' # Kelvin
COMMAND_WHITE = '31 00 00 08 05 64 00 00 00'
COMMAND_NIGHT = '31 00 00 08 04 05 00 00 00'

#WW have same but one less in value in two last places
WW_COMMAND_ON='31 00 00 07 03 01 00 00 00';
WW_COMMAND_OFF = '31 00 00 07 03 02 00 00 00'
WW_COMMAND_COLOR_PREFIX = '31 00 00 07 01' #The next 4 are color values
#SATURATION does not exist
WW_COMMAND_MODE_PREFIX = '31 00 00 07 04'
WW_COMMAND_BRIGHTNESS_PREFIX = '31 00 00 07 02'
WW_COMMAND_SPEED_PREFIX = '31 00 00 07 03' # plus 03 for up, 04 for down
# TEMPERATURE does not exist
WW_COMMAND_WHITE = '31 00 00 07 03 05 00 00 00'
WW_COMMAND_NIGHT = '31 00 00 07 03 06 00 00 00'

class milight:
    def calcChecksum(self, command):
        checksum = 0
        for n in bytearray.fromhex(command):
            checksum += n
        checksumhex = format(checksum, "04X")
        return format(checksum, "04X")[2:]
        
    def send(self, command, zone):
        #if MILIGHT_IDS[0] == 0:
        initMsg = bytearray.fromhex('20 00 00 00 16 02 62 3A D5 ED A3 01 AE 08 2D 46 61 41 A7 F6 DC AF D3 E6 00 00 1E')
        try :
            # create dgram udp socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #Set the whole string
            s.sendto(initMsg, (MILIGHT_IP, MILIGHT_PORT))
             
            # receive data from client (data, addr)
            s.settimeout(2.0)
            d = s.recvfrom(1024)
            s.settimeout(None)
            reply = d[0]
            addr = d[1]
             
            response = reply.encode('hex')
            #print 'Server reply : ' + response
            #print 'ids : ' + response[-6:-4] + " " + response[-4:-2]
            MILIGHT_IDS[0] = response[-6:-4]
            MILIGHT_IDS[1] = response[-4:-2]
         
            command = command + ' ' + zone;		
            tosend= '80 00 00 00 11 ' + MILIGHT_IDS[0] + ' ' + MILIGHT_IDS[1] + ' 00 5D 00 ' + command + ' 00 ' + self.calcChecksum(command)
            print "sending: " + tosend
            s.sendto(bytearray.fromhex(tosend), (MILIGHT_IP, MILIGHT_PORT))
            s.close()
        except socket.error, initMsg:
            print 'Error Code : ' + str(initMsg)
            s.settimeout(None)
            s.close()

    def on(self, type, zone):
        if type=='WW':
            self.send(WW_COMMAND_ON, zone);
        else:			
            self.send(COMMAND_ON, zone);
        
    def off(self, type, zone):
        if type=='WW':
            self.send(WW_COMMAND_OFF, zone);
        else:
            self.send(COMMAND_OFF, zone);
    
    def color(self, type, zone, hexColor):
        if type=='WW':
            self.send(WW_COMMAND_COLOR_PREFIX + " " + hexColor + " " + hexColor + " " + hexColor + " " + hexColor, zone);
        else:			
            self.send(COMMAND_COLOR_PREFIX + " " + hexColor + " " + hexColor + " " + hexColor + " " + hexColor, zone);
        
    def brightness(self, type, zone, brightnessHex):
        if type=='WW':
            self.send(WW_COMMAND_BRIGHTNESS_PREFIX + " " + brightnessHex + " 00 00 00 ", zone)            
        else:			
            self.send(COMMAND_BRIGHTNESS_PREFIX + " " + brightnessHex + " 00 00 00 ", zone)
        
    def saturation(self, type, zone, saturationHex):
        if type=='WW':
            self.send(WW_COMMAND_SATURATION_PREFIX + " " + saturationHex + " 00 00 00 ", zone)
        else:			
            self.send(COMMAND_SATURATION_PREFIX + " " + saturationHex + " 00 00 00 ", zone)
    
    def temperature(self, type, zone, temperatureHex):
        if type=='WW':
            #not supported?
            return
        else:			
            self.send(COMMAND_TEMPERATURE_PREFIX + " " + saturationHex + " 00 00 00 ", zone)     
 
    def white(self, type, zone):
        if type=='WW':
            self.send(WW_COMMAND_WHITE, zone)
        else:			
            self.send(COMMAND_WHITE, zone)
		
    def night(self, type, zone):
        if type=='WW':
            self.send(WW_COMMAND_NIGHT, zone)
        else:			
            self.send(COMMAND_NIGHT, zone)
		
    def mode(self, type, zone, mode):
        if type=='WW':
            self.send(WW_COMMAND_MODE_PREFIX + " " + mode + " 00 00 00 ", zone)
        else:			
            self.send(COMMAND_MODE_PREFIX + " " + mode + " 00 00 00 ", zone)
		
    def speedUp(self, type, zone):
        if type=='WW':
            self.send(WW_COMMAND_SPEED_PREFIX + " 03 00 00 00", zone)
        else:			
            self.send(COMMAND_SPEED_PREFIX + " 03 00 00 00", zone)
			
    def speedDown(self, type, zone):
        if type=='WW':
            self.send(WW_COMMAND_SPEED_PREFIX + " 04 00 00 00", zone)
        else:			
            self.send(COMMAND_SPEED_PREFIX + " 04 00 00 00", zone)
