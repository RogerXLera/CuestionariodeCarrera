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
    

st.session_state['survey'] = False #survey not answered

#st.write("# Welcome to the Yoma Learning Pathway Recommender! 👋 :trumpet: :doughnut:")
st.write("# Welcome to the Yoma Learning Pathway Recommender! 👋 ")

#st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This is a demo page to test the Yoma Learning Pathway Recommender. The algorithm aims to plan a course path 
    according to your preferences. 

    To use the app, follow the next sequence of steps.

        1. Set up your preferences.
        2. Run the Learning Pathway Recommender.
        3. Answer the survey. 
    
"""
)

#link_ = st.button('Go to preferences',on_click=switch_page("Preferences"))
link_ = st.button('Go to preferences')

st.markdown(
    """


    ### Want to learn more about Yoma?
    - Check out [Yoma](https://www.yoma.africa/)
    - Create your Yoma [profile]()
    - Jump into our [opportunities](https://app.yoma.africa/opportunities) offer. 
"""
)

if link_:
    switch_page("Preferences")

    






