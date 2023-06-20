"""
Roger Lera
2023/06/20
"""
import os
import pandas as pd
import numpy as np
import csv
from definitions import * # classes Skill, Activity, TimePeriod, TimePeriodSequence, Job, User Preference, Topics
import json
import streamlit as st

def job_tree(J):

    dic = {'':{'id':'','name':'','predecesor':[]}}

    id_previous = ''
    for j in J.keys():
        job = J[j]
        for i in range(1,len(job.id)+1):
            if job.id[:-i] in dic.keys():
                dic[job.id[:-i]]['predecesor'].append(job.id)
                break
        
        dic.update({job.id:{'id':job.id,'name':job.name,'predecesor':[]}})
        id_previous = job.id

    return dic

def update_tree(dic,choice_id):

    parent = ''
    for i in range(1,len(choice_id)+1):
        if choice_id[:-i] in J.keys():
            parent = choice_id[:-i]
            break

    if choice_id not in dic[parent]['predecesor']:
        raise ValueError(f"Ancestor of {choice_id} not found")
    
    for element in dic[parent]['predecesor']:
        dic[element]['choice'] = 0
    dic[choice_id]['choice'] = 1
    return None

def init_tree(dic):

    for item in dic.keys():
        if item == '':
            st.session_state[f"job_{item}"] = True
        else:
            st.session_state[f"job_{item}"] = False
    return None

def questionnaire(Q,q_id,question_answer,q_list):

    q_list.remove(q_id)
    if q_id != 0 and len(q_list) == 0:
        "I cannot fine a suitable field for you."
        return None
    
    if question_answer == 2:
        q_list = Q[q_id].predecesor + q_list
    elif question_answer == 1:
        q_list += Q[q_id].predecesor

    q_id = q_list[0]
    return q_id

if __name__ == '__main__':
    from read_file import *
    wd_ = 'data'
    file_ = "anzsco.xlsx"
    file_path = os.path.join(os.getcwd(),wd_,file_)

    levels = ["Major Group",
              "Sub-Major Group",
              "Minor Group",
              "Unit Group",
              "Occupation"]
    J = read_jobs_a(file_path)
    dic = job_tree(J)
    for i in dic.keys():
        print(dic[i])