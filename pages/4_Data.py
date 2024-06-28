"""
Roger Lera
20/04/2023
"""
import os
import numpy as np
import argparse as ap
import time
import csv
from definitions import * # classes Skill, Activity, TimePeriod, TimePeriodSequence, Job, User Preference
from read_file import *
import streamlit as st
import pandas as pd
import plotly.express as px


def checking_access(user,pw,credentials):
    if user == credentials.username and pw == credentials.password:
        return True
    else:
        return False
    
def process_list_str(list_str:str) -> list:

    list_ = list_str.strip("[]").split(',')
    return [el.strip().strip("\'") for el in list_]
    
def process_data(df):

    usernames = {}
    j_list = []
    for i in range(len(df)):
        un = df['username'].iloc[i]
        list_str = df['fields'].iloc[i]
        list_ = process_list_str(list_str)
        j_list += list_
        usernames.update({un:list_})

    
    j_set = set(j_list)
    j_list = list(j_set) 
    len_u = len(usernames)
    counter = {j:0 for j in j_list if j != ''}
    for un,list_ in usernames.items():
        for j in list_:
            if j not in counter.keys():
                continue
            
            counter[j] += 1
        
    perc = [(j,val/len_u*100) for j,val in counter.items()]
    return perc
    
def bar_chart(perc,dict_,label,n:int=10):

    def sort_func(el):
        return el[1]
    
    perc.sort(reverse=True,key=sort_func)
    if len(perc) > n:

        freq = [perc[i][1] for i in range(n)]
        fields = [dict_[perc[i][0]] for i in range(n)]
    else:
        freq = [perc[i][1] for i in range(len(perc))]
        fields = [dict_[perc[i][0]] for i in range(len(perc))]

    ja_df = pd.DataFrame({'Frecuencia':freq,f'{label}':fields})
    bar = px.bar(ja_df, x=f'{label}', y='Frecuencia', orientation='v')
    bar.update_yaxes(title_text = "Frecuencia de usuarios (%)",
                    range=[0, 100],
                    tickfont=dict(size=14))
    bar.update_xaxes(tickfont=dict(size=14))
    bar.update_layout(yaxis=dict(title=dict(font=dict(size=16))),
                    xaxis=dict(title=dict(font=dict(size=16))))
    st.plotly_chart(bar)
    return None

def bar_chart_degree(perc,dict_,label,n:int=10):

    def sort_func(el):
        return el[1]
    
    perc.sort(reverse=True,key=sort_func)
    
    list_degrees = []
    freq = []
    for i in range(len(perc)):
        degrees = dict_[perc[i][0]]
        for deg in degrees:
            if deg not in list_degrees:
                list_degrees += [deg]
                freq += [perc[i][1]]


    ja_df = pd.DataFrame({'Frecuencia':freq,f'{label}':list_degrees})
    bar = px.bar(ja_df, x=f'{label}', y='Frecuencia', orientation='v')
    bar.update_yaxes(title_text = "Frecuencia de usuarios (%)",
                    range=[0, 100],
                    tickfont=dict(size=14))
    bar.update_xaxes(tickfont=dict(size=14))
    bar.update_layout(yaxis=dict(title=dict(font=dict(size=16))),
                    xaxis=dict(title=dict(font=dict(size=16))))
    st.plotly_chart(bar)
    return None

wd_ = 'data'
path_ = os.getcwd()

job_file_path = os.path.join(path_,wd_,"anzsco.xlsx")
q_file_path = os.path.join(path_,wd_,"questions.json")

try:
    J = st.session_state['J']
    j_tree = st.session_state['job_tree']
    j_dict = st.session_state['j_dict']
    degrees_dict = st.session_state['degrees_dict']
except:
    J = read_jobs_a(job_file_path)
    j_dict = read_jobs_dict()
    degrees_dict = read_degrees_dict()
    st.session_state['J'] = J
    st.session_state['j_dict'] = j_dict
    st.session_state['degrees_dict'] = degrees_dict


access = False

wd_ = 'data'
path_ = os.getcwd()

sur_file_path = os.path.join(path_,wd_,"answers.csv")

st.title("Respuestas del Cuestionario")
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

    #st.dataframe(df_)
    perc = process_data(df_)
    bar_chart(perc,j_dict,'Sectores')
    bar_chart_degree(perc,degrees_dict,'Grados Universitarios')
    csvfile_ = open(sur_file_path)
    st.download_button('Download Data :page_facing_up:',
                        data=csvfile_,file_name='AIHUB_survey.csv')
    csvfile_.close()




