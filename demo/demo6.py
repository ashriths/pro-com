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
            # f, orig_img = self.capture.read()
            orig_img = cv2.imread("star.jpg")
            orig_img = cv2.flip(orig_img, 1)
            img = cv2.GaussianBlur(orig_img, (5,5), 0)
            kernel = np.ones((2,2),np.uint8)
            # cv2.imshow("GaussianBlur", orig_img);

            img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)

            cv2.imshow("ConvertColor",img);

            # img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))
            red_lower = np.array([110, 70, 70],np.uint8)
            red_upper = np.array([130, 255,255],np.uint8)
            red_binary = cv2.inRange(img, red_lower, red_upper)
            binary = cv2.morphologyEx(red_binary, cv2.MORPH_OPEN, kernel)
            cv2.imshow("inRange", red_binary);
            cv2.imshow("Morph",binary)
            #dilation = np.ones((15, 15), "uint8")
            #red_binary = cv2.dilate(red_binary, dilation)
            contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            area3={};
            # largest = contours[0]
            for idx, contour in enumerate(contours):
                area3[cv2.contourArea(contour)] = contour
                # if(cv2.contourArea(largest) < cv2.contourArea(contour)):
                #     largest = contour


            area3 = OrderedDict(sorted(area3.items(), key=lambda t: t[0], reverse=True))
            #
            # for key in area3.iterkeys():
            #     cv2.drawContours(orig_img,area3[key],-1,(0,255,0),3)
            #     break;
            # cv2.drawContours(orig_img, largest,-1,(0,0,255),3)

            contours = area3
            for idx,contour in enumerate(contours):
                cv2.drawContours(orig_img, [contours[contour]],0,(0,0,250),3)
                approx = cv2.approxPolyDP(contours[contour],0.01*cv2.arcLength(contours[contour],True),True)
                # print len(approx)
                cv2.imshow("ColourTrackerWindow  :  "+str(idx), orig_img)
                x = cv2.isContourConvex(contours[contour])
                print "Points ", len(contours[contour]),"  :  ",len(approx), "   :  ",x

                time.sleep(3)



            print "done here \n\n\n\n\n"
            # i=0;
            # for key in area3.iterkeys():
            #     rect = cv2.minAreaRect(area3[key]);
            #     rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
            #     if i>=1:
            #         break;
            #     box = cv2.cv.BoxPoints(rect)
            #     box = np.int0(box)
            #     cv2.drawContours(orig_img,[box], 0, (0, 0, 255), 2)
            #
            #     i+=1;



            if cv2.waitKey(10) == 27:
                # cv2.destroyWindow("ColourTrackerWindow")
                # cv2.destroyWindow("inRange")
                # cv2.destroyWindow("GaussianBlur")
                cv2.destroyAllWindows()
                self.capture.release()
                break
            break;
    # def shape(self,approx):
    #     poly_points = len(apporx)
    #     if( poly_points == 3):
    #         return "triangle"
    #     elif( poly_points == 4 )
    #         return "rectangle"
    #     elif( poly_points == 5)
    #         return "pentagon"
    #     elif( poly_points >50)
    #         return "circle"



if __name__ == "__main__":
  colour_tracker = ColourTracker()
  colour_tracker.run()