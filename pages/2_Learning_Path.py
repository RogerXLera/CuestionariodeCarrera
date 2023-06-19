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
from solve import definitions_generation,model_elements,model_ilp_mixed,solve_problem,job_affinity,print_results
from formalisation import *
from plots import *
import streamlit as st
import pandas as pd
from Home import switch_page
from web_utils import *

st.set_page_config(
    page_title="Yoma LP",
    page_icon="👋",
)

def results_dataframe_old(x_ind,x,P,usp):
    """
        This function returns a dataframe with the results of the course path.
    """
    dict_ = {}
    dedi_ = usp.dedication
    ac = [] # activity
    sd = [] # start date
    ed = [] # end date
    bg = [] # budget
    to = []
    budget_ = 0
    for p_ in P.sequence:
        for i in range(len(x)):
            if x[i] == 1:
                a = x_ind[i][0]
                p = x_ind[i][1]
                if p_.id == p.id:
                    budget_ += a.cost
                    time_ = a.time
                    peri_ = time_ // dedi_
                    if time_ % dedi_ > 0:
                        peri_ += 1
                    topic_ = ''
                    for topic in a.topics:
                        if len(topic_) > 0:
                            topic_ += f"\n - {topic.name}"
                        else:
                            topic_ += f" - {topic.name}"
                    ac.append(a.name)
                    sd.append(p_.id)
                    ed.append(p_.id + peri_ - 1)
                    bg.append(budget_)
                    to.append(topic_)

    return pd.DataFrame({"Activities":ac,"Starting Date (h)":sd,
                         "Finishing Date (h)":ed,"Budget (ZLTO)":bg,"Topics":to})

def results_dataframe(df,P):
    """
        This function returns a dataframe with the results of the course path.
    """
    dict_ = {}
    ac = [] # activity
    sd = [] # start date
    ed = [] # end date
    tr = []
    bg = [] # budget
    to = [] # topics
    budget_ = 0
    for i in range(len(df)):

        topic_ = ''
        for topic in df['activity'].iloc[i].topics:
            if len(topic_) > 0:
                topic_ += f"\n - {topic.name}"
            else:
                topic_ += f" - {topic.name}"
        budget_ += df['activity'].iloc[i].cost
        ac.append(df['activity'].iloc[i].name)
        sd.append(df['s_date'].iloc[i].id)
        ed.append(df['e_date'].iloc[i].id)
        tr.append(df['activity'].iloc[i].time)
        bg.append(budget_)
        to.append(topic_)

    return pd.DataFrame({"Activities":ac,"Starting Date (h)":sd,
                         "Finishing Date (h)":ed,"Time required (h)":tr,"Budget (ZLTO)":bg,"Topics":to})


def name_to_object(label_list,object_list):
    
    list_ = []
    for el in object_list:
        if el.name in label_list:
            list_.append(el)
    
    return list_

def df_level_acquired(job,A_):

    skill_list = []
    target_lev = []
    target_acquired = []
    course_given = []
    emoji = []
    for sk in job.skills:
        max_level = 0
        max_subject = '  ---  '
        for ac in A_:
            _,skl_ = sk.check_skill(ac.skills)
            if skl_ > max_level:
                max_level = skl_
                max_subject = ac.name
            elif skl_ == max_level and skl_ > 0:
                max_subject += f",\n{ac.name}"
        
        skill_list.append(sk.name)
        target_lev.append(sk.level)
        target_acquired.append(max_level)
        course_given.append(max_subject)
        if max_level >= sk.level:
            emoji.append('🟢')
        elif max_level == 0:
            emoji.append('🔴')
        else:
            emoji.append('🟠')

    return pd.DataFrame({"Skill":skill_list,"Target Level":target_lev,
                         "Acquired Level":target_acquired,"Course":course_given,"":emoji})


st.write("## Learning Path")

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
    st.warning('You had not defined the preferences yet!', icon="⚠️")


# Add a selectbox to the sidebar:
st.sidebar.title("Extra settings")
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
    
job = st.sidebar.selectbox(
    'Select Target Job',
     j_list,index=job_index,key='job')

for j in J:
    if job == j.name:
        usp.target_job = j
        break

n_steps=100
labels_ = ["Null","Low","Medium","High","Top"]
labels_topics = qualitative_slider(labels_,n_steps)

# Add a slider to the sidebar:
if 'a' not in st.session_state:
    default_index = n_steps
    alpha_ = st.sidebar.select_slider('Importance of Target Job', options=labels_topics,
            value=labels_topics[default_index],
            format_func=representation_format,
            key=f"a",label_visibility='visible'
    )
else:
    alpha_ = st.sidebar.select_slider('Importance of Target Job', options=labels_topics,
            value=st.session_state.a,
            format_func=representation_format,
            key=f"a",label_visibility='visible'
    )
if 'b' not in st.session_state:
    default_index = n_steps//4
    beta_ = st.sidebar.select_slider('Importance of Finishing Early', options=labels_topics,
            value=labels_topics[default_index],
            format_func=representation_format,
            key=f"b",label_visibility='visible'
    )
else:
    beta_ = st.sidebar.select_slider('Importance of Finishing Early', options=labels_topics,
            value=st.session_state.b,
            format_func=representation_format,
            key=f"b",label_visibility='visible'
    )
if 'd' not in st.session_state:
    default_index = n_steps//2
    delta_ = st.sidebar.select_slider('Importance of Target Topics', options=labels_topics,
            value=labels_topics[default_index],
            format_func=representation_format,
            key=f"d",label_visibility='visible'
    )
else:
    delta_ = st.sidebar.select_slider('Importance of Target Topics', options=labels_topics,
            value=st.session_state.d,
            format_func=representation_format,
            key=f"d",label_visibility='visible'
    )

alpha_ = int(alpha_.split('/')[1])/100
beta_ = int(beta_.split('/')[1])/100
delta_ = int(delta_.split('/')[1])/100
w = (alpha_,beta_,delta_)

placeholder = st.sidebar.empty()

#link_1 = st.sidebar.button('Complete Survey :question:')
link_1a = placeholder.button('Complete Survey :question:',disabled = True, key="link_1a")
link_2 = st.sidebar.button('Go to preferences: :gear:')

if "link_1b" in st.session_state:
    if st.session_state['link_1b']:
        switch_page("Survey")
    

if link_1a:
    switch_page("Survey")
if link_2:
    switch_page("Preferences")

    
st.session_state['survey'] = False
with st.spinner('##### Extracting preferences... '):
    matrices = model_elements(A,P,J,usp,skills,max_level,topics)
    problem,x,x_,y,z,h = model_ilp_mixed(matrices,w,1)

st.write('##### Extracting preferences :white_check_mark:')
with st.spinner('Computing plan... '):
    
    obj_value,xx,xx_,yy,zz = solve_problem(problem,x,x_,y,z,h,"CPLEX",solvertime=20)
    #obj_value,xx,xx_,yy,zz = solve_problem(problem,x,x_,y,z,h,"ECOS_BB",max_iter=10000)
    #obj_value,xx,xx_,yy,zz = solve_problem(problem,x,x_,y,z,h,"GLPK_MI",solvertime=20,max_iter=10)
    t = matrices[24]
    ja = job_affinity(t,zz,1)
    x_ind = matrices[0]
    df_results = print_results(xx,xx_,x_ind,P)
    results = results_dataframe(df_results,P)


st.write('##### Computing plan :white_check_mark:')
st.dataframe(results)
st.write(f"##### Target Skills for {usp.target_job.name}:")
ac_object_list = name_to_object(list(results['Activities']),A)
skill_df = df_level_acquired(usp.target_job,ac_object_list)
st.table(skill_df)
st.write(f"###### Job affinity: {ja:.2f} %")


fig = gantt_diagram(df_results,font_size=15,max_characters=25)
st.plotly_chart(fig)

st.session_state['results'] = results
st.session_state['ja'] = ja
st.session_state['w'] = w

link_1b = placeholder.button('Complete Survey :question:',disabled=False,key='link_1b')
    




