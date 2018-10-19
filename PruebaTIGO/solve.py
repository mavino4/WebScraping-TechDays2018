
# coding: utf-8

# # Extrayendo la letras que corresponden 

# In[15]:


import os
import os.path
import cv2
import glob
import imutils


# In[16]:


os.system("python3 cutLetters.py")


# # Redimensionando Para ajustar

# In[17]:


def resize_to_fit(image, width, height):
    """
    A helper function to resize an image to fit within a given size
    :param image: image to resize
    :param width: desired width in pixels
    :param height: desired height in pixels
    :return: the resized image
    """
    # grab the dimensions of the image, then initialize
    # the padding values
    (h, w) = image.shape[:2]

    # if the width is greater than the height then resize along
    # the width
    if w > h:
        image = imutils.resize(image, width=width)

    # otherwise, the height is greater than the width so resize
    # along the height
    else:
        image = imutils.resize(image, height=height)

    # determine the padding values for the width and height to
    # obtain the target dimensions
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)

    # pad the image then apply one more resizing to handle any
    # rounding issues
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
        cv2.BORDER_REPLICATE)
    image = cv2.resize(image, (width, height))

    # return the pre-processed image
    return image


# In[18]:


def changeContrast(img , b= 5. ,  c = 700.):
    return cv2.addWeighted(img, 1. + c/127., img, 0, b-c)


# In[19]:


paths = ["1.png", "2.png", "3.png", "4.png"]


# In[20]:




# # Cargar el modelo para predecir 

# In[21]:


import pandas
import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib


# In[22]:


labels = np.fromfile("labels", dtype="<U1")


# In[23]:


loaded_model = joblib.load("lrAll.hdf5")


# In[24]:



def Prediccion():
    Y = []
    for path in paths:
        X =cv2.imread(path)
        X = resize_to_fit(changeContrast(cv2.cvtColor(X, cv2.COLOR_BGR2RGB)),20,20)
        X = X[:,:,0].flatten()
        Y.append(X)

    loaded_model.predict(Y)
    salida = ""
    for letter in loaded_model.predict(Y):
        print(labels[int(letter)])
        salida += labels[int(letter)]
    return salida

Prediccion()