__author__ = 'ashishrawat'


import cv2, math
import numpy as np

from collections import OrderedDict
import time
class ColourTracker:
    def __init__(self):
        cv2.namedWindow("ColourTrackerWindow", cv2.CV_WINDOW_AUTOSIZE)

        self.capture = cv2.VideoCapture(0)
        #attempt to subtrack background
        # self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        # self.fgbg = cv2.BackgroundSubtractorMOG()

        self.colors = ('blue','red', 'green')
        self.scale_down = 4
        self.lower = {}
        self.upper = {}
        self.xx = 1
        self.yy = 1


        self.lower['blue'] = np.array([110, 70, 70],np.uint8)
        self.upper['blue'] = np.array([130, 255, 255],np.uint8)

        self.lower['red'] = np.array([170, 200, 50],np.uint8)
        self.upper['red'] = np.array([179, 255, 255],np.uint8)

        self.lower['green'] = np.array([85,80,150],np.uint8)
        self.upper['green'] = np.array([95,255,160],np.uint8)

    def track_it(self):
        while True:
            f, orig_img = self.capture.read()
            #attempt bg subtraction
            # fgmask = self.fgbg.apply(orig_img)
            # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
            #cv2.imshow("bgsub",fgmask)

            orig_img = cv2.flip(orig_img, 1)
            img = cv2.GaussianBlur(orig_img, (5,5), 0)
            img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
            img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))
            kernel = np.ones((2,2),np.uint8)


            # mask the same image for red, green and blue
            for color in self.colors:
                binary = cv2.inRange(img, self.lower[color], self.upper[color])
                #cv2.imshow("ColourTrackerWindow2",binary)
                #erode image to remove noise then dilate image to increase pixel thickness
                binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
                #cv2.imshow("ColourTrackerWindow3",binary)

                contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                #sort contours in desc acc to area
                area3 = {}
                for idx, contour in enumerate(contours):
                    area3[cv2.contourArea(contour)] = contour
                area3 = OrderedDict(sorted(area3.items(), key = lambda t: t[0], reverse = True))

                # i=0
                #plot rectangles for contours
                for key in area3.iterkeys():
                    rect = cv2.minAreaRect(area3[key])
                    rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
                    # if i>1:
                    #     break;
                    box = cv2.cv.BoxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(orig_img,[box], 0, (0, 0, 255),2)
                    #i+=1;
                    break

            cv2.imshow("ColourTrackerWindow", orig_img)
            if cv2.waitKey(10) == 27:
                cv2.destroyWindow("ColourTrackerWindow")
                # cv2.destroyWindow("ColourTrackerWindow2")
                # cv2.destroyWindow("ColourTrackerWindow3")
                # cv2.destroyWindow("bgsub")
                self.capture.release()
                break


    def sorted_contours(self,contours):
        area = {}
        for idx, contour in enumerate(contours):
            area[cv2.contourArea] = contour
        area = OrderedDict(sorted(area.items(), key = lambda t: t[0], reverse = True))
        return area

if __name__ == "__main__":
  colour_tracker = ColourTracker()
  colour_tracker.track_it()
