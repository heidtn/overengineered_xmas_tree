import glob
import cv2
import numpy as np
from tqdm import tqdm
import numba
from numba import njit


def map_pixels(image_files, box_corner, box_width):
    # mark out a box around the desired area
    # do we want to weight the pixels or something? average?
    # keep it simple to start
    # find the pixel that matches in the box, save a map from that pixel to that LED
        # ok yeah and one LED can match multiple pixels with a weight, we can sum them
    # just reverse the map
    base_image = cv2.imread(image_files[0])
    base_grey = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)

    end_point = (box_corner[0] + box_width, box_corner[1] + box_width)

    base_grey = base_grey[box_corner[1]:end_point[1], box_corner[0]:end_point[0]]

    box_map = [[0 for j in range(box_width)] for i in range(box_width)]
    neopixel_map = [[] for i in range(len(image_files))]

    for num, image in enumerate(tqdm(image_files[1:])):
        im = cv2.imread(image)
        im = im[box_corner[1]:end_point[1], box_corner[0]:end_point[0]]

        im_grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(base_grey, im_grey)
        ret, thresh = cv2.threshold(diff, 127, 255, cv2.THRESH_BINARY)
        thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        showimage = np.hstack((im, thresh_color))

        count_pixels(thresh, box_map, neopixel_map, num)

        cv2.imshow("box", showimage)
        #if cv2.waitKey(1) == ord('q'):
        #    return

    weighted_map = [[] for i in range(len(image_files))]
    for light in range(len(image_files)):
        for point in neopixel_map[light]:
            if point:
                # TODO(HEIDT) we only need a count of the box map
                led_count = box_map[point[0]][point[1]]
                weighted_map[light].append((point, 1.0/led_count))
            else:
                pass
    
    with open('out.txt', 'w') as f:
        for index, light in enumerate(image_files):
            f.write(",".join([str(m) for m in weighted_map[index]]))
            if index != len(image_files) - 1:
                f.write("\n")

def count_pixels(thresh, box_map, neopixel_map, num):
    for i in range(thresh.shape[0]):
        for j in range(thresh.shape[1]):
            if thresh[i][j] != 0:
                box_map[i][j] += 1
                neopixel_map[num + 1].append((i, j))

def main():
    images = glob.glob("xmas_tree/images/*.png")
    map_pixels(images, (550, 100), 350)

if __name__ == "__main__":
    main()