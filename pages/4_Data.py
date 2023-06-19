"""
Roger Lera
20/04/2023
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


st.set_page_config(
    page_title="Yoma LP",
    page_icon="👋",
)
def checking_access(user,pw,credentials):
    if user == credentials.username and pw == credentials.password:
        return True
    else:
        return False


access = False

wd_ = 'data'
path_ = os.getcwd()

sur_file_path = os.path.join(path_,wd_,"survey.csv")

st.title("Survey answer")
st.sidebar.title("Database access")

user = st.sidebar.text_input("Username:")
pw = st.sidebar.text_input("Password:",type='password')

submit_access = st.sidebar.button("Log in")

credentials_ = st.secrets.db_credentials

if submit_access:
    access = checking_access(user,pw,credentials_)


if access:
    st.sidebar.success("Access granted!")
    df_ = pd.read_csv(sur_file_path)
    st.dataframe(df_)
    csvfile_ = open(sur_file_path)
    st.download_button('Download Data :page_facing_up:',
                        data=csvfile_,file_name='yoma_survey.csv')
    csvfile_.close()




