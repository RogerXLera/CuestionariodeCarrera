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
from questionnaire import *
from read_file import *
import streamlit as st
from Home import *


st.set_page_config(
    page_title="Yoma LP",
    page_icon="👋",
)
wd_ = 'data'
path_ = os.getcwd()

job_file_path = os.path.join(path_,wd_,"anzsco.xlsx")
q_file_path = os.path.join(path_,wd_,"questions.json")

st.write("# Jobs Tree")
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





def leave_checkout(tree_,id_):

    hash_ = '#######'
    space_ = '              '
    job = tree_[id_]
    cbs = []
    if len(id_) > 0:
        label = f"{job['id']}: {job['name']}"
        cb = st.checkbox(label, value=st.session_state[f'job_{id_}'], key=f'job_{id_}')
        
    
    for id_l in job['predecesor']:
        pred = tree_[id_l]
        if st.session_state[f'job_{id_l}']:
            leave_checkout(tree_,id_l)
            #st.session_state[f'job_{id_}'] = True
        else:
            label = f"{pred['id']}: {pred['name']}"
            check_box = st.checkbox(label, value=st.session_state[f'job_{id_l}'], key=f'job_{id_l}')
            cbs.append(check_box)


leave_checkout(j_tree,'')