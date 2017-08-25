#!/usr/bin/python

#
#
#

from ledStrip import ledstrip
import time
import argparse
import datetime
from datetime import date 
import logging
import ConfigParser

# Open the config file
Config = ConfigParser.RawConfigParser()
Config.readfp(open('config.ini'))

# Define app description and optional parameters
parser = argparse.ArgumentParser(description = 'Example sketch that controls an LED strip via Spacesb. It uses the 	LED Strip Python library for Adafruit\'s LPD8806 LED strips.')
# Define the led strip length optional parameter
parser.add_argument('-l', '--leds', '--pixels', 
        nargs = 1, type = int, default = 32,
        help = 'Length of led strip leds or pixels')
# Read all command line parameters
args = parser.parse_args()    

# Set up logging
logging.basicConfig(filename='alarm.log', level=logging.INFO, format='%(asctime)s %(message)s')


def main():

    day = time.strftime('%A')
    start_time = Config.get('StartTimes', day)
        
    if (start_time != 'None'):
        start_day = time.strftime('%Y-%m-%d')
        start = ' ' . join([start_day, start_time])
        now = time.time()
        start_now = time.mktime(datetime.datetime.strptime(start, '%Y-%m-%d %H:%M').timetuple())
           
        next_cron = now + 240
        if start_now > now and start_now <= next_cron:
            alarm_start(start_now)


def alarm_start(start_now):

    while True:
        now = time.time()
        if now >= start_now and now <= start_now + 1:
            # initialize spi and leds objects
            spidev	= file("/dev/spidev0.0", "wb")  # ref to spi connection to the led bar
            leds = ledstrip.LEDStrip(pixels = args.leds, spi = spidev)
            all_off(leds)
            logging.info('Starting alarm')
            alarm_on(leds, debug = False)
            time.sleep(600)
            logging.info('Stopping alarm')
            all_off(leds)
            break


def alarm_on(leds, debug = False):
    if debug:
        pause = 1
    else:
        pause = 10
    colors = {'red':[255, 0, 0], 'pink':[127, 7, 2], 'yellow':[124, 51, 1], 'blue':[135, 206, 235]}
    phases = ['red', 'pink', 'yellow', 'blue']
    for phase in phases:
        for pix in range(32):
            if phase != 'blue':
                leds.setPixelColorRGB(pixel = pix, red = colors[phase][0], green = colors[phase][1], blue = colors[phase][1])
                leds.show()
                time.sleep(pause)
            else:
                if pix % 2 == 0:
                    leds.setPixelColorRGB(pixel = pix, red = colors[phase][0], green = colors[phase][1], blue = colors[phase][1])
                else:
                    leds.setPixelColorRGB(pixel = pix, red = 127, green = 127, blue = 127)
                leds.show()
                time.sleep(pause)

def all_off(leds):
    for each in range(32):
        leds.setPixelColorRGB(pixel = each, red = 0, green = 0, blue = 0)
        leds.show()

if __name__ == "__main__":
    main()
