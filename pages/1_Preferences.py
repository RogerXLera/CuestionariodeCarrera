"""
Roger Lera
17/04/2023
"""
import os
import cvxpy as cp
import numpy as np
import argparse as ap
import time
import csv
from definitions import * # classes Skill, Activity, TimePeriod, TimePeriodSequence, Job, User Preference
from read_file import read_activities,skills_enumeration,topics_enumeration,read_jobs,read_input
from solve import definitions_generation,model_elements
from formalisation import *
from plots import *
import streamlit as st
from Home import *
from web_utils import *

st.set_page_config(
    page_title="Yoma LP",
    page_icon="👋",
)

labels_ = ["Not interested","Low interest","Medium interest","High interest","Total interest"]

wd_ = 'data'
path_ = os.getcwd()

act_file_path = os.path.join(path_,wd_,"activities.csv")
job_file_path = os.path.join(path_,wd_,"jobs.csv")
user_file_path = os.path.join(path_,wd_,f"input_pref_def.csv")

try:
    A = st.session_state['A']
    P = st.session_state['P']
    J = st.session_state['J']
    usp = st.session_state['usp']
    skills = st.session_state['skills']
    max_level = st.session_state['max_level']
    topics = st.session_state['topics']
except:
    A,P,J,usp,skills,max_level,topics = definitions_generation(act_file_path,job_file_path,user_file_path)
    


st.write("## Set your preferences")

st.write("First we need you to write your name. This data will just be used to ensure that every participant has complete the survey correctly.")
if 'name' not in st.session_state:
    name_ = st.text_input("Name and Surname: ", key="name", value=usp.name)
else:
    name_ = st.text_input("Name and Surname: ", key="name", value=st.session_state.name)
usp.name = name_

st.write("Now, it is time to set your preferences.")
# Add a slider to the sidebar:
if 'weeks' not in st.session_state:
    max_weeks = st.slider(
        '#### Maximum duration of the path (weeks)',
        1, 20, (usp.nperiods),key='weeks'
    )
else:
    max_weeks = st.slider(
        '#### Maximum duration of the path (weeks)',
        1, 20, (st.session_state.weeks),key='weeks'
    )
usp.nperiods = max_weeks

if 'hours' not in st.session_state:
    max_hours = st.slider(
        '#### Dedication time during the week (hours)',
        1, 40, (usp.dedication),key='hours'
    )
else:
    max_hours = st.slider(
        '#### Dedication time during the week (hours)',
        1, 40, (st.session_state.hours),key='hours'
    )
usp.dedication = max_hours

n_steps=100
labels_topics = qualitative_slider(labels_,n_steps)

st.write("#### Topics")
for topic in usp.topic_pref.keys():
    if f"topic_{topic}" not in st.session_state:
        default_index = int(usp.topic_pref[topic]*n_steps)
        slid_ = st.select_slider(topic, options=labels_topics,
                value=labels_topics[default_index],
                format_func=representation_format,
                key=f"topic_{topic}",label_visibility='visible'
        )
    else:
        #default_v = st.session_state[f"topic_{topic}"].split("/")[0]
        slid_ = st.select_slider(topic, options=labels_topics,
                value=st.session_state[f"topic_{topic}"],
                format_func=representation_format,
                key=f"topic_{topic}",label_visibility='visible'
        )
    val_ = int(slid_.split('/')[1])/n_steps
    usp.topic_pref.update({topic:val_})

st.write("#### Target Job")
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
    
job = st.selectbox(
    'Select Target Job',
     j_list,index=job_index,key='job')

for j in J:
    if job == j.name:
        usp.target_job = j
        break

st.write(f"In order to be a {j.name} we need the following skills:")
for sk in j.skills:
    st.markdown(f"\t - {sk.name} (level {sk.level})")


#link_ = st.button('Course Path',switch_page("Course Path"))
link_ = st.button('Next')

P = sequence_time_periods(usp,0)
st.session_state['A'] = A
st.session_state['P'] = P
st.session_state['J'] = J
st.session_state['usp'] = usp
st.session_state['skills'] = skills
st.session_state['max_level'] = max_level
st.session_state['topics'] = topics


if link_:
    switch_page("Learning Path")