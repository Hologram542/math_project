# -*- coding: utf-8 -*-
"""math_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l3gNuLe75dqh5YfIPz1l2Box3GQrqORi
"""

import numpy as np
import math
import pandas as pd
from matplotlib import pyplot as plt
from keras import backend as K
import tensorflow as tf
from sklearn.model_selection import train_test_split
import keras
from sklearn.metrics import mean_squared_error
from datetime import datetime
from google.colab import drive
from numba import jit

drive.mount('/content/drive')
path = "/content/drive/MyDrive/Colab Notebooks/2d ad model src u v as param/files/"
obs_file = "obstructions2d.csv"

def scale(num,min,max):
  middle = (min+max)/2
  num_scaled = (num-middle)/(max-middle)
  return num_scaled

#@jit(nopython=True)
def run_code(total_rows,total_columns,f, phi_old,obstructions, u, v, time_steps):
  #def scale(num,min,max):
    #middle = (min+max)/2
    #num_scaled = (num-middle)/(max-middle)
    #return num_scaled

  u_scaled = scale(u, 1, 5)
  v_scaled = scale(v, 1, 5)

  input = []
  output = []

  #randomly sample the initial state
  for count in range(0,500):
    row = np.random.randint(0,total_rows)
    col = np.random.randint(0,total_columns)
    if obstructions[row][col] != 999:
      x = scale(col, 0, 100)
      y = scale(row, 0, 100)
      input.append([-1,x,y,u_scaled,v_scaled])
      output.append([phi_old[row][col]])

  dt, dx, dy, D = 0.001, 0.1, 0.1, 1
  phi_new = np.zeros((total_rows,total_columns),dtype=np.float32)
  for time in range(1,time_steps):
    for row in range(0,total_rows):
      for col in range(0,total_columns):
        if obstructions[row][col] == 999:
          phi_new[row][col] = 999
        else:
          if row == 0:
            phi_above = phi_old[total_rows-1][col]
          else:
            phi_above = phi_old[row-1][col]
          if row == total_rows-1:
            phi_below = phi_old[0][col]
          else:
            phi_below = phi_old[row+1][col]
          if col == 0:
            phi_left = phi_old[row][total_columns-1]
          else:
            phi_left = phi_old[row][col-1]
          if col == total_columns-1:
            phi_right = phi_old[row][0]
          else:
            phi_right = phi_old[row][col+1]

          #BUT if the value to your right is a barrier ...
          if phi_old[row][col+1] == 999:
            phi_right = phi_old[row][col-1]
          #BUT if your value to your left is a barrier ...
          if phi_old[row][col-1] == 999:
            phi_left = phi_old[row][col+1] 
          #etc
          if phi_old[row-1][col] == 999:
            phi_above = phi_old[row+1][col]
          if phi_old[row+1][col] == 999:
            phi_below = phi_old[row-1][col]   

          laplacian = (phi_right - 2*phi_old[row][col]+phi_left)/dx**2 \
          + (phi_below - 2*phi_old[row][col]+phi_above)/dy**2
          advection_x = (phi_right - phi_left)/(2*dx)
          advection_y = (phi_below - phi_above)/(2*dy)
          rate = D*laplacian - u*advection_x - v*advection_y +f[row][col]
          phi_new[row][col] = phi_old[row][col] + dt*(rate)
    phi_old = phi_new.copy()

    if time%100 == 0:
      time_scaled = scale(time, 0, 1000)
      for count in range(0,500):
        row = np.random.randint(0,total_rows)
        col = np.random.randint(0,total_columns)
        if obstructions[row][col] != 999:
          x = (col-50)/50
          y = (row-50)/50
          input.append([time_scaled,x,y,u_scaled,v_scaled])
          output.append([phi_old[row][col]])
  return phi_old, input, output

def generate_initial_model(c_x, c_y, u, v, time_steps):
  # load obstructions
  obstructions = pd.read_csv(path+obs_file)
  obstructions = obstructions.to_numpy()
  # load pollution source
  total_rows, total_columns = obstructions.shape
  f = np.zeros((total_rows,total_columns),dtype=np.float32)
  cx = scale(c_x, 0, 100)
  cy = scale(c_y, 0, 100)
  for row in range(0,total_rows):
    # row = 0 to 100 will scale down to y = -1 to 1
    y = scale(row, 0, 100)
    for col in range(0,total_columns):
      x = scale(col, 0, 100)
      radius = ((cx-x)**2+(cy-y)**2)**0.5
      f[row][col] = 5*math.exp(-5*radius)
      if (obstructions[row][col] == 999):
        f[row][col] = 999
  f_mod = f.copy()
  f_mod[f_mod == 999] = 'nan'
  plt.imshow(f_mod, cmap='jet',interpolation='nearest')
  plt.colorbar()
  print(f"\n Initial Condition \n")
  plt.show()


def generate_math_model(c_x, c_y, u, v, time_steps):
  #generate the math model
  # SPECIFY THE VALUES FOR ALL VARIABLES HERE

  # load obstructions
  obstructions = pd.read_csv(path+obs_file)
  obstructions = obstructions.to_numpy()

  # load pollution source
  total_rows, total_columns = obstructions.shape
  f = np.zeros((total_rows,total_columns),dtype=np.float32)
  cx = scale(c_x, 0, 100)
  cy = scale(c_y, 0, 100)
  for row in range(0,total_rows):
    # row = 0 to 100 will scale down to y = -1 to 1
    y = scale(row, 0, 100)
    for col in range(0,total_columns):
      x = scale(col, 0, 100)
      radius = ((cx-x)**2+(cy-y)**2)**0.5
      f[row][col] = 5*math.exp(-5*radius)
      if (obstructions[row][col] == 999):
        f[row][col] = 999
  f_mod = f.copy()
  f_mod[f_mod == 999] = 'nan'
  plt.imshow(f_mod, cmap='jet',interpolation='nearest')
  plt.colorbar()
  #print(f"\n Initial Condition Pollution - source=({c_x},{c_y})\n")
  #plt.show()

  phi_old = np.zeros((total_rows,total_columns),dtype=np.float32)
  phi_old, input, output = run_code(total_rows,total_columns,f,phi_old,obstructions,u,v, time_steps)
  phi_old_modified = phi_old.astype('float')
  phi_old_modified[phi_old_modified==999] = 'nan'
  plt.imshow(phi_old_modified,cmap='jet',interpolation='nearest')
  plt.colorbar()
  print(f"\nMath Model - source=({c_x},{c_y}) u={u} v={v} t={time_steps}\n")
  plt.show()

# user input
# hard coded for now
c_x=60
c_y=60
u, v = 3, 2
time_steps = 1000

#start time
t1 = datetime.now()
generate_initial_model(c_x, c_y, u, v, time_steps)
generate_math_model(c_x, c_y, u, v, time_steps)
# time difference in milliseconds
t2 = datetime.now()
delta = t2 - t1
ms = delta.total_seconds() * 1000
print("")
print(f"Time to generate math model - {round(ms,3)} milliseconds\n")