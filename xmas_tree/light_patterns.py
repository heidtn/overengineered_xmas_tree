# collection of interesting lighting configurations
#
# Based off of the work of Tony DiCola (tony@tonydicola.com)
import time
import random
from colorsys import hls_to_rgb


from rpi_ws281x import Color, PixelStrip, ws

# LED strip configuration:
LED_COUNT = 200         # Number of LED pixels.
LED_PIN = 12           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.WS2811_STRIP_RGB
#LED_STRIP = ws.SK6812W_STRIP



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    print("wiping: ", color)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(((i * 256 // strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

#def rainbowSmooth(strip)

def randomLights(strip):
    for i in range(strip.numPixels()):
        color = random.randrange(0, 0xFFFFFF)
        strip.setPixelColor(i, color)
    strip.show()

def christmasTree(strip):
    colors = [0x8934B8,
              0x0A53DE,
              0x24D024,
              0xFBF21A,
              0xFB6F24,
              0xEA0D0D]
              
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, colors[i % len(colors)])
    strip.show()

def oneColor(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    christmasTree(strip)
    while True:
        rainbowCycle(strip)
    #oneColor(strip, Color(0, 255, 255))
