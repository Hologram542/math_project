import streamlit as st
from datetime import datetime

@st.experimental_memo(show_spinner = False)
def run_models(time_step, cx, cy, u, v):

  st.markdown("""Time spent = {0}, source of pollution (cx, cy) = {1}, {2}, u = {3}, v = {4}""".format(time_step, cx, cy, u, v))
  

  with st.spinner('Importing Initial model...'):
    from math_model import generate_initial_model
  with st.spinner('Running Initial model...'):
    generate_initial_model(cx, cy,u,v, time_step)

  with st.spinner('Importing PINN model...'):
    from demo_client import generate_PINN_model
  with st.spinner('Running PINN model...'):
    pinn_model_time = generate_PINN_model(time_step, cx, cy,u,v)
  #start time
  t1 = datetime.now()
  with st.spinner('Importing Math model...'):
    from math_model import generate_math_model
  with st.spinner('Running Math model...'):
    math_model_time = generate_math_model(cx, cy,u,v, time_step)

  # time difference in milliseconds
  t2 = datetime.now()
  delta = t2 - t1
  math_model_time = delta.total_seconds() * 1000

  return pinn_model_time, math_model_time


def performance_func_ui(pinn_time, math_time):

  img_col1, img_col2, img_col3 = st.columns(3)

  with img_col1:
    st.image('Initial condition.png')

  with img_col2:
    st.image('pinn model.png')
    st.write("Time to generate PINN model") 
    st.write("{} milliseconds".format(str(pinn_time)))

  with img_col3:
    st.image('math model.png')
    st.write("Time to generate math model") 
    st.write("{} milliseconds".format(str(math_time)))

def accuracy_func_ui(timsteps, pinn_time, math_time):

  num_cols = (timsteps//100) + 2

  
  # for col_num in range(1, num_cols + 1):
  #   globals()[f"variable1{col_num}"] = 
    

  st.write('work in progress')

## Dropdowns

st.write("**Enter the values for simulation**")
time_step_dropdown = int(st.selectbox("Time step", ["100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"]))

st.write("**Pollution Source Location**")
col1, col2 = st.columns(2)
with col1:
  cx_dropdown = int(st.selectbox("cx", ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]))

with col2:
  cy_dropdown = int(st.selectbox("cy", ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]))

st.write("**velocity in x and y directions**")
col3, col4 = st.columns(2)

with col3:
  u_input = st.number_input("u")

with col4:
  v_input = st.number_input("v")

##Buttons

but_col1, but_col2 = st.columns(2)

with but_col1:
  performance_stimulation = st.button("RUN PERFORMANCE STIMULATION")
  run_both = st.button("RUN BOTH")
  

with but_col2:
  accuracy_stimulation = st.button("RUN ACCURACY STIMULATION")
  clear_results = st.button("CLEAR RESULTS")

# If the "PERFORMANCE STIMULATION" is pressed
if performance_stimulation:

  st.markdown("""Time spent = {0}, source of pollution (cx, cy) = {1}, {2}, u = {3}, v = {4}""".format(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input))

  # pinn_model_time, math_model_time = run_models(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input)

  pinn_model_time, math_model_time = 1, 2000

  performance_func_ui(pinn_model_time, math_model_time)

# If the "ACCURACY STIMULATION" is pressed
if accuracy_stimulation:

  st.markdown("""Time spent = {0}, source of pollution (cx, cy) = {1}, {2}, u = {3}, v = {4}""".format(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input))

  # pinn_model_time, math_model_time = run_models(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input)

  pinn_model_time, math_model_time = 1, 2000

  accuracy_func_ui(time_step_dropdown, pinn_model_time, math_model_time)

# If "RUN BOTH" is pressed
if run_both:

  st.markdown("""Time spent = {0}, source of pollution (cx, cy) = {1}, {2}, u = {3}, v = {4}""".format(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input))

  # pinn_model_time, math_model_time = run_models(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input)

  pinn_model_time, math_model_time = 1, 2000

  performance_func_ui(pinn_model_time, math_model_time)
  accuracy_func_ui(pinn_model_time, math_model_time)

# If "CLEAR RESULTS" is pressed
if clear_results:

  st.write("Deleted")