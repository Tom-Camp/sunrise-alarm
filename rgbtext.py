#!/usr/bin/python

from ledStrip import ledstrip
import argparse
import time

# Define app description and optional parameters
parser = argparse.ArgumentParser(description = 'Example sketch that controls an LED strip via Spacesb. It uses the 	LED Strip Python library for Adafruit\'s LPD8806 LED strips.')
# Define the led strip length optional parameter
parser.add_argument('-l', '--leds', '--pixels', 
        nargs = 1, type = int, default = 32,
        help = 'Length of led strip leds or pixels')
# Read all command line parameters
args = parser.parse_args()


def main():
    # initialize spi and leds objects
    spidev = file("/dev/spidev0.0", "wb")  # ref to spi connection to the led bar
    leds = ledstrip.LEDStrip(pixels=args.leds, spi=spidev)
    turn_off(leds)

    while True:
        ured, ugreen, ublue = raw_input( "Enter RGB values (x to exit): ").split()

        if ured == 'x':
            break
        for i in range(32):
            leds.setPixelColorRGB(pixel = i, red = int(ured), green = int(ugreen), blue = int(ublue))
            leds.show()

        time.sleep(3)
        turn_off(leds)


def turn_off(leds):
    for each in range(32):
        leds.setPixelColorRGB(pixel = each, red = 0, green = 0, blue = 0)
        leds.show()


if __name__ == "__main__":
    main()
