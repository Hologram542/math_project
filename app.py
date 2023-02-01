import streamlit as st
with st.spinner('Importing functions'):
  from demo_client import generate_PINN_model
  from math_model import generate_initial_model, generate_math_model


def performance_func_ui(pinn_time, math_time):

  img_col1, img_col2, img_col3 = st.columns(3)

  with img_col1:
    st.image('pinn model.png').

  with img_col2:
    st.image('pinn model.png')
    st.write("Time to generate PINN model") 
    st.write("{} milliseconds".format(str(pinn_time)))

  with img_col3:
    st.image('pinn model.png')
    st.write("Time to generate math model") 
    st.write("{} milliseconds".format(str(math_time)))

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

# If the "SPEED STIMULATION" is pressed
if performance_stimulation:
  st.markdown("""Time spent = {0}, source of pollution (cx, cy) = {1}, {2}, u = {3}, v = {4}""".format(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input))
  
  with st.spinner('Running function...'):
    generate_initial_model(cx_dropdown, cy_dropdown,u_input,v_input, time_step_dropdown)
    math_model_time = generate_math_model(cx_dropdown, cy_dropdown,u_input,v_input, time_step_dropdown)
    pinn_model_time = generate_PINN_model(time_step_dropdown, cx_dropdown, cy_dropdown,u_input,v_input)

  performance_func_ui(pinn_model_time, pinn_model_time)

