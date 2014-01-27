###############################################################################
## Gmilito
##
## Copyright (C) 2014 Juan Delgado dp.juan@gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import imaplib
import time
import serial
import struct


HOST = "imap.gmail.com"
USER = "example@gmail.com"
PASS = "password"

MAILBOX = "INBOX"

UNSEEN = "UNSEEN"

TTY = "/dev/tty.usbmodem411"
BAUDRATE = 9600

class MailCheck_WriteSerial:
    def __init__(self):
        """CONSTRUCTOR"""
        self.mailbox = imaplib.IMAP4_SSL(HOST)
        self.mailbox.login(USER, PASS)
        #self.mailbox.select(MAILBOX)
        self.ser = serial.Serial(TTY, BAUDRATE)
    

    def get_updates(self):
        response, message = self.mailbox.status(MAILBOX, "(%s)" % UNSEEN)
        if response == 'OK':
            return int(message[0].split(UNSEEN)[1].split(")")[0])
        
    def write(self,num):
        if num < 0:
            num = 0
        elif num > 255:
            num = 255
        self.ser.write(struct.pack('B', num))        

    def __del__(self):
        """DESTRUCTOR"""
        self.mailbox.logout()
        #self.mailbox.close()
        self.ser.close()

if __name__ == "__main__":
    C = MailCheck_WriteSerial()
    while True:
        time.sleep(5)
        C.write(C.get_updates())    
