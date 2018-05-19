import sys
import os
import pygame
import pygame.midi
from pygame.locals import *
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))
def print_device_info():
    pygame.midi.init()
    _print_device_info()
print_device_info()
input_id = pygame.midi.get_default_input_id()
print(input_id)
i = pygame.midi.Input(input_id)
myleaguedict = {36 : 0x10 , 37 : 0x11, 38 : 0x12, 39 : 0x13, 40 : 0x20, 41 : 0x21, 42 : 0x2, 43 : 0x3, 44 : 0x0F, 45 : 0x5, 46 : 0x6, 47 : 0x7, 48 : 0x8,49 : 0x30,50 : 0x31,51 : 0x39}
mystarcraftdict = {36 : 0x1D , 37 : 0x2A, 38 : 0x30, 39 : 0x22, 40 : 0x12, 41 : 0x2C, 42 : 0x1F, 43 : 0x1E, 44 : 0x31, 45 : 0x15, 46 : 0x2E, 47 : 0x2F, 48 : 0x02,49 : 0x03,50 : 0x04,51 : 0x01}
alldicts = [myleaguedict,mystarcraftdict]
mode = 0
modeswitchbutton1 = 0
modeswitchbutton2 = 0
while(1):
  if(i.poll()):
    ival = i.read(1)
    if(ival[0][0][0] <= 159 and ival[0][0][0] >= 144):
      print(mode)
      PressKey(alldicts[mode][ival[0][0][1]])
      if(modeswitchbutton1 and modeswitchbutton2):
        ReleaseKey(alldicts[mode][ival[0][0][1]])
        ReleaseKey(alldicts[mode][48])
        ReleaseKey(alldicts[mode][49])
        mode = ival[0][0][1] - 36
      if(ival[0][0][1] == 48):
        modeswitchbutton1 = 1
      if(ival[0][0][1] == 49):
        modeswitchbutton2 = 1
    if(ival[0][0][0] <= 143 and ival[0][0][0] >= 128):
      print(ival[0][0][1])
      ReleaseKey(alldicts[mode][ival[0][0][1]])
      if(ival[0][0][1] == 48):
        modeswitchbutton1 = 0
      if(ival[0][0][1] == 49):
        modeswitchbutton2 = 0
      
pygame.midi.quit()