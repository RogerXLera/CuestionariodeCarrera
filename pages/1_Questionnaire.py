"""
Roger Lera
17/04/2023
"""
import os
import numpy as np
import argparse as ap
import time
import csv
from definitions import * # classes Skill, Activity, TimePeriod, TimePeriodSequence, Job, User Preference
from read_file import *
from questionnaire import *
import streamlit as st
import pandas as pd
from Home import switch_page

st.set_page_config(
    page_title="Yoma LP",
    page_icon="👋",
)

st.write("## Learning Path")
J = st.session_state['J']
Q = st.session_state['Q']
q_id = st.session_state['q_id']
q_response = st.session_state['q_response']
job_tree = st.session_state['job_tree']



labels_ = ["No","Maybe","Yes"]
# Add a selectbox to the sidebar:
st.sidebar.title("Extra settings")
j_list = []
job_index = 0
if 'job' not in st.session_state:
    for i in range(len(J)):
        j_list.append(J[i].name)
        if J[i].name == usp.target_job:
            job_index = i
else:
    for i in range(len(J)):
        j_list.append(J[i].name)
        if J[i].name == st.session_state.job:
            job_index = i
    
job = st.sidebar.selectbox(
    'Select Target Job',
     j_list,index=job_index,key='job')

for j in J:
    if job == j.name:
        usp.target_job = j
        break

n_steps=100
labels_ = ["Null","Low","Medium","High","Top"]
labels_topics = qualitative_slider(labels_,n_steps)

# Add a slider to the sidebar:
if 'a' not in st.session_state:
    default_index = n_steps
    alpha_ = st.sidebar.select_slider('Importance of Target Job', options=labels_topics,
            value=labels_topics[default_index],
            format_func=representation_format,
            key=f"a",label_visibility='visible'
    )
else:
    alpha_ = st.sidebar.select_slider('Importance of Target Job', options=labels_topics,
            value=st.session_state.a,
            format_func=representation_format,
            key=f"a",label_visibility='visible'
    )
if 'b' not in st.session_state:
    default_index = n_steps//4
    beta_ = st.sidebar.select_slider('Importance of Finishing Early', options=labels_topics,
            value=labels_topics[default_index],
            format_func=representation_format,
            key=f"b",label_visibility='visible'
    )
else:
    beta_ = st.sidebar.select_slider('Importance of Finishing Early', options=labels_topics,
            value=st.session_state.b,
            format_func=representation_format,
            key=f"b",label_visibility='visible'
    )
if 'd' not in st.session_state:
    default_index = n_steps//2
    delta_ = st.sidebar.select_slider('Importance of Target Topics', options=labels_topics,
            value=labels_topics[default_index],
            format_func=representation_format,
            key=f"d",label_visibility='visible'
    )
else:
    delta_ = st.sidebar.select_slider('Importance of Target Topics', options=labels_topics,
            value=st.session_state.d,
            format_func=representation_format,
            key=f"d",label_visibility='visible'
    )

alpha_ = int(alpha_.split('/')[1])/100
beta_ = int(beta_.split('/')[1])/100
delta_ = int(delta_.split('/')[1])/100
w = (alpha_,beta_,delta_)

placeholder = st.sidebar.empty()

#link_1 = st.sidebar.button('Complete Survey :question:')
link_1a = placeholder.button('Complete Survey :question:',disabled = True, key="link_1a")
link_2 = st.sidebar.button('Go to preferences: :gear:')

if "link_1b" in st.session_state:
    if st.session_state['link_1b']:
        switch_page("Survey")
    

if link_1a:
    switch_page("Survey")
if link_2:
    switch_page("Preferences")

    
st.session_state['survey'] = False
with st.spinner('##### Extracting preferences... '):
    matrices = model_elements(A,P,J,usp,skills,max_level,topics)
    problem,x,x_,y,z,h = model_ilp_mixed(matrices,w,1)

st.write('##### Extracting preferences :white_check_mark:')
with st.spinner('Computing plan... '):
    
    obj_value,xx,xx_,yy,zz = solve_problem(problem,x,x_,y,z,h,"CPLEX",solvertime=20)
    #obj_value,xx,xx_,yy,zz = solve_problem(problem,x,x_,y,z,h,"ECOS_BB",max_iter=10000)
    #obj_value,xx,xx_,yy,zz = solve_problem(problem,x,x_,y,z,h,"GLPK_MI",solvertime=20,max_iter=10)
    t = matrices[24]
    ja = job_affinity(t,zz,1)
    x_ind = matrices[0]
    df_results = print_results(xx,xx_,x_ind,P)
    results = results_dataframe(df_results,P)


st.write('##### Computing plan :white_check_mark:')
st.dataframe(results)
st.write(f"##### Target Skills for {usp.target_job.name}:")
ac_object_list = name_to_object(list(results['Activities']),A)
skill_df = df_level_acquired(usp.target_job,ac_object_list)
st.table(skill_df)
st.write(f"###### Job affinity: {ja:.2f} %")


fig = gantt_diagram(df_results,font_size=15,max_characters=25)
st.plotly_chart(fig)

st.session_state['results'] = results
st.session_state['ja'] = ja
st.session_state['w'] = w

link_1b = placeholder.button('Complete Survey :question:',disabled=False,key='link_1b')
    




