# From: https://learn.adafruit.com/nokia-5110-3310-lcd-python-library?view=all

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import Image
import ImageDraw
import ImageFont

class DisplayNokia5110:

    def __init__(self):
        # Raspberry Pi hardware SPI config:
        DC = 23
        RST = 24
        SPI_PORT = 0
        SPI_DEVICE = 0

        # Hardware SPI usage:
        self.display = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))


    def display_weather_values(self, date_time, temperature, humidity, pressure, light):
        # Initialize library.
        self.display.begin(contrast=60)

        # Clear display.
        self.display.clear()
        self.display.display()

        # Load default font.
        font = ImageFont.load_default()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Write some text.
        draw.text((0, 12), 'HEY =;)', font=font)
        #draw.text((0, 12), date_time, font=self.font)
        #draw.text((0, 24), "{:.1f}C ".format(temperature) + "{:.1f}%".format(humidity), font=self.font)
        #draw.text((0, 36), "{:.2f}mBar".format(pressure), font=self.font)
        #draw.text((0, 48), "{:.1f}lx".format(light), font=self.font)

        # Display image.
        self.display.image(image)
        self.display.display()
