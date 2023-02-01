import streamlit as st
import demo_client
import math_model

## Dropdowns

st.write("**Enter the values for simulation**")
time_step_dropdown = st.selectbox("Time step", ["100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"])

st.write("**Pollution Source Location**")
col1, col2 = st.columns(2)
with col1:
  cx_dropdown = st.selectbox("cx", ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])

with col2:
  cy_dropdown = st.selectbox("cy", ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])

st.write("**velocity in x and y directions**")
col3, col4 = st.columns(2)

with col3:
  u_input = st.number_input("u")

with col4:
  v_input = st.number_input("v")

##Buttons

but_col1, but_col2 = st.columns(2)

with but_col1:
  accuracy_stimulation = st.button("RUN ACCURACY STIMULATION")
  run_both = st.button("RUN BOTH")
  

with but_col2:
  speed_stimulation = st.button("RUN SPEED STIMULATION")
  clear_results = st.button("CLEAR RESULTS")

# If the "SPEED STIMULATION" is pressed
if speed_stimulation:
  st.markdown("""Time spent = {0}    source of pollution (cx, cy) = {1}, {2}    u = {3}, v = {4}""".format(time_step_dropdown, cx_dropdown, cy_dropdown, u_input, v_input))
  demo_client.generate_PINN_model(time_step_dropdown, cx_dropdown, cy_dropdown,u_input,v_input)
  math_model.generate_math_model(cx_dropdown, cy_dropdown,u_input,v_input, time_step_dropdown)
  st.write("Time to generate PINN model - 1481.868 milliseconds")