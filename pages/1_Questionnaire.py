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
base_link = "https://www.abs.gov.au/statistics/classifications/anzsco-australian-and-new-zealand-standard-classification-occupations/2022/browse-classification/"


if 'username' not in st.session_state.keys():
    st.write("You must introduce your Goodwall username.")
    user_name = st.text_input("Introduce Goodwall user name.",
    value="",placeholder='john_smith')
    st.session_state['username'] = user_name
    

elif len(st.session_state['username']) == 0:
    st.write("You must introduce your Goodwall username.")
    user_name = st.text_input("Introduce Goodwall user name.",
    value="",placeholder='john_smith')
    if st.session_state['username'] != user_name:
        st.session_state['username'] = user_name
        st.experimental_rerun()

else:
    st.write(f"User: {st.session_state.username}")
    if len(q_list) > 0:
        for q_id in q_list[:3]:
            st.radio(Q[q_id].question, range(3), format_func=lambda x: labels_[x], index= 0, key=f'q_response_{q_id}')
                
        label_button = "Next question"    
        link_1 = st.button(label_button)

    else:
        f"The fields selected according to your answers are the following."
        for i in range(len(j_list)):
            link = generate_link(base_link,j_list[i])
            st.write(f"{i+1}. [{J[j_list[i]].name}]({link})")
        st.session_state['j_list'] = []

        col1,col2 = st.columns(2)
        link_1 = False
        link_2a = col1.button("Try again")
        link_2b = col2.button("Submit")

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

    elif link_2a:
        st.session_state['q_id'] = 1
        st.session_state['q_response'] = 0
        st.session_state['q_list'] = Q[0].predecesor.copy()
        link_1 = False
    elif link_2b:
        submit_results()


    #elif link_2:
        #switch_page("Jobs")




