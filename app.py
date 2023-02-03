import streamlit as st
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import imageio
import base64

st.set_page_config(layout="wide")
st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;font-size:15px'>SIMPLE FLOW REGIME WITH CONSTANT ADVECTION VALUES (2D Advection Diffusion Pollution Spread Math Model and PINN)</h1>", unsafe_allow_html=True)

# @st.experimental_memo(show_spinner = False)
def run_models(time_step, cx, cy, u, v, show_input = True):

  if show_input:
    st.markdown("""<h1 style='text-align: center;font-size:25px'>Results</h1>""".format(time_step, cx, cy, u, v), unsafe_allow_html=True)
    st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.markdown("""<h1 style='text-align: center;font-size:15px'>Time spent = {0}, source of pollution (cx, cy) = {1}, {2}, u = {3}, v = {4}</h1>""".format(time_step, cx, cy, u, v), unsafe_allow_html=True)
  

  with st.spinner('Importing Initial model...'):
    from math_model import generate_initial_model
  with st.spinner('Running Initial model...'):
    initial_fig = generate_initial_model(cx, cy,u,v, time_step)

  with st.spinner('Importing PINN model...'):
    from demo_client import generate_PINN_model
  with st.spinner('Running PINN model...'):
    pinn_model_time, pinn_fig = generate_PINN_model(time_step, cx, cy,u,v)
  #start time
  t1 = datetime.now()
  with st.spinner('Importing Math model...'):
    from math_model import generate_math_model
  with st.spinner('Running Math model...'):
    math_fig = generate_math_model(cx, cy,u,v, time_step)

  # time difference in milliseconds
  t2 = datetime.now()
  delta = t2 - t1
  math_model_time = delta.total_seconds() * 1000

  return pinn_model_time, math_model_time, initial_fig, pinn_fig, math_fig


def images_to_gif(images, gif_name):
  # Convert the images into a gif
  with imageio.get_writer(gif_name, mode='I') as writer:
    for image in images:
      writer.append_data(image)
      file_ = open(gif_name, "rb")
      contents = file_.read()
      data_url = base64.b64encode(contents).decode("utf-8")
      file_.close()
  return data_url


def performance_func_ui(pinn_time, math_time, initial_fig, pinn_fig, math_fig):

  img_col1, img_col2, img_col3 = st.columns(3)

  with img_col1:
    st.image('initial condition.png')

  with img_col2:
    st.image('pinn model.png')
    st.write("Time to generate PINN model **{:.3f}** milliseconds".format(str(pinn_time)))

  with img_col3:
    st.image('math model.png')
    st.write("Time to generate math model **{:.3f}** milliseconds".format(str(math_time)))

def accuracy_func_ui(time_steps_max):
  
  for timesteps in range(100, time_steps_max + 100, 100):

    run_models(timesteps, cx_dropdown, cy_dropdown, u_input, v_input, False)
    globals()[f"pinn img {timesteps}"] = imageio.imread("pinn model.png")
    globals()[f"math img {timesteps}"] = imageio.imread("math model.png")

  pinn_files = [globals()[f"pinn img {timesteps}"] for timesteps in range(100, time_steps_max + 100, 100)]
  math_files = [globals()[f"math img {timesteps}"] for timesteps in range(100, time_steps_max + 100, 100)]

  st.image(pinn_files)
  st.image(math_files)

  pinn_data_url = images_to_gif(pinn_files, 'pinn model.gif')
  st.markdown(
      f'<img src="data:image/gif;base64,{pinn_data_url}" alt="pinn model gif">',
      unsafe_allow_html=True,
  )
  math_data_url = images_to_gif(math_files, 'pinn model.gif')
  st.markdown(
      f'<img src="data:image/gif;base64,{math_data_url}" alt="pinn model gif">',
      unsafe_allow_html=True,
  )

## Dropdowns

st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.write("**Enter the values for simulation**")
time_step_dropdown = st.selectbox("Time step", np.arange(100, 1100, 100), index = 9)

st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.write("**Pollution Source Location**")
col1, col2 = st.columns(2)
with col1:
  cx_dropdown = st.selectbox("cx", np.arange(0, 110, 10), index = 6)

with col2:
  cy_dropdown = st.selectbox("cy", np.arange(0, 110, 10), index = 6)

st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.write("**velocity in x and y directions**")
col3, col4 = st.columns(2)

with col3:
  u_input = st.selectbox("u", np.arange(0.0, 5.5, 0.5), index = 6)

with col4:
  v_input = st.selectbox("v", np.arange(0.0, 5.5, 0.5), index = 4)


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

  pinn_model_time, math_model_time, initial_fig, pinn_fig, math_fig = run_models(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input)

  performance_func_ui(pinn_model_time, math_model_time, initial_fig, pinn_fig, math_fig)

# If the "ACCURACY SIMULATION" is pressed
if accuracy_simulation:

  accuracy_func_ui(time_step_dropdown)

# If "RUN BOTH" is pressed
if run_both:

  for timesteps in range(100, time_step_dropdown + 100, 100):
    pinn_model_time, math_model_time, initial_fig, pinn_fig, math_fig = run_models(timesteps, cx_dropdown, cy_dropdown, u_input, v_input, False)

    
    accuracy_func_ui(time_step_dropdown)

  performance_func_ui(pinn_model_time, math_model_time, initial_fig, pinn_fig, math_fig)
