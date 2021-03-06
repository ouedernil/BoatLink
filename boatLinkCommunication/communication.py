#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Leila Ouederni"
__copyright__ = "HEIAFR 2017, Project BoatLink for HYDROcontest"
__credits__ = ["Leila Ouederni"]
__version__ = "1"
__email__ = "ouederni.l@gmail.com"
__status__ = "Prototype"
import sys
import glob
import serial

class communication(object):
    def __init__(self):
        """
        Function: __init__
        --------------------------
        Construct a new communication object
        """
        #self.baudrate = 115200
        self.baudrate = 57600
        #self.baudrate = 9600
        self.port = '/dev/ttyUSB3'
        #self.getPort()
        self.xbee = serial.Serial(self.port, self.baudrate)


    def getPort(self):
        """ 
        Function: __init__
        --------------------------
        Get the USB port where the Xbee is connected

        returns:True if the xbee is connected, otherwise false
        """
        print('Please connect the Xbee Module...')
        while(True):
            portsList = self.listPorts()
            for e in portsList:
                print(e)
                if((e == '/dev/ttyUSB0') or (e == '/dev/ttyUSB1') or (e == '/dev/ttyUSB2') or (e == '/dev/ttyUSB3')):

                    self.port = e
                    return True
            return False

    def getChar(self):
        """
        Function: getChar
        --------------------------
        Read the serial port

        returns:Data if data recieved
        """
        try:
            return self.xbee.read(1)
        except(KeyboardInterrupt, SystemExit):
            self.xbee.close()
            raise


    def listPorts(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes the current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def writeCmd(self, frame):
        """
        Function: writeCmd
        --------------------------
        Set frame to serial

        frame: the frame to send

        returns: A list containing the Edge Router ouptut

        """
        try:
            print(frame)
            self.xbee.write(frame)
        except(KeyboardInterrupt, SystemExit):
            self.xbee.close()
            raise
