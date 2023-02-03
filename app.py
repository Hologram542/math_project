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


#Run the initial model
def run_initial_model(time_step, cx, cy, u, v):

  # Add "Results" title
  st.markdown("""<h1 style='text-align: center;font-size:25px'>Results</h1>""".format(time_step, cx, cy, u, v), unsafe_allow_html=True)

  #Show the input values
  st.markdown("""<h1 style='text-align: center;font-size:15px;padding-top:0rem;'>Time step = {0}, source of pollution (cx, cy) = {1}, {2}, u = {3}, v = {4}</h1>""".format(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown), unsafe_allow_html=True)

  #Import and run the initial model
  with st.spinner('Importing Initial model...'):
    from math_model import generate_initial_model
  with st.spinner('Running Initial model...'):
    initial_fig = generate_initial_model(cx, cy,u,v, time_step)

#Run the PINN model
def run_pinn_model(time_step, cx, cy, u, v):

  # Import and run the PINN model
  with st.spinner('Importing Initial model...'):
    from math_model import generate_initial_model
  with st.spinner('Running Initial model...'):
    initial_fig = generate_initial_model(cx, cy,u,v, time_step)

  with st.spinner('Importing PINN model...'):
    from demo_client import generate_PINN_model
  with st.spinner('Running PINN model...'):
    pinn_model_time, pinn_fig = generate_PINN_model(time_step, cx, cy,u,v)

  return pinn_model_time

#Run the math model
def run_math_model(time_step, cx, cy, u, v):

  #start time
  t1 = datetime.now()

  #Import and run the math model
  with st.spinner('Importing Math model...'):
    from math_model import generate_math_model
  with st.spinner('Running Math model...'):
    math_fig = generate_math_model(cx, cy,u,v, time_step)

  # time difference in milliseconds
  t2 = datetime.now()
  delta = t2 - t1
  math_model_time = delta.total_seconds() * 1000

  return math_model_time



# Convert the images into a gif
def images_to_gif(gif_name, files):

  images = []
  for file in files:
    images.append(file)

  imageio.mimsave(gif_name, images, duration = 0.5)

#Performance function
def performance_func_ui(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown):

  upper_col1, upper_col2, upper_col3 = st.columns(3)

  lower_col1, lower_col2, lower_col3 = st.columns(3)


  with upper_col2:
    run_initial_model(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
    st.markdown("<h1 style='text-align: center;font-size:20px;padding-top:rem0;'>Initial condition</h1>", unsafe_allow_html=True)
    st.image('initial condition.png')

  with lower_col1:
    pinn_time = run_pinn_model(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
    st.markdown("<h1 style='text-align: center;font-size:20px'pading-top:rem0;'>PINN Results</h1>", unsafe_allow_html=True)
    st.image('pinn model.png')
    st.markdown(f"<h1 style='text-align: center;font-size:15px;padding-top:rem0;'>Time to generate PINN model {str(round(pinn_time, 3))} milliseconds</h1>", unsafe_allow_html=True)



  with lower_col3:
    math_time = run_math_model(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
    st.markdown("<h1 style='text-align: center;font-size:20px;padding-top:rem0;'>Ground Truth (Math Model Results)</h1>", unsafe_allow_html=True)
    st.image('math model.png')
    st.markdown(f"<h1 style='text-align: center;font-size:15px;padding-top:rem0;'>Time to generate math model {str(round(math_time, 3))} milliseconds</h1>", unsafe_allow_html=True)

def accuracy_func_ui(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown):


  num_cols = ((time_step_dropdown)//100) + 2

  initial_cols = st.columns(int(num_cols))
  text_cols = st.columns(int(num_cols))
  pinn_cols = st.columns(int(num_cols))
  math_cols = st.columns(int(num_cols))


  with initial_cols[int(num_cols)//2]:
    run_initial_model(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
    st.image('initial condition.png')
    st.markdown("<h1 style='text-align: center;font-size:15px'>Time steps</h1>", unsafe_allow_html=True)


  text_cols[0].write("**Model**")
  pinn_cols[0].write("**PINN Results**")
  math_cols[0].write("**Math Model Results (Ground Truth)**")

  
  for i, timesteps in enumerate(np.arange(100, time_step_dropdown + 1, 100)):

    
    text_cols[i+1].markdown("<h1 style='text-align: center;font-size:15px'>{}</h1>".format(timesteps), unsafe_allow_html=True)

    run_pinn_model(timesteps, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
    pinn_cols[i+1].image("pinn model.png")
    run_math_model(timesteps, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
    math_cols[i+1].image("math model.png")
    globals()[f"pinn img {timesteps}"] = imageio.imread("pinn model.png")
    globals()[f"math img {timesteps}"] = imageio.imread("math model.png")

  pinn_files = [globals()[f"pinn img {timesteps}"] for timesteps in range(100, time_step_dropdown + 100, 100)]
  math_files = [globals()[f"math img {timesteps}"] for timesteps in range(100, time_step_dropdown + 100, 100)]


  text_cols[num_cols - 1].markdown("<h1 style='text-align: center;font-size:15px'>ANIMATED GIF OF ALLMAGES TO THE LEFT</h1>", unsafe_allow_html=True)

  pinn_final = pinn_cols[num_cols - 1]
  math_final = math_cols[num_cols - 1]

  images_to_gif('pinn model.gif', pinn_files)
  images_to_gif('math model.gif', math_files)

  pinn_final.image('pinn model.gif')
  math_final.image('math model.gif')



## Dropdowns

st.markdown("<h1 style='text-align: center;font-size:20px;padding-top:rem0;'>Enter the values for simulation</h1>", unsafe_allow_html=True)

time_step_dropdown = st.selectbox("Time step", np.arange(100, 1100, 100), index = 9)


st.markdown("<h1 style='padding-top:rem0;'>Pollution Source Location</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
  cx_dropdown = st.selectbox("cx", np.arange(0, 110, 10), index = 6)

with col2:
  cy_dropdown = st.selectbox("cy", np.arange(0, 110, 10), index = 6)

st.markdown("<h1 style='padding-top:rem0;'>velocity in x and y directions</h1>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
  u_dropdown = st.selectbox("u", np.arange(0.0, 5.5, 0.5), index = 6)

with col4:
  v_dropdown = st.selectbox("v", np.arange(0.0, 5.5, 0.5), index = 4)


##Buttons

but_col1, but_col2, but_col3, but_col4 = st.columns(4)

with but_col1:
  performance_simulation = st.button("RUN PERFORMANCE SIMULATION")

with but_col2:
  accuracy_simulation = st.button("RUN ACCURACY SIMULATION")

with but_col3:
  run_both = st.button("RUN BOTH")

with but_col4:
  clear_results = st.button("CLEAR RESULTS")

# If the "PERFORMANCE SIMULATION" is pressed
if performance_simulation:

  performance_func_ui(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)

# If the "ACCURACY SIMULATION" is pressed
if accuracy_simulation:

  accuracy_func_ui(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)

# # If "RUN BOTH" is pressed
if run_both:

  performance_func_ui(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)
  accuracy_func_ui(time_step_dropdown, cx_dropdown, cy_dropdown, u_dropdown, v_dropdown)





