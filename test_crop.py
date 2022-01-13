# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 20:24:40 2021

@author: Dai Duong
"""

import cv2
import numpy as np
image = cv2.imread('plate.jpg')
cv2.imshow("Original Image", image)
cv2.waitKey(0)

height, width = image.shape[:2]
print (image.shape)

# Let's get the starting pixel coordiantes (top left of cropped top)
start_row, start_col = int(0), int(0)
# Let's get the ending pixel coordinates (bottom right of cropped top)
end_row, end_col = int(height * .5), int(width)
cropped_top = image[start_row:end_row , start_col:end_col]
print (start_row, end_row) 
print (start_col, end_col)

cv2.imshow("Cropped Top", cropped_top) 
cv2.waitKey(0) 
cv2.destroyAllWindows()

# Let's get the starting pixel coordiantes (top left of cropped bottom)
start_row, start_col = int(height * .5), int(0)
# Let's get the ending pixel coordinates (bottom right of cropped bottom)
end_row, end_col = int(height), int(width)
cropped_bot = image[start_row:end_row , start_col:end_col]
print (start_row, end_row) 
print (start_col, end_col)

cv2.imshow("Cropped Bot", cropped_bot) 
cv2.waitKey(0) 
cv2.destroyAllWindows()