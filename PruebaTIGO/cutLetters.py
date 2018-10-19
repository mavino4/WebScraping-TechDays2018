
# coding: utf-8

# # Extrayendo la letras que corresponden 

# In[2]:


import os
import os.path
import cv2
import glob
import imutils


# In[3]:


filename = os.path.basename("test_i/test.png")
captcha_correct_text = "0123"


# In[4]:


# Load the image and convert it to grayscale
image = cv2.imread("test_i/test.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# In[5]:


# Add some extra padding around the image
gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)

# threshold the image (convert it to pure black and white)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# find the contours (continuous blobs of pixels) the image
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Hack for compatibility with different OpenCV versions
contours = contours[0] if imutils.is_cv2() else contours[1]


# In[6]:


letter_image_regions = []
# Now we can loop through each of the four contours and extract the letter
# inside of each one
for contour in contours:
    # Get the rectangle that contains the contour
    (x, y, w, h) = cv2.boundingRect(contour)

    # Compare the width and height of the contour to detect letters that
    # are conjoined into one chunk
    if w / h > 1.25:
        # This contour is too wide to be a single letter!
        # Split it in half into two letter regions!
        half_width = int(w / 2)
        letter_image_regions.append((x, y, half_width, h))
        letter_image_regions.append((x + half_width, y, half_width, h))
    else:
        # This is a normal letter by itself
        letter_image_regions.append((x, y, w, h))


# In[7]:


letter_image_regions

# Sort the detected letter images based on the x coordinate to make sure
# we are processing them from left-to-right so we match the right image
# with the right letter
letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])
letter_image_regions


# In[8]:


# If we found more or less than 4 letters in the captcha, our letter extraction
# didn't work correcly. Skip the image instead of saving bad training data!
# if len(letter_image_regions) != 4:
#    continue
i = 0
# Save out each letter as a single image
for letter_bounding_box, letter_text in zip(letter_image_regions, captcha_correct_text):
    # Grab the coordinates of the letter in the image
    x, y, w, h = letter_bounding_box

    # Extract the letter from the original image with a 2-pixel margin around the edge
    letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]

    # write the letter image to a file
    i +=1
    cv2.imwrite(str(i) + ".png", letter_image)

