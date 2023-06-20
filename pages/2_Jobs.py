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

J = st.session_state['J']
Q = st.session_state['Q']
q_id = st.session_state['q_id']
q_response = st.session_state['q_response']
job_tree = st.session_state['job_tree']
init_tree(job_tree)

def leave_checkout(tree_,id_):

    hash_ = '#######'
    job = tree_[id_]
    label = f"{hash_[:-(6-len(id_l))]} {pred['id']}: {pred['name']}"
    st.checkbox(label, value=st.session_state[f'job_{id_}'], key=f'job_{id_}')
    if st.session_state[f'job_{id_}']:
        for id_l in job['predecesor']:
            pred = tree_[id_l]
            if st.session_state[f'job_{id_l}']:
                return leave_checkout(tree_,id_l)
            else:
                label = f"{hash_[:-(6-len(id_l))]} {pred['id']}: {pred['name']}"
                st.checkbox(label, value=st.session_state[f'job_{id_l}'], key=f'job_{id_l}')
    return None
        

def create_job_checkout(tree_):

    for j in tree_.keys():
        leave_checkout(tree_,j)
                
    return None

create_job_checkout(job_tree)