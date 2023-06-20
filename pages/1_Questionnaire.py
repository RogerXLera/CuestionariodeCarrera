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
    
    
except:
    J = read_jobs_a(job_file_path)
    Q = read_questions(q_file_path)
    q_id = 1
    q_response = 2
    j_tree = job_tree(J)
    q_list = Q[0].predecesor
    init_tree(j_tree)
    st.session_state['J'] = J
    st.session_state['Q'] = Q
    st.session_state['q_id'] = 1
    st.session_state['q_response'] = q_response
    st.session_state['q_list'] = q_list
    st.session_state['job_tree'] = j_tree

labels_ = ["No","Maybe","Yes"]



st.radio(Q[q_id].question, range(3), format_func=lambda x: labels_[x], key='q_response')

col1, col2 = st.columns(2)
link_1 = col1.button("Next question")
link_2 = col2.button("Recommend me jobs")

if link_1:
    q_id = questionnaire(Q,st.session_state['q_id'],st.session_state['q_response'],q_list)

elif link_2:
    q_id = questionnaire(Q,st.session_state['q_id'],st.session_state['q_response'],q_list)




