# import the required libraries
import cv2
import time
import numpy as np
  
  
# define a video capture object

vid = cv2.VideoCapture(0)

# Background capture before for the invisible effect

_, background = vid.read()
time.sleep(2)
_, background = vid.read()

# Filter function for removing noise 

def filter_mask(mask):
    open_kernel = np.ones((5,5),np.uint8)
    close_kernel = np.ones((7,7),np.uint8)
    dilation_kernel = np.ones((10, 10), np.uint8)
    close_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel)
    open_mask = cv2.morphologyEx(close_mask, cv2.MORPH_OPEN, open_kernel)
    dilation = cv2.dilate(open_mask, dilation_kernel, iterations= 1)
    return dilation

# Infinite loop starts here :-

while(True):

      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
    
    # Using cvtColor function to convert to colorspace : -
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Lower Bound of the color desired for the Cloak [Currently set to make the colour green invisible]
    lower_bound = np.array([50, 80, 50])
    # Upper Bound of the color desired for the Cloak [Currently set to make the colour green invisible]
    upper_bound = np.array([90, 255, 255])
    
    # mask is the region where the colour is in the colour range defined above 
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Removing Noise using the filter_mask function 
    mask = filter_mask(mask)
    
    # Apply the mask to take only those region from the saved background 
    # where our cloak is present in the current frame
    cloak = cv2.bitwise_and(background, background, mask=mask)
    
    # inverted mask so the region in black turns white and vice versa
    inverse_mask = cv2.bitwise_not(mask)
    
    # Current background  
    current_background = cv2.bitwise_and(frame, frame, mask=inverse_mask)
    
    # Combining everything together now
    combined = cv2.add(cloak, current_background)
    
    # Display the resulting Final Combined video
    cv2.imshow('Final', combined)
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    key = cv2.waitKey(1)
    if key in [27, ord('q'), ord('Q')]:
        cv2.destroyAllWindows()
        break
        


  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()


