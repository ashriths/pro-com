__author__ = 'ashishrawat'



import cv2, math
import numpy as np

from collections import OrderedDict
import time
import datetime
class ColourTracker:
    def __init__(self):
        cv2.namedWindow("ColourTrackerWindow", cv2.CV_WINDOW_AUTOSIZE)

        self.capture = cv2.VideoCapture(0)
        #attempt to subtrack background
        # self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        # self.fgbg = cv2.BackgroundSubtractorMOG()

        self.colors = ( 'blue','red', 'green' )
        self.present = {'red':{}, 'blue':{}, 'green':{}}
        for key in self.present:
            self.present[key]['present'] = False
            self.present[key]['timestamp'] = None
        print self.present
        self.scale_down = 4
        self.lower = {}
        self.upper = {}
        self.xx = 1
        self.yy = 1


        self.lower['blue'] = np.array([105, 125, 70],np.uint8)
        self.upper['blue'] = np.array([120, 255, 180],np.uint8)

        self.lower['red'] = np.array([160, 120, 80],np.uint8)
        self.upper['red'] = np.array([180, 255, 200],np.uint8)

        self.lower['green'] = np.array([50,140,50],np.uint8)
        self.upper['green'] = np.array([70,255,200],np.uint8)

    def track_it(self):
        while True:
            f, orig_img = self.capture.read()

            orig_img = cv2.flip(orig_img, 1)
            base_img = cv2.GaussianBlur(orig_img, (5,5), 0)
            base_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
            # cv2.imshow("cvtColor",base_img)


            kernel = np.ones((4,4),np.uint8)


            # mask the same image for red, green and blue
            for color in self.colors:
                img = base_img
                binary = cv2.inRange(img, self.lower[color], self.upper[color])
                # cv2.imshow("inrange",binary)
                #erode image to remove noise then dilate image to increase pixel thickness
                dilated_img = cv2.dilate(binary,kernel,iterations = 1)
                # cv2.imshow("dilation",dilated_img)
                binary = cv2.morphologyEx(dilated_img, cv2.MORPH_OPEN, kernel)
                # cv2.imshow("opening",binary)

                contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
                #sort contours in desc acc to area
                allContours = {}
                for idx, contour in enumerate(contours):
                    allContours[cv2.contourArea(contour)] = contour
                allContours = OrderedDict(sorted(allContours.items(), key = lambda t: t[0], reverse = True))

                i=0
                #plot rectangles for contours
                for key in allContours.iterkeys():
                    if(cv2.contourArea(allContours[key]) <200 or i>1 ):
                        break;
                    # print cv2.contourArea(allContours[key])
                    # this is code to draw a min area rect around the contour
                    # rect = cv2.minAreaRect(allContours[key])
                    # rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
                    # box = cv2.cv.BoxPoints(rect)
                    # box = np.int0(box)
                    self.present[color]['present'] = True
                    timestamp = str (datetime.datetime.utcnow());
                    print timestamp
                    self.present[color]['timestamp'] = timestamp;
                    print color,"  " ,self.present[color]
                    print "\n\n\n"
                    self.printText(orig_img,allContours[key],color)

                    cv2.drawContours(orig_img,[allContours[key]], 0, (0, 0, 255),1)
                    i+=1;

                # break for blue color

            cv2.imshow("ColourTrackerWindow", orig_img)
            if cv2.waitKey(10) == 27:
                cv2.destroyWindow("ColourTrackerWindow")
                # cv2.destroyWindow("ColourTrackerWindow2")
                # cv2.destroyWindow("ColourTrackerWindow3")
                # cv2.destroyWindow("bgsub")
                cv2.destroyAllWindows()
                self.capture.release()
                break
    def printText(self, img, contour, text):

        # text_size,f = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, thickness=2)
        # corner1 = tuple(approx[0][0])
        # corner2 = (approx[0][0][0] + text_size[0] , approx[0][0][1] - text_size[1]  )
        # cv2.rectangle(img,corner1,corner2  , (0,255,0), -1)
        approx = cv2.approxPolyDP(contour,0.05*cv2.arcLength(contour,True),True)
        # print approx
        # print "\ndone here \n"
        # img2 = img
        # cv2.drawContours(img2,approx, 0, (0, 0, 255),2)
        # cv2.imshow("contour approximation",img2)
        # find top right point
        largest = [10000,10000]
        for coord1 in approx:
            for coord_inner in coord1:
                if largest[0] > coord_inner[0]:
                    largest = coord_inner
        largest[0]-=10;
        largest[1]-=10

        M = cv2.moments(contour);
        if M['m00']<10:
            return
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(img, (cx, cy), 5,(0,100,255) ,thickness=3)
        cv2.putText(img, str(cx)+", "+str(cy) , (cx+10, cy+10), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,150,255),thickness= 1);

        cv2.putText(img, text , tuple(largest), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),thickness= 2);

    def sorted_contours(self,contours):
        area = {}
        for idx, contour in enumerate(contours):
            area[cv2.contourArea] = contour
        area = OrderedDict(sorted(area.items(), key = lambda t: t[0], reverse = True))
        return area

if __name__ == "__main__":
  colour_tracker = ColourTracker()
  colour_tracker.track_it()

