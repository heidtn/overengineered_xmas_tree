import numpy as np
import cv2
from ast import literal_eval
import time

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

def visualize_video(video_file, map_file, size):
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    pixel_map = []
    with open(map_file, 'r') as f:
        for line in f.readlines():
            try:
                tuples = literal_eval(line.strip("\n"))
            except:
                tuples = []
            pixel_map.append(tuples)

    cap = cv2.VideoCapture(video_file)
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, frame = cap.read()
        resized = cv2.resize(frame, (size, size))
        strip.clear()
    
        for index, pixel in enumerate(pixel_map):
            color = np.array([0, 0, 0])
            for weight in pixel:
                color += weight[1] * frame[weight[0][0], weight[0][1]]
            strip.setPixelColorRGB(index, color[2], color[1], color[0])
        strip.show() 
        time.sleep(0.05)
        for index, pixel in enumerate(pixel_map):
            strip.setPixelColor(0x000000)
        strip.show()
        


def main():
   visualize_video("xmas_tree/Rick_Astley_Never_Gonna_Give_You_Up.mp4", "out.txt", 350) 

if __name__ == "__main__":
    main()