from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import time

from rpi_ws281x import Color, PixelStrip, ws


# LED strip configuration:
LED_COUNT = 200         # Number of LED pixels.
LED_PIN = 12           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 155   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.WS2811_STRIP_RGB

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

with SimpleXMLRPCServer(('0.0.0.0', 8000), allow_none=True) as server:
    server.register_introspection_functions()

    # Register a function under function.__name__.
    @server.register_function
    def set_led(led_num, color):
        strip.setPixelColor(led_num, color) 
        print(f"Setting LED {led_num} to color {hex(color)}")
        strip.show()

    @server.register_function
    def clear():
        print("Clearing all LEDs")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, 0)
        strip.show()
        
    server.serve_forever()