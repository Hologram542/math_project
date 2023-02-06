import streamlit as st
import time
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import imageio
import base64

#Stretch the wider 
st.set_page_config(layout="wide")
#Remove the unwanted space on the top
st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
#Title
st.markdown("<h1 style='text-align: center;font-size:20px;paddng-top:0rem;paddng-bottom:0rem;'>SIMPLE FLOW REGIME WITH CONSTANT ADVECTION VALUES </h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;font-size:20px;padding-top:0rem;paddng-bottom:0rem;'>(2D Advection Diffusion Pollution Spread Math Model and PINN) </h1>", unsafe_allow_html=True)



#Run the PINN model
def run_pinn_model(time_step, cx, cy, u, v):


  with st.spinner('Running PINN model...'):
    from demo_client import generate_PINN_model
  with st.spinner('Running PINN model...'):
    pinn_model_time, pinn_fig = generate_PINN_model(time_step, cx, cy,u,v)

  return pinn_model_time

#Run the math model
def run_math_model(time_step, cx, cy, u, v):

  #start time
  t1 = datetime.now()

  #Import and run the math model
  with st.spinner('Running Math model...'):
    from math_model import generate_math_model
  with st.spinner('Running Math model...'):
    math_model_time, math_fig = generate_math_model(cx, cy,u,v, time_step)

  return math_model_time



# Convert the images into a gif
def images_to_gif(gif_name, files):

  images = []
  for file in files:
    images.append(file)

  imageio.mimsave(gif_name, images, duration = 0.5)



def accuracy_func_ui(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown):

  # Add "Results" title
  st.markdown("""<h1 style='text-align: center;font-size:25px;padding-top:0rem;'>Results</h1>""", unsafe_allow_html=True)

  #Show the input values
  st.markdown("""<h1 style='text-align: center;font-size:18px;padding-top:0rem;'>PINN and Math Model Simulation for &nbsp;&nbsp; - &nbsp;&nbsp; time steps 100 to {0} ; &nbsp;&nbsp;&nbsp;&nbsp; Source of pollution cx = {1} cy = {2} ; &nbsp;&nbsp;&nbsp;&nbsp; Velocity u = {3} v = {4}</h1>""".format(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown), unsafe_allow_html=True)


  num_cols = ((time_step_dropdown)//100) + 1

  initial_cols = st.columns(5)
  text_cols = st.columns(int(num_cols))
  pinn_cols = st.columns(int(num_cols))
  math_cols = st.columns(int(num_cols))
  gif_cols = st.columns(2)


  #text_cols[0].write("**Model**")
  pinn_cols[0].write("**PINN**")
  math_cols[0].write("**Ground Truth  \n  (Math Model)**")

  
  for i, timesteps in enumerate(np.arange(100, time_step_dropdown + 1, 100)):

    
    text_cols[i+1].markdown("<h1 style='text-align: center;font-size:15px'>{}</h1>".format(timesteps), unsafe_allow_html=True)

    run_pinn_model(timesteps, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
    pinn_cols[i+1].image("pinn model.png")

    globals()[f"pinn img {timesteps}"] = imageio.imread("pinn model.png")

  for i, timesteps in enumerate(np.arange(100, time_step_dropdown +1, 100)):

    run_math_model(timesteps, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
    math_cols[i+1].image("math model.png")
    globals()[f"math img {timesteps}"] = imageio.imread("math model.png")

  pinn_files = [globals()[f"pinn img {timesteps}"] for timesteps in range(100, time_step_dropdown + 100, 100)]
  
  
  pinn_final = gif_cols[0]
  pinn_final.markdown("<h1 style='text-align: center;font-size:15px'>PINN MODEL</h1>", unsafe_allow_html=True)
  images_to_gif('pinn model.gif', pinn_files)
  pinn_final.image('pinn model.gif')




  math_files = [globals()[f"math img {timesteps}"] for timesteps in range(100, time_step_dropdown + 100, 100)]

  math_final = gif_cols[1]
  math_final.markdown("<h1 style='text-align: center;font-size:15px'>Ground Truth</h1>", unsafe_allow_html=True)
  images_to_gif('math model.gif', math_files)
  math_final.image('math model.gif')

  



## Dropdowns

st.write("**Enter the values for simulation**")

time_step_dropdown = st.selectbox("Time step", np.arange(100, 1100, 100), index = 9)


st.write("**Pollution Source Location**&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;**Velocity in x and y directions**")
col1, col2 = st.columns(2)
with col1:
  cx_dropdown = st.selectbox("cx", np.arange(0, 110, 10), index = 6)

with col2:

  u_dropdown = st.selectbox("u", np.arange(0.0, 5.5, 0.5), index = 6)


col3, col4 = st.columns(2)

with col3:

  cy_dropdown = st.selectbox("cy", np.arange(0, 110, 10), index = 6)
with col4:
  v_dropdown = st.selectbox("v", np.arange(0.0, 5.5, 0.5), index = 4)


##Buttons
but_col1, but_col2, but_col3, but_col4 = st.columns(4)


with but_col2:
  accuracy_simulation = st.button("RUN SIMULATION")

#with but_col3:
#  run_both = st.button("RUN BOTH")

with but_col4:
  clear_results = st.button("RESET SIMULATION")



# If the "ACCURACY SIMULATION" is pressed
if accuracy_simulation:

  accuracy_func_ui(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)


if clear_results:
  st.write(clear_results)
  # st.rerun()





