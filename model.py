#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Libraries
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt 

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda
from keras.layers import Convolution2D, Cropping2D
from keras.layers.pooling import MaxPooling2D


# In[2]:


file_path = 'C:/Users/hhaggan/Desktop/BehaviorCloning/data/data/'

def GetData():
    lines = []
    images = []
    center = []
    left = []
    right = []
    measurements = []

    with open(file_path + 'driving_log.csv') as csvFile:
        reader = csv.reader(csvFile)
        next(reader, None)
        for line in reader:
            steering_center = float(line[3])

            # create adjusted steering measurements for the side camera images
            correction = 0.2 # this is a parameter to tune
            steering_left = steering_center + correction
            steering_right = steering_center - correction

            measurements.append(float(line[3]))
            center.append(file_path + '/' + line[0].strip())
            left.append(file_path + '/' + line[1].strip())
            right.append(file_path + '/' + line[2].strip())
    
    images.extend(center)
    images.extend(left)
    images.extend(right)
    
    return images, measurements


# In[3]:


#data augmentation
def Augment_Data(images_path, measurements):
    augmented_images, augmented_measurements = [], []
    for image_path, measurement in zip(images_path, measurements):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        augmented_images.append(cv2.flip(image, 1))
        augmented_measurements.append(measurement*-1.0)
    return augmented_images, augmented_measurements


# In[4]:


#building NVIdia model
def Nvidia_Model():
    model = Sequential()
    model.add(Lambda(lambda x: (x / 255.0) - 0.5, input_shape=(160,320,3)))
    model.add(Cropping2D(cropping=((70, 25), (0,0))))
    model.add(Convolution2D(24,5,5, subsample=(2,2), activation='relu'))
    #model.add(MaxPooling2D())
    model.add(Convolution2D(36,5,5, subsample=(2,2),activation='relu'))
    #model.add(MaxPooling2D())
    model.add(Convolution2D(48,5,5, subsample=(2,2), activation='relu'))
    model.add(Convolution2D(64,3,3,activation='relu'))
    model.add(Convolution2D(64,3,3,activation='relu'))
    model.add(Flatten())
    model.add(Dense(100))
    model.add(Dense(50))
    model.add(Dense(10))
    model.add(Dense(1))

    return model


# In[5]:


def Train_Nvidia_Model(model, X_train, y_train):
    model.compile(loss='mse', optimizer='adam')
    model.fit(X_train, y_train, validation_split=0.2, shuffle=True, epochs=5)
    model.save('model.h5')


# In[10]:


def __main__():
    print('Getting the data for the images and the steering measurements...')
    image_path, measurements = GetData()
    print('Augmenting the existing data...')
    images, measurements = Augment_Data(image_path, measurements) 
    
    X_train = np.array(images)
    y_train = np.array(measurements)
    
    print('Training a Nvidia Model')
    NvidiaModel = Nvidia_Model()
    Train_Nvidia_Model(NvidiaModel, X_train, y_train)


# In[ ]:


__main__()


# In[ ]:




