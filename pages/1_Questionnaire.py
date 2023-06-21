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

st.write("# Questionnaire")

wd_ = 'data'
path_ = os.getcwd()

job_file_path = os.path.join(path_,wd_,"anzsco.xlsx")
q_file_path = os.path.join(path_,wd_,"questions.json")
try:
    J = st.session_state['J']
    Q = st.session_state['Q']
    q_id = st.session_state['q_id']
    q_response = st.session_state['q_response']
    j_tree = st.session_state['job_tree']
    q_list = st.session_state['q_list']
    j_list = st.session_state['j_list']
    
    
except:
    J = read_jobs_a(job_file_path)
    Q = read_questions(q_file_path)
    q_id = 1
    q_response = 0
    j_tree = job_tree(J)
    q_list = Q[0].predecesor.copy()
    j_list = []
    init_tree(j_tree)
    st.session_state['J'] = J
    st.session_state['Q'] = Q
    st.session_state['q_id'] = 1
    st.session_state['q_response'] = q_response
    st.session_state['q_list'] = q_list
    st.session_state['j_list'] = j_list
    st.session_state['job_tree'] = j_tree

labels_ = ["No","A little","Yes"]


if q_id == None:
    if len(j_list) == 0:
        f"I cannot find any career that you want to pursue. Try again."

    label_button = "Try again"
else:
    st.radio(Q[q_id].question, range(3), format_func=lambda x: labels_[x], index= 0, key='q_response')
    label_button = "Next question"

col1, col2 = st.columns(2)
link_1 = col1.button(label_button)
link_2 = col2.button("Explore jobs")

if q_id == None:
    f"Some of the fields that have been selected according to your answers."
    for i in range(len(j_list)):
        st.write(f"{i+1}. {J[j_list[i]].name}")
    st.session_state['j_list'] = []
else:
    if len(j_list) >= 3:
        f"Some of the fields that have been selected according to your answers."
        for i in range(3):
            st.write(f"{i+1}. {J[j_list[i]].name}")


if link_1:
    if q_id == None:
        st.session_state['q_id'] = 1
        st.session_state['q_response'] = 0
        st.session_state['q_list'] = Q[0].predecesor.copy()
        link_1 = False
        st.experimental_rerun()
    
    q_id,q_list_new,j_list_new = questionnaire(Q,st.session_state['q_id'],st.session_state['q_response'],q_list,j_list)
    st.session_state['q_id'] = q_id
    st.session_state['q_list'] = q_list_new
    st.session_state['j_list'] = j_list_new
    link_1 = False
    st.experimental_rerun()

elif link_2:
    switch_page("Jobs")




