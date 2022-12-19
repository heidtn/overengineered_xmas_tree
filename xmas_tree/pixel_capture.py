import light_client
import cv2

NUM_LEDS = 200

light_client.clear_all_leds()
cap = cv2.VideoCapture(0)

for i in range(NUM_LEDS):
    light_client.set_led_color(i, 0xFFFFFF)
    ret, im = cap.read()
    cv2.imshow("frame", im)
    cv2.waitKey(50)
    cv2.imwrite(f"images/{i:05d}.png", im)
    light_client.set_led_color(i, 0x000000)
