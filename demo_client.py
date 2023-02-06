# -*- coding: utf-8 -*-
"""demo_client.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VE2gniVJ9mgN7lWFgnjkO4SuezxDBw1j
"""

import numpy as np
import math
import pandas as pd
from numba import jit
from matplotlib import pyplot as plt
from keras import backend as K
import tensorflow as tf
from sklearn.model_selection import train_test_split
import keras
from sklearn.metrics import mean_squared_error
import time
from datetime import datetime

obs_file = "obstructions2d.csv"

def scale(num,min,max):
  middle = (min+max)/2
  #value scaled = (value-middle)/(max-middle)
  num_scaled = (num-middle)/(max-middle)
  return num_scaled


def custom_loss_wrapper(obstructions):
  def custom_loss(y_actual,y_pred):
    loss = K.mean(K.square(y_actual-y_pred))
    return loss
  return custom_loss

def generate_PINN_model(time, cx, cy,u,v):
  cx = scale(cx, 0, 100)
  cy = scale(cy, 0, 100)
  u_scaled = scale(u, 1, 5)
  v_scaled = scale(v, 1, 5)
  #time domain is [0,1000]
  time = scale(time, 0, 1000)
  test_input = []

  obs = pd.read_csv(obs_file)
  obs = obs.to_numpy()
  total_rows, total_columns = obs.shape

  for row in range(0,total_rows):
    y = scale(row, 0, 100)
    for col in range(0,total_columns):
      x = scale(col, 0, 100)
      test_input.append([time, x, y, cx, cy, u_scaled, v_scaled])
  test_input = np.vstack(test_input)


  old_model = keras.models.load_model('pollution.h5',custom_objects={'custom_loss':custom_loss_wrapper(obs)})
  X_validation = pd.DataFrame(test_input,columns =['time', 'x','y','cx','cy', 'u', 'v'])

  #start time
  t1 = datetime.now()
  Y_validation = old_model.predict(X_validation)
  # time difference in milliseconds
  t2 = datetime.now()
  delta = t2 - t1
  duration_ms = delta.total_seconds() * 1000

  Y_validation = np.array(Y_validation)
  Y_validation = Y_validation.reshape(total_rows,total_columns)
  for row in range(0,total_rows):
    for col in range(0,total_columns):
      if obs[row][col] == 999:
        Y_validation[row][col] = 'nan'
  pinn_fig = plt.figure()
  plt.imshow(Y_validation,cmap='jet',interpolation='nearest')
  plt.colorbar()
  plt.tight_layout()
  plt.savefig('pinn model.png')
  return duration_ms, pinn_fig