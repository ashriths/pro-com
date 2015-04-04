__author__ = 'ashishrawat'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2, math
import numpy as np
from collections import OrderedDict
import time
class ColourTracker:
  def __init__(self):
    cv2.namedWindow("ColourTrackerWindow", cv2.CV_WINDOW_AUTOSIZE)

    self.capture = cv2.VideoCapture(0)
    self.scale_down = 4
    self.xx = 1
    self.yy = 1
  def run(self):

      while True:
        f, orig_img = self.capture.read()
        orig_img = cv2.flip(orig_img, 1)
        img = cv2.GaussianBlur(orig_img, (5,5), 0)
        img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
        img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))

        red_lower = np.array([110, 50, 50],np.uint8)
        red_upper = np.array([130, 255, 255],np.uint8)
        red_binary = cv2.inRange(img, red_lower, red_upper)

        # ([17, 15, 100], [50, 56, 200])

        #dilation = np.ones((15, 15), "uint8")
        #red_binary = cv2.dilate(red_binary, dilation)

        contours, hierarchy = cv2.findContours(red_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        area3={};
        for idx, contour in enumerate(contours):
            area3[cv2.contourArea(contour)]=contour
        #print area3.keys();
        area3 = OrderedDict(sorted(area3.items(), key=lambda t: t[0], reverse=True))
        #print area3.keys();
        #area3.sort()
        #area3.reverse()

        i=0;
        for key in area3.iterkeys():
            rect = cv2.minAreaRect(area3[key]);
            rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
            i+=1;
            if i>2:
                break;
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(orig_img,[box], 0, (0, 0, 255), thickness = 3)

        cv2.imshow("ColourTrackerWindow", orig_img)

        if cv2.waitKey(10) == 27:
            cv2.destroyWindow("ColourTrackerWindow")
            self.capture.release()
            break

if __name__ == "__main__":
  colour_tracker = ColourTracker()
  colour_tracker.run()
