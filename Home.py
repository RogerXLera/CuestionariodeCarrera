"""
Roger Lera
17/04/2023
"""
import os
import numpy as np
import time
import csv
from definitions import * # classes Skill, Activity, TimePeriod, TimePeriodSequence, Job, User Preference
from read_file import *
from questionnaire import *
import streamlit as st


st.set_page_config(
    page_title="Yoma LP",
    page_icon="👋",
)

def switch_page(page_name: str):

    from streamlit.runtime.scriptrunner import RerunData,RerunException
    #from streamlit import _RerunData, _RerunException
    #from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")
    
    page_name = standardize_name(page_name)

    pages = st.source_util.get_pages("Home.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

    return None

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
    st.session_state['q_id'] = q_id
    st.session_state['q_response'] = q_response
    st.session_state['q_list'] = q_list
    st.session_state['job_tree'] = j_tree

    

st.session_state['survey'] = False #survey not answered

#st.write("# Welcome to the Yoma Learning Pathway Recommender! 👋 :trumpet: :doughnut:")
st.write("# Welcome to the Yoma Career Path Questionnaire! 👋 ")

#st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This is a demo page to test the Yoma Career Path Questionnaire! The algorithm aims to suggest and help you a possible career path 
    according to your preferences and answers. 

    To use the app, follow the next sequence of steps.

        1. Explore the Career Hierarchy.
        2. Answer the questionnaire.
        3. Submit the job suggested. 
    
"""
)

st.markdown(f"Do you know your desired career role?")
# Display buttons in the same row using columns
col1, col2 = st.columns(2)
link_1 = col1.button("No, can you suggest me one?")
link_2 = col2.button("Yes, let me indicate it in the Job Hierarchy.")

st.markdown(
    """


    ### Want to learn more about Yoma?
    - Check out [Yoma](https://www.yoma.africa/)
    - Create your Yoma [profile](https://app.yoma.africa/)
    - Jump into our [opportunities](https://app.yoma.africa/opportunities) offer. 
"""
)

if link_1:
    switch_page("Questionnaire")
elif link_2:
    switch_page("Jobs")

    






