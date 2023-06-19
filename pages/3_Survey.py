"""
Roger Lera
18/04/2023
"""
import os
import cvxpy as cp
import numpy as np
import argparse as ap
import time
import csv
from definitions import * # classes Skill, Activity, TimePeriod, TimePeriodSequence, Job, User Preference
from read_file import read_activities,skills_enumeration,topics_enumeration,read_jobs,read_input
from solve import definitions_generation,model_elements,model_ilp_mixed,solve_problem,job_affinity
from formalisation import *
from plots import *
import streamlit as st
import pandas as pd
from Home import *
from web_utils import *

st.set_page_config(
    page_title="Yoma LP",
    page_icon="👋",
)

usp = st.session_state['usp']
try:
    results = st.session_state['results']
    ja = st.session_state['ja']
    w = st.session_state['w']
    comp_ = True

except:
    results = pd.DataFrame({"Activities":[],"Starting Date (h)":[],
                         "Finishing Date (h)":[],"Budget (ZLTO)":[]})
    ja = 0.0
    w = (0,0,0)
    st.warning('You had not computed a plan yet!', icon="⚠️")
    comp_ = False

def submit_survey(list_):

    
    wd_ = 'data'
    path_ = os.getcwd()
    field_names = ['name','job','topic','weights','activities',
                    'start_date','end_date','budget','ja','survey']

    ac = list(results['Activities'])
    sd = list(results['Starting Date (h)'])
    ed = list(results['Finishing Date (h)'])
    bg = list(results['Budget (ZLTO)'])
    dict_ = {'name':usp.name,'job':usp.target_job.name,'topic':list(usp.topic_pref.values()),
            'weights':w,'activities':ac,'start_date':sd,'end_date':ed,'budget':bg,
            'ja':ja,'survey':list_}


    survey_file_path = os.path.join(path_,wd_,"survey.csv")
    with open(survey_file_path,'a') as file_:
        dict_object = csv.DictWriter(file_, fieldnames=field_names)
        dict_object.writerow(dict_)

    st.session_state['survey'] = True
    return None

surv_ = st.sidebar.button('Submit answer',disabled=st.session_state['survey'] or not comp_)

if surv_:
    submit_survey(st.session_state['survey_q'])

survey_q = []
st.write("## Survey")
if st.session_state['survey']:
    st.write("### Survey Completed! :tada: :confetti_ball:")

    link_ = st.button('Go Home')

    if link_:
        switch_page("Home")

    for i in range(3):
        st.balloons()
        time.sleep(1)
    

else:
    
    sl1 = st.select_slider(
        '##### Did you like the app?',
        options=range(1,6),
        value=(3)
        )
    survey_q.append(sl1)
    st.session_state['survey_q'] = survey_q


